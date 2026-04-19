# Library Management System — Ready to Use

## Quick Start (Local Development)
```bash
# 1. Copy environment template
cp .env.example .env
# Edit .env and add GOOGLE_BOOKS_API_KEY if desired

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 in your browser.

## API Endpoints
- `GET /` — Web UI home
- `GET /books` — Catalog/search (HTMX-powered)
- `GET /books/{id}` — Book detail with borrow form
- `POST /register` — Create local user
- `POST /login` — Sign in (session cookie)
- `POST /logout` — Sign out
- `POST /borrow` — Borrow a book (requires login)
- `POST /return` — Return a book (requires login)
- `GET /api/books/search?q=…&limit=10` — JSON search (Open Library + optional Google Books)

## Features
- Local JSON storage (swapable to SQLite/MongoDB)
- Two free book backends: Open Library (no key) and Google Books (optional API key)
- Unified search with deduplication and 5-minute cache (invalidated on borrow/return)
- Session-based auth with password hashing (bcrypt)
- HTMX-based web UI for quick iteration
- Comprehensive inline documentation for AI continuation

## Project Notes for AI
- All modules include inline guidance for continuation.
- Storage files are in `app/storage/` (`books.json`, `users.json`, `loans.json`).
- Cache lives in `app/utils/cache.py` (TTL 300s, prefix `search:`).
- Backend adapters are in `app/storage/backends/`.
- To add persistence (SQLite/Mongo), modify `app/storage/books.py`, `users.py`, `loans.py`.

## Testing (no test suite yet)
```bash
# Quick smoke test
python -c "from fastapi.testclient import TestClient; from app.main import app; c=TestClient(app); r=c.get('/api/books/search?q=python&limit=2'); print(r.status_code, len(r.json()))"
```

## Next Enhancements (optional)
- Add SQLite via SQLAlchemy for robust data.
- Add admin dashboard.
- Add pagination and advanced filters.
- Add frontend tests (Playwright) and unit tests (pytest).
- Containerize with Docker.
- Deploy to Render / Railway.