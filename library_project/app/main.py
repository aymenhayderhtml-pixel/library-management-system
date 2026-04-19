import uuid
import os
import random
from datetime import datetime, timezone

from fastapi import FastAPI, Depends, Form, Request, Response, HTTPException, status, Response as FastAPIResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import db_session, BookModel, UserModel, LoanModel, init_db
from app.storage.books import add_book, get_book_by_id, search_books, delete_book as delete_book_storage
from app.storage.users import save_user, get_user_by_username
from app.storage.loans import create_loan as create_loan_storage, get_active_loans as get_active_loans_storage, return_loan as return_loan_storage
from app.services.book_search import search as search_external, invalidate_search_cache
from app.utils.make_admin import make_admin as make_admin_cli

# ---- Security ----
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)
def is_admin(user: dict) -> bool:
    return user and user.get("role") == "admin"

# ---- App ----
app = FastAPI(title="Library Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

SESSION_STORE = {}

def get_session_user(request: Request) -> dict | None:
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    return SESSION_STORE.get(session_id)

# ---- Flash helpers ----
def _flash_url(url: str, msg: str, msg_type: str = "info") -> str:
    from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
    parsed = list(urlparse(url))
    qs = parse_qs(parsed[4])
    qs["msg"] = [msg]
    qs["msg_type"] = [msg_type]
    parsed[4] = urlencode(qs, doseq=True)
    return urlunparse(parsed)

def _get_random_books(limit=20):
    words = ["science", "history", "python", "fiction", "art", "music", "mystery", "space", "fantasy", "technology", "nature", "cooking", "travel", "biography", "novel", "poetry", "magic", "code", "sea", "time"]
    topic = random.choice(words)
    invalidate_search_cache()
    external_results = search_external(topic, limit=limit)
    for b in external_results:
        add_book(b)
    random.shuffle(external_results)
    return external_results

# ---- Routes ----
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, user: dict = Depends(get_session_user)):
    books = _get_random_books(6)
    return templates.TemplateResponse("index.html", {"request": request, "user": user, "books": books})

@app.get("/books", response_class=HTMLResponse)
async def list_books(request: Request, user: dict = Depends(get_session_user), q: str = ""):
    if q:
        external_results = search_external(q, limit=20)
        for b in external_results:
            add_book(b)
        results = search_books(q)
    else:
        results = _get_random_books(20)
    return templates.TemplateResponse("books.html", {"request": request, "user": user, "books": results, "query": q})

@app.get("/books/{book_id}", response_class=HTMLResponse)
async def book_detail(request: Request, book_id: str, user: dict = Depends(get_session_user)):
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    has_active = False
    if user:
        active = get_active_loans_storage(user["id"])
        has_active = any(l["book_id"] == book_id for l in active)
    return templates.TemplateResponse("book_detail.html", {
        "request": request,
        "user": user,
        "book": book,
        "has_active_loan": has_active,
    })

# ---- Auth ----
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["password_hash"]):
        return RedirectResponse(_flash_url("/login", "Invalid credentials", "danger"), status_code=303)
    session_id = f"sess_{username}"
    SESSION_STORE[session_id] = {"username": username, "role": user["role"]}
    resp = RedirectResponse("/", status_code=303)
    resp.set_cookie("session_id", session_id, httponly=True)
    return resp

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    if get_user_by_username(username):
        return RedirectResponse(_flash_url("/register", "Username already exists", "danger"), status_code=303)
    hashed = hash_password(password)
    new_user = {"username": username, "password_hash": hashed, "role": "user"}
    save_user(new_user)
    session_id = f"sess_{username}"
    SESSION_STORE[session_id] = {"username": username, "role": new_user["role"]}
    resp = RedirectResponse("/", status_code=303)
    resp.set_cookie("session_id", session_id, httponly=True)
    return resp

@app.post("/logout")
async def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if session_id and session_id in SESSION_STORE:
        del SESSION_STORE[session_id]
    response.delete_cookie("session_id")
    return RedirectResponse("/", status_code=303)

# ---- Borrow / Return ----
@app.post("/borrow")
async def borrow_book(request: Request, book_id: str = Form(...), user: dict = Depends(get_session_user)):
    if not user:
        return RedirectResponse(_flash_url("/login", "Not authenticated", "danger"), status_code=303)
    try:
        create_loan_storage(user["id"], book_id)
        return RedirectResponse(_flash_url(f"/books/{book_id}", "Book borrowed successfully", "success"), status_code=303)
    except ValueError as e:
        return RedirectResponse(_flash_url(f"/books/{book_id}", str(e), "danger"), status_code=303)

@app.post("/return")
async def return_book(request: Request, book_id: str = Form(...), user: dict = Depends(get_session_user)):
    if not user:
        return RedirectResponse(_flash_url("/login", "Not authenticated", "danger"), status_code=303)
    try:
        return_loan_storage(user["id"], book_id)
        return RedirectResponse(_flash_url(f"/books/{book_id}", "Book returned successfully", "success"), status_code=303)
    except ValueError as e:
        return RedirectResponse(_flash_url(f"/books/{book_id}", str(e), "danger"), status_code=303)

# ---- History ----
@app.get("/history", response_class=HTMLResponse)
async def history(request: Request, user: dict = Depends(get_session_user)):
    if not user:
        return RedirectResponse("/login", status_code=303)
    show_returned = request.query_params.get("show", "active") == "returned"
    loans = get_active_loans_storage(user["id"])
    if show_returned:
        all_loans = db_session.query(LoanModel).filter(LoanModel.user_id == user["id"]).all()
        loans = [l for l in all_loans if l.returned]
    else:
        loans = [l for l in loans if not l.returned]
    enriched = []
    for l in loans:
        book = get_book_by_id(l.book_id) or {"title": "Unknown", "authors": []}
        enriched.append({"loan": l, "book": book})
    return templates.TemplateResponse("history.html", {
        "request": request,
        "user": user,
        "loans": enriched,
        "show_returned": show_returned,
    })

# ---- Admin: CRUD Books ----
@app.get("/admin/books", response_class=HTMLResponse)
async def admin_books_list(request: Request, user: dict = Depends(get_session_user)):
    if not is_admin(user):
        return RedirectResponse("/", status_code=303)
    books = db_session.query(BookModel).all()
    return templates.TemplateResponse("admin_books.html", {"request": request, "user": user, "books": books, "msg": request.query_params.get("msg"), "msg_type": request.query_params.get("msg_type", "info")})

@app.get("/admin/books/new", response_class=HTMLResponse)
async def admin_books_new(request: Request, user: dict = Depends(get_session_user)):
    if not is_admin(user):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("admin_books.html", {"request": request, "user": user, "books": [], "editing": False})

@app.get("/admin/books/{book_id}/edit", response_class=HTMLResponse)
async def admin_books_edit(request: Request, book_id: str, user: dict = Depends(get_session_user)):
    if not is_admin(user):
        return RedirectResponse("/", status_code=303)
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("admin_books.html", {"request": request, "user": user, "books": [book], "editing": True})

@app.post("/admin/books", response_class=HTMLResponse)
async def admin_books_create(request: Request, user: dict = Depends(get_session_user)):
    if not is_admin(user):
        raise HTTPException(status_code=403)
    data = {
        "title": request.query_params.get("title") or Form(...),
        "authors": (request.query_params.get("authors") or "").split(","),
        "isbn": request.query_params.get("isbn") or "",
        "total_copies": int(request.query_params.get("total_copies") or 1),
        "available_copies": int(request.query_params.get("available_copies") or 0),
        "description": request.query_params.get("description") or "",
        "cover_url": request.query_params.get("cover_url") or "",
        "id": request.query_params.get("id") or str(uuid.uuid4()),
    }
    if not data["title"]:
        return RedirectResponse("/admin/books?msg=Title+is+required&msg_type=error", status_code=303)
    if isinstance(data["authors"], str):
        data["authors"] = [a.strip() for a in data["authors"].split(",") if a.strip()]
    try:
        if data["id"]:
            existing = get_book_by_id(data["id"])
            if existing:
                for k, v in data.items():
                    setattr(existing, k, v)
                db_session.add(existing)
            else:
                db_book = BookModel(**data)
                db_session.add(db_book)
        else:
            db_book = BookModel(**data)
            db_session.add(db_book)
        db_session.commit()
        return RedirectResponse("/admin/books?msg=Book+saved&msg_type=success", status_code=303)
    except Exception as e:
        return RedirectResponse(f"/admin/books?msg=Error+saving+book&msg_type=error&detail={str(e)}", status_code=303)

@app.delete("/admin/books/{book_id}", response_class=HTMLResponse)
async def admin_books_delete(book_id: str, user: dict = Depends(get_session_user)):
    if not is_admin(user):
        raise HTTPException(status_code=403)
    try:
        delete_book_storage(book_id)
        db_session.query(LoanModel).filter(LoanModel.book_id == book_id).delete()
        db_session.commit()
        return JSONResponse({"ok": True})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---- Hidden helper: promote user to admin (POST JSON) ----
@app.post("/admin/make_user", response_class=JSONResponse)
async def make_admin_endpoint(request: Request):
    if not is_admin(request.user):
        raise HTTPException(status_code=403)
    body = await request.json()
    username = body.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="username required")
    user = db_session.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = "admin"
    db_session.commit()
    make_admin_cli(username)
    return {"ok": True, "username": username, "role": "admin"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)