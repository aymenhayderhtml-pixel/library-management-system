from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./library.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)

# Models
class BookModel(Base):
    __tablename__ = "books"
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    authors = Column(String)  # JSON list stored as string; keep simple for now
    isbn = Column(String, nullable=True)
    published_date = Column(String, nullable=True)
    description = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)

class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")

class LoanModel(Base):
    __tablename__ = "loans"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    book_id = Column(String, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    returned = Column(Boolean, default=False)
    return_date = Column(DateTime, nullable=True)