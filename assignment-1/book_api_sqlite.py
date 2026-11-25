"""Fetch book metadata from Open Library and store it in SQLite.

Example:
    python assignment-1/book_api_sqlite.py --query "the lord of the rings" --limit 10
"""
import argparse
import sqlite3
from pathlib import Path

import requests

DB_PATH = Path(__file__).with_name("books.db")
API_URL = "https://openlibrary.org/search.json"


def create_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            open_library_key TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            author TEXT,
            publication_year INTEGER
        )
    """)
    connection.commit()


def fetch_books(query, limit=10):
    response = requests.get(
        API_URL,
        params={"q": query, "limit": limit},
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()

    books = []
    for item in payload.get("docs", []):
        key = item.get("key")
        title = item.get("title")
        if not key or not title:
            continue

        years = item.get("first_publish_year")
        books.append({
            "key": key,
            "title": title,
            "author": ", ".join(item.get("author_name", [])[:3]) or "Unknown",
            "year": years if isinstance(years, int) else None,
        })
    return books


def save_books(connection, books):
    with connection:
        connection.executemany("""
            INSERT INTO books (open_library_key, title, author, publication_year)
            VALUES (:key, :title, :author, :year)
            ON CONFLICT(open_library_key) DO UPDATE SET
                title = excluded.title,
                author = excluded.author,
                publication_year = excluded.publication_year
        """, books)


def display_books(connection):
    rows = connection.execute("""
        SELECT title, author, publication_year
        FROM books
        ORDER BY title
    """).fetchall()

    print(f"\nBooks stored: {len(rows)}")
    for title, author, year in rows:
        print(f"- {title} | {author} | {year or 'Year unavailable'}")


def main():
    parser = argparse.ArgumentParser(description="Fetch books and store them in SQLite.")
    parser.add_argument("--query", default="python programming")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")

    books = fetch_books(args.query, args.limit)
    with sqlite3.connect(DB_PATH) as connection:
        create_table(connection)
        save_books(connection, books)
        display_books(connection)


if __name__ == "__main__":
    main()
