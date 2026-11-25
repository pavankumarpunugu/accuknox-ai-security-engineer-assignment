"""Validate a CSV file and import users into SQLite using a transaction."""
import csv
import re
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "users.csv"
DB_PATH = BASE_DIR / "users.db"
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def create_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    connection.commit()


def import_users(connection, csv_path):
    inserted = 0
    skipped = 0

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        required = {"name", "email"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("CSV must contain 'name' and 'email' columns.")

        with connection:
            for row in reader:
                name = (row.get("name") or "").strip()
                email = (row.get("email") or "").strip().lower()

                if not name or not EMAIL_PATTERN.match(email):
                    skipped += 1
                    continue

                cursor = connection.execute(
                    "INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
                    (name, email),
                )
                if cursor.rowcount:
                    inserted += 1
                else:
                    skipped += 1

    return inserted, skipped


def main():
    with sqlite3.connect(DB_PATH) as connection:
        create_table(connection)
        inserted, skipped = import_users(connection, CSV_PATH)
        users = connection.execute(
            "SELECT id, name, email FROM users ORDER BY id"
        ).fetchall()

    print(f"Inserted: {inserted}; skipped/duplicate/invalid: {skipped}")
    for user in users:
        print(user)


if __name__ == "__main__":
    main()
