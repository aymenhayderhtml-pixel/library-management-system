import time
from typing import Any

TTL = 300  # seconds

_STORE = {}

def _key(*parts) -> str:
    return "|".join(str(p) for p in parts)

def get(key: str) -> Any:
    entry = _STORE.get(key)
    if not entry:
        return None
    if time.time() - entry["at"] > entry["ttl"]:
        del _STORE[key]
        return None
    return entry["value"]

def set(key: str, value: Any, ttl: int = TTL):
    _STORE[key] = {"value": value, "at": time.time(), "ttl": ttl}

def invalidate_prefix(prefix: str):
    keys_to_delete = [k for k in _STORE.keys() if k.startswith(prefix)]
    for k in keys_to_delete:
        del _STORE[k]