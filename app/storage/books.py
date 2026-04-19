import json
from typing import List, Dict, Optional
from app.database import db_session, BookModel
def search_books(query: str) -> List[Dict]:
    q = query.strip().lower()
    if not q:
        return [book_to_dict(b) for b in db_session.query(BookModel).all()]
    # naive search across title and authors (authors stored as JSON string)
    books = db_session.query(BookModel).filter(
        (BookModel.title.ilike(f"%{q}%")) |
        (BookModel.authors.ilike(f"%{q}%"))
    ).all()
    return [book_to_dict(b) for b in books]
def get_book_by_id(book_id: str) -> Optional[Dict]:
    b = db_session.query(BookModel).get(book_id)
    return book_to_dict(b) if b else None
def add_book(book: dict) -> dict:
    # normalize fields
    book.setdefault("total_copies", 1)
    if "available_copies" not in book:
        book["available_copies"] = book["total_copies"]
    # ensure authors is a JSON string for simple storage
    if "authors" in book and isinstance(book["authors"], list):
        book["authors"] = json.dumps(book["authors"])
    elif "authors" not in book:
        book["authors"] = json.dumps([])
    # idempotent: if id present, update; else insert
    existing = db_session.query(BookModel).get(book["id"]) if "id" in book else None
    if existing:
        for k, v in book.items():
            setattr(existing, k, v)
        db_session.add(existing)
        result = existing
    else:
        result = BookModel(**book)
        db_session.add(result)
    db_session.commit()
    return book_to_dict(result)

def delete_book(book_id: str):
    """Delete a book by ID. Raises ValueError if not found."""
    book = db_session.query(BookModel).get(book_id)
    if not book:
        raise ValueError("Book not found")
    db_session.delete(book)
    db_session.commit()

def book_to_dict(b: BookModel) -> Dict:
    return {
        "id": b.id,
        "title": b.title,
        "authors": json.loads(b.authors) if b.authors else [],
        "isbn": b.isbn,
        "published_date": b.published_date,
        "description": b.description,
        "cover_url": b.cover_url,
        "total_copies": b.total_copies,
        "available_copies": b.available_copies,
    }