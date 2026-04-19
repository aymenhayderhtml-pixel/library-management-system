import httpx

# Use Open Library API (free, no key required)
SEARCH_URL = "https://openlibrary.org/search.json"
def search_external(query: str, limit: int = 10):
    """Search Open Library and return simplified book records."""
    params = {"q": query, "limit": limit}
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.get(SEARCH_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        # Graceful fallback for learning/demo
        return []
    results = []
    for doc in data.get("docs", [])[:limit]:
        authors = doc.get("author_name", [])
        first_author = authors[0] if authors else "Unknown"
        # prefer first publish year
        publish_year = ""
        if doc.get("first_publish_year"):
            publish_year = str(doc["first_publish_year"])
        title = doc.get("title", "Unknown")
        results.append({
            "id": f"ol:{doc.get('key', '').lstrip('/works/')}",
            "title": title,
            "authors": [authors[0]] if authors else ["Unknown"],
            "isbn": doc.get("isbn", [""])[0] or "",
            "published_date": publish_year,
            "description": doc.get("subtitle", ""),
            "cover_url": f"https://covers.openlibrary.org/b/id/{doc.get('cover_i')}-M.jpg"
            if doc.get("cover_i") else "",
            "available_copies": 1,  # demo value
            "total_copies": 1,
        })
    return results