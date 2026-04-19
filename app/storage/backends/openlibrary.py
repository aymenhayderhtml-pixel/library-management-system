import requests
from typing import List, Dict

BASE_SEARCH = "https://openlibrary.org/search.json"

def search_books(query: str, limit: int = 10) -> List[Dict]:
    params = {"q": query, "limit": limit}
    try:
        resp = requests.get(BASE_SEARCH, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        docs = data.get("docs", [])
        out = []
        for doc in docs:
            authors = doc.get("author_name", [])
            out.append({
                "id": f"ol:{doc.get('key', '').lstrip('/works/')}",
                "title": doc.get("title", "Unknown"),
                "authors": authors,
                "isbn": doc.get("isbn", [None])[0],
                "published_date": doc.get("first_publish_year"),
                "description": None,
                "cover_url": f"https://covers.openlibrary.org/b/id/{doc.get('cover_i')}-M.jpg" if doc.get("cover_i") else None,
                "total_copies": 1,
                "available_copies": 1,
            })
        return out
    except Exception:
        return []

def get_book_details(identifier: str) -> Dict | None:
    if identifier.startswith("ol:"):
        key = identifier[3:]
        url = f"https://openlibrary.org/works/{key}.json"
    else:
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{identifier}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {"id": identifier, "raw": data}
    except Exception:
        return None