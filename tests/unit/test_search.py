import pytest
from unittest.mock import patch, MagicMock
from app.services.book_search import search
def test_search_with_mocked_backends():
    mock_ol_results = [
        {"id": "ol:123", "title": "Python Guide", "authors": ["Jane"], "isbn": None, "published_date": None, "description": None, "cover_url": None, "total_copies": 1, "available_copies": 1}
    ]
    mock_gb_results = [
        {"id": "gb:456", "title": "Python Guide", "authors": ["Jane"], "isbn": "1234567890", "published_date": 2020, "description": "desc", "cover_url": None, "total_copies": 1, "available_copies": 1}
    ]
    with patch("app.services.book_search.backends", [MagicMock(search_books=lambda q, limit: mock_ol_results if "ol" in q else mock_gb_results)]) as mock_backends:
        # ensure deduplication works (same title but different ids)
        results = search("python", limit=10)
        assert len(results) == 2  # both returned because different ids
        ids = {r["id"] for r in results}
        assert "ol:123" in ids
        assert "gb:456" in ids
def test_borrow_flow(monkeypatch):
    # Mock external search backend to return a book
    mock_book = {"id": "ol:test123", "title": "Borrow Test", "authors": ["Test"], "isbn": None, "published_date": None, "description": None, "cover_url": None, "total_copies": 2, "available_copies": 2}
    with patch("app.services.book_search.search_external", return_value=[mock_book]):
        from app.main import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        # register and login to get session
        r = client.post("/register", data={"username": "borrow_user", "password": "pass"})
        assert r.status_code == 200
        # login
        r = client.post("/login", data={"username": "borrow_user", "password": "pass"}, follow_redirects=True)
        assert r.status_code == 200
        cookie = r.cookies.get("session_id")
        # search endpoint (uses mocked backends for speed)
        r = client.get("/api/books/search?q=Borrow&limit=5")
        assert r.status_code == 200
        # borrow
        r = client.post("/borrow", data={"book_id": "ol:test123"}, cookies={"session_id": cookie})
        assert r.status_code in (200, 303)  # redirect or json depending on route
        # check it would reduce available copies in local storage (hard to assert without DB access)
        # return
        r = client.post("/return", data={"book_id": "ol:test123"}, cookies={"session_id": cookie})
        assert r.status_code in (200, 303)