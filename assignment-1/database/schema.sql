PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    salary REAL NOT NULL CHECK (salary >= 0),
    department_id INTEGER,
    manager_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);

CREATE INDEX IF NOT EXISTS idx_employees_department
ON employees(department_id);
