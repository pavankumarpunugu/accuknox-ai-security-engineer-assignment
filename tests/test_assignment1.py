import importlib.util
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_book_table_and_upsert():
    module = load_module("assignment-1/book_api_sqlite.py", "books_module")
    with sqlite3.connect(":memory:") as connection:
        module.create_table(connection)
        sample = [{"key": "/works/OL1W", "title": "Sample", "author": "A", "year": 2020}]
        module.save_books(connection, sample)
        module.save_books(connection, sample)
        count = connection.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        assert count == 1


def test_job_match():
    module = load_module(
        "assignment-1/advanced_python/job_eligibility_analyzer.py", "job_module"
    )
    candidate = module.Candidate("Test", {"python", "sql"}, 0)
    job = module.Job("Junior", {"python", "sql"}, 0)
    result = module.analyze_match(candidate, job)
    assert result["eligible_by_rules"] is True
    assert result["skill_match_percent"] == 100.0
