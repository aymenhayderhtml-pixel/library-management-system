import importlib
from typing import List, Dict
from app.utils.cache import get as cache_get, set as cache_set, invalidate_prefix, TTL

backends = []

def _load_backends():
    global backends
    if backends:
        return
    try:
        ol = importlib.import_module("app.storage.backends.openlibrary")
        backends.append(ol)
    except Exception:
        pass
    try:
        gb = importlib.import_module("app.storage.backends.googlebooks")
        backends.append(gb)
    except Exception:
        pass

def search(query: str, limit: int = 10) -> List[Dict]:
    _load_backends()
    cache_key = f"search:{query}:{limit}"
    cached = cache_get(cache_key)
    if cached is not None:
        return cached

    results = []
    seen_ids = set()
    for backend in backends:
        try:
            items = backend.search_books(query, limit=limit)
            for item in items:
                if item["id"] not in seen_ids:
                    seen_ids.add(item["id"])
                    results.append(item)
            if len(results) >= limit:
                break
        except Exception:
            continue
    results = results[:limit]
    cache_set(cache_key, results, ttl=TTL)
    return results

def invalidate_search_cache():
    invalidate_prefix("search:")