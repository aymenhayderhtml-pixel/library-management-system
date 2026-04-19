import pathlib
content = '''import pytest
from app.database import db_session, BookModel, UserModel, LoanModel

def setup_module(module):
    from app.database import engine
    BookModel.__table__.drop(engine, checkfirst=True)
    UserModel.__table__.drop(engine, checkfirst=True)
    LoanModel.__table__.drop(engine, checkfirst=True)
    BookModel.__table__.create(engine)
    UserModel.__table__.create(engine)
    LoanModel.__table__.create(engine)

def teardown_module(module):
    engine = db_session.get_bind()
    BookModel.__table__.drop(engine, checkfirst=True)
    UserModel.__table__.drop(engine, checkfirst=True)
    LoanModel.__table__.drop(engine, checkfirst=True)

def test_book_crud():
    from app.storage.books import add_book, get_book_by_id, search_books
    book = {"title": "Test Book", "authors": ["Author A"], "total_copies": 3}
    added = add_book(book)
    assert added["id"] is not None
    assert added["title"] == "Test Book"
    assert added["available_copies"] == 3
    fetched = get_book_by_id(added["id"])
    assert fetched is not None
    assert fetched["title"] == "Test Book"
    results = search_books("Test")
    assert len(results) >= 1

def test_user_storage():
    from app.storage.users import save_user, get_user_by_username
    user = {"username": "testuser", "password_hash": "hash", "role": "user"}
    saved = save_user(user)
    assert saved["id"] is not None
    fetched = get_user_by_username("testuser")
    assert fetched is not None
    assert fetched["username"] == "testuser"

def test_loan_availability():
    from app.storage.books import add_book
    from app.storage.loans import create_loan, get_active_loans, return_loan
    book = add_book({"title": "Loan Test", "authors": ["A"], "total_copies": 1})
    user_id = "user_123"
    loan = create_loan(user_id, book["id"])
    assert loan["returned"] is False
    active = get_active_loans(user_id)
    assert len(active) == 1
    with pytest.raises(ValueError, match="No copies available"):
        create_loan("user_456", book["id"])
    returned = return_loan(user_id, book["id"])
    assert returned["returned"] is True
    active = get_active_loans(user_id)
    assert len(active) == 0
    loan2 = create_loan("user_789", book["id"])
    assert loan2["returned"] is False
'''
path = pathlib.Path('tests/unit/test_storage.py')
path.write_text(content)
print('done')