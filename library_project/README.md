# Library Management System (Prototype)

This is a Python-first prototype for a local library management system. It uses FastAPI for the API layer, Pydantic for validation, and JSON files (SQLite optional) for storage. Designed for learning and optional later publishing.

Features planned:
- Catalog / search books via free book API (e.g., Open Library)
- Borrow / return books
- Admin + user roles with login (local users)
- Web UI (HTMX templates for simplicity)
- Local development

Tech stack:
- Language: Python
- API: FastAPI
- Validation/Serialization: Pydantic
- Storage: JSON files (SQLite as lightweight option); later can scale to NoSQL like MongoDB
- Auth: passlib + BCrypt, session-based auth
- Frontend: HTML templates (optional SPA later)
- Testing: pytest
- AI assistance: Extensive inline comments and modular design for AI-based continuation

Environment:
- Copy `.env.example` to `.env` and set `GOOGLE_BOOKS_API_KEY` if you want Google Books results.

Getting started (local):
- Ensure Python 3.10+.
- Install dependencies: `pip install -r requirements.txt`
- Run: `uvicorn app.main:app --reload`
- Open http://localhost:8000/docs for API docs

Project structure:
- app/
  - main.py (FastAPI app, routes)
  - models.py (Pydantic schemas, storage models)
  - storage/ (json files / sqlite helpers)
  - auth.py (user auth helpers)
  - services/ (book API integration, borrowing logic)
  - templates/ (HTMX templates)
  - static/ (css/js)
- tests/
  - unit/
  - integration/
- scripts/
  - seed.py (seed free API data)

Notes: Designed for easy AI continuation — clear module boundaries and inline guidance.