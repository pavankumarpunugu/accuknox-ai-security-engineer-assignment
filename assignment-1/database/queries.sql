-- 1. List employees with their department names.
SELECT e.employee_name, e.email, d.department_name
FROM employees AS e
LEFT JOIN departments AS d
    ON e.department_id = d.department_id
ORDER BY e.employee_name;

-- 2. Average salary by department.
SELECT d.department_name, ROUND(AVG(e.salary), 2) AS average_salary
FROM departments AS d
JOIN employees AS e ON e.department_id = d.department_id
GROUP BY d.department_id, d.department_name
ORDER BY average_salary DESC;

-- 3. Departments whose average salary exceeds a chosen threshold.
SELECT d.department_name, AVG(e.salary) AS average_salary
FROM departments AS d
JOIN employees AS e ON e.department_id = d.department_id
GROUP BY d.department_id, d.department_name
HAVING AVG(e.salary) > ?;

-- 4. Employees earning more than the overall average.
SELECT employee_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- 5. Count employees in each department, including empty departments.
SELECT d.department_name, COUNT(e.employee_id) AS employee_count
FROM departments AS d
LEFT JOIN employees AS e ON e.department_id = d.department_id
GROUP BY d.department_id, d.department_name;

-- 6. Safe parameterized update example (bind values in application code).
UPDATE employees
SET salary = ?
WHERE employee_id = ?;
