import os
import requests
from typing import List, Dict, Optional

API_URL = "https://www.googleapis.com/books/v1/volumes"

def search_books(query: str, limit: int = 10) -> List[Dict]:
    params = {"q": query, "maxResults": limit}
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    if api_key:
        params["key"] = api_key
    try:
        resp = requests.get(API_URL, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        out = []
        for item in items:
            info = item.get("volumeInfo", {})\n            industry_ids = info.get("industryIdentifiers", [])
            isbn = None
            for id_entry in industry_ids:
                if id_entry.get("type") in ("ISBN_13", "ISBN_10"):
                    isbn = id_entry.get("identifier")
                    break
            out.append({
                "id": f"gb:{item.get('id')}",
                "title": info.get("title", "Unknown"),
                "authors": info.get("authors", []),
                "isbn": isbn,
                "published_date": info.get("publishedDate"),
                "description": info.get("description"),
                "cover_url": info.get("imageLinks", {}).get("thumbnail"),
                "total_copies": 1,
                "available_copies": 1,
            })
        return out
    except Exception:
        return []

def get_book_details(identifier: str) -> Optional[Dict]:
    is_isbn = identifier.startswith("978") or identifier.startswith("979") or identifier.startswith("0")
    if is_isbn:
        url = f"{API_URL}?q=isbn:{identifier}"
    else:
        url = f"{API_URL}/{identifier}"
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    if api_key:
        if "?" in url:
            url += f"&key={api_key}"
        else:
            url += f"?key={api_key}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        if not items:
            return None
        item = items[0]
        info = item.get("volumeInfo", {})\n        industry_ids = info.get("industryIdentifiers", [])
        isbn = None
        for id_entry in industry_ids:
            if id_entry.get("type") in ("ISBN_13", "ISBN_10"):
                isbn = id_entry.get("identifier")
                break
        return {
            "id": f"gb:{item.get('id')}",
            "title": info.get("title", "Unknown"),
            "authors": info.get("authors", []),
            "isbn": isbn,
            "published_date": info.get("publishedDate"),
            "description": info.get("description"),
            "cover_url": info.get("imageLinks", {}).get("thumbnail"),
            "total_copies": 1,
            "available_copies": 1,
        }
    except Exception:
        return None