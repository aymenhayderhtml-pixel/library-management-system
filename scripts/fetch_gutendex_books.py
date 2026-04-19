#!/usr/bin/env python3
"""
Fetch public domain books from Gutendex API and store results into an SQLite DB
and local files (EPUBs) under the project workspace.
"""

import argparse
import json
import sqlite3
import time
import requests
from pathlib import Path
from urllib.parse import urljoin

# ---------- Configuration ----------
EPUB_FALLBACK_ORDER = [
    "text/plain; charset=utf-8",
    "text/html",
    "application/epub+zip",
]
DELAY_SECONDS = 1  # Respectful delay between requests

# ---------- Helpers ----------
def pick_format_url(formats):
    for fmt in EPUB_FALLBACK_ORDER:
        url = formats.get(fmt)
        if url:
            return url
    return None

def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)

# ---------- Core fetch & store ----------
def fetch_and_store(root_dir, max_pages=None):
    root = Path(root_dir).resolve()
    db_path = root / "library.db"
    out_dir = root / "gutendex_output" / "epubs"
    json_path = root / "gutendex_output" / "books.json"
    ensure_dir(out_dir)

    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            authors TEXT NOT NULL,
            summaries TEXT,
            subjects TEXT,
            languages TEXT,
            download_count INTEGER,
            formats_url TEXT
        )
    """)
    conn.commit()

    base_url = "https://gutendex.com/books"
    params = {
        "languages": "en",
        "copyright": "false",
        "sort": "popular",
        "limit": 32,
    }

    all_books = []
    next_url = f"{base_url}?{requests.compat.urlencode(params)}"
    page = 0

    while next_url:
        page += 1
        if max_pages and page > max_pages:
            print(f"Reached max_pages={max_pages}. Stopping.")
            break

        print(f"[Page {page}] Fetching: {next_url}")
        resp = requests.get(next_url, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        for item in data.get("results", []):
            book_id = str(item.get("id", ""))
            title = item.get("title", "").strip()
            authors = [a.get("name", "") for a in (item.get("authors") or [])]
            # Keep authors as JSON string for SQLite TEXT column
            authors_json = json.dumps(authors, ensure_ascii=False)
            summary = item.get("summary", "")
            subjects = json.dumps(item.get("subjects", []), ensure_ascii=False)
            languages = json.dumps(item.get("languages", []), ensure_ascii=False)
            download_count = int(item.get("download_count", 0))
            formats_url = pick_format_url(item.get("formats", {}))

            # Insert or ignore
            conn.execute("""
                INSERT OR IGNORE INTO books
                (id, title, authors, summaries, subjects, languages,
                 download_count, formats_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (book_id, title, authors_json, summary,
                  subjects, languages, download_count, formats_url))
            conn.commit()

            all_books.append({
                "id": book_id,
                "title": title,
                "authors": authors,
                "summaries": summary,
                "subjects": json.loads(subjects),
                "languages": json.loads(languages),
                "download_count": download_count,
                "formats_url": formats_url,
            })

            # Download ebook file if available
            if formats_url:
                filename = f"{book_id}_{title[:40]}.epub"
                safe = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_'))
                dest = out_dir / safe.strip()
                try:
                    dl = requests.get(formats_url, stream=True, timeout=60)
                    dl.raise_for_status()
                    with open(dest, "wb") as f:
                        for chunk in dl.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"  Downloaded: {safe}")
                except Exception as e:
                    print(f"  Download failed: {e}")

        # Pagination
        next_url = data.get("next")
        if next_url:
            print(f"Next page available. Sleeping {DELAY_S} before next request.")
            time.sleep(DELAY_SECONDS)

    conn.close()

    # Save JSON output
    json_path.write_text(json.dumps(all_books, indent=2, ensure_ascii=False))
    print(f"\nDone. Total books processed: {len(all_books)}")
    print(f"SQLite DB: {db_path}")
    print(f"JSON list: {json_path}")
    print(f"Ebooks: {out_dir}")

# ---------- CLI ----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Gutendex books into project SQLite.")
    parser.add_argument("--root", default=".", help="Project root directory (default: current directory)")
    parser.add_argument("--pages", type=int, default=None, help="Max pages to fetch (default: all)")
    args = parser.parse_args()
    fetch_and_store(args.root, max_pages=args.pages)