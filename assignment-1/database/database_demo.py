"""Create and query a small relational database demonstrating joins and aggregates."""
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / "company.db"


def main():
    schema = (HERE / "schema.sql").read_text(encoding="utf-8")

    with sqlite3.connect(DB_PATH) as connection:
        connection.executescript(schema)

        connection.executemany(
            "INSERT OR IGNORE INTO departments VALUES (?, ?)",
            [(1, "Engineering"), (2, "HR"), (3, "Data")],
        )
        connection.executemany("""
            INSERT OR IGNORE INTO employees
            (employee_id, employee_name, email, salary, department_id, manager_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (101, "Anita", "anita@example.com", 65000, 1, None),
            (102, "Bharat", "bharat@example.com", 52000, 1, 101),
            (103, "Charan", "charan@example.com", 48000, 2, None),
            (104, "Divya", "divya@example.com", 72000, 3, None),
        ])

        rows = connection.execute("""
            SELECT d.department_name,
                   COUNT(e.employee_id) AS employee_count,
                   ROUND(AVG(e.salary), 2) AS average_salary
            FROM departments d
            LEFT JOIN employees e ON e.department_id = d.department_id
            GROUP BY d.department_id, d.department_name
            ORDER BY d.department_name
        """).fetchall()

        print("Department summary")
        for row in rows:
            print(row)

        minimum_salary = 55000
        high_earners = connection.execute(
            "SELECT employee_name, salary FROM employees WHERE salary > ?",
            (minimum_salary,),
        ).fetchall()
        print(f"\nEmployees earning more than {minimum_salary}:")
        for row in high_earners:
            print(row)


if __name__ == "__main__":
    main()
