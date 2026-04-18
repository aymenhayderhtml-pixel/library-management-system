import uuid
from typing import Optional, List
from datetime import datetime, timezone
from app.database import db_session, LoanModel, BookModel

def create_loan(user_id: str, book_id: str) -> dict:
    # ensure book exists and availability
    book = db_session.query(BookModel).get(book_id)
    if not book:
        raise ValueError("Book not found")
    # compute lent count
    lent = db_session.query(LoanModel).filter(
        LoanModel.book_id == book_id,
        LoanModel.returned == False
    ).count()
    if lent >= book.total_copies:
        raise ValueError("No copies available")
    # check if user already has an active loan for this book
    existing = db_session.query(LoanModel).filter(
        LoanModel.user_id == user_id,
        LoanModel.book_id == book_id,
        LoanModel.returned == False
    ).first()
    if existing:
        raise ValueError("You already have this book borrowed")
    due = datetime.now(timezone.utc) + _delta_days(14)
    loan = LoanModel(
        id=str(uuid.uuid4()),
        user_id=user_id,
        book_id=book_id,
        borrow_date=datetime.now(timezone.utc),
        due_date=due,
        returned=False,
    )
    # decrease available copies
    book.available_copies = max(0, book.available_copies - 1)
    db_session.add(loan)
    db_session.commit()
    return loan_to_dict(loan)

def get_active_loans(user_id: str) -> List[dict]:
    loans = db_session.query(LoanModel).filter(
        LoanModel.user_id == user_id,
        LoanModel.returned == False
    ).all()
    return [loan_to_dict(l) for l in loans]

def get_user_loans(user_id: str) -> List[dict]:
    """Get ALL loans (active + returned) for the user, ordered by borrow date desc."""
    loans = db_session.query(LoanModel).filter(
        LoanModel.user_id == user_id,
    ).order_by(LoanModel.borrow_date.desc()).all()
    return [loan_to_dict(l) for l in loans]

def user_has_active_loan(user_id: str, book_id: str) -> bool:
    """Check if a user currently has an active (unreturned) loan for a specific book."""
    loan = db_session.query(LoanModel).filter(
        LoanModel.user_id == user_id,
        LoanModel.book_id == book_id,
        LoanModel.returned == False
    ).first()
    return loan is not None

def return_loan(user_id: str, book_id: str) -> dict:
    loan = db_session.query(LoanModel).filter(
        LoanModel.user_id == user_id,
        LoanModel.book_id == book_id,
        LoanModel.returned == False
    ).first()
    if not loan:
        raise ValueError("Active loan not found")
    loan.returned = True
    loan.return_date = datetime.now(timezone.utc)
    # increase available copies
    book = db_session.query(BookModel).get(book_id)
    if book:
        book.available_copies = min(book.total_copies, book.available_copies + 1)
    db_session.commit()
    return loan_to_dict(loan)

def loan_to_dict(l: LoanModel) -> dict:
    from .books import book_to_dict
    book = db_session.query(BookModel).get(l.book_id) if l.book_id else None
    book_d = book_to_dict(book) if book else {}
    return {
        "id": l.id,
        "user_id": l.user_id,
        "book_id": l.book_id,
        "borrow_date": l.borrow_date.isoformat() if l.borrow_date else None,
        "due_date": l.due_date.isoformat() if l.due_date else None,
        "returned": l.returned,
        "return_date": l.return_date.isoformat() if l.return_date else None,
        "book": book_d,
    }

def _delta_days(n: int):
    from datetime import timedelta
    return timedelta(days=n)