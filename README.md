# AccuKnox – AI Security Engineer Trainee Assignment

A fresher-level, runnable submission covering Python, REST APIs, SQLite, CSV processing,
data visualization, LLM/RAG concepts, and a document knowledge assistant.

## Important honesty note
This repository is a learning/demo implementation prepared for the assignment. Review it,
run it, and make sure you can explain every part before submitting. Update the self-assessment
and project description to reflect your actual work. Do not claim production deployment,
independent expertise, or results that you have not verified.

## Repository structure

```text
assignment-1/
  book_api_sqlite.py
  student_score_api.py
  student_score_analysis.py
  csv_to_sqlite.py
  advanced_python/
    job_eligibility_analyzer.py
  database/
    schema.sql
    queries.sql
    database_demo.py
  data/
    users.csv
assignment-2/
  responses.md
assignment-3/
  README.md
  app.py
  requirements.txt
  sample_documents/
    python_basics.txt
.github/workflows/
  python-tests.yml
requirements.txt
```

## Run online without installing Python locally

### Option A: GitHub Codespaces (recommended)
1. Create a **public or private** GitHub repository.
2. Upload the contents of this ZIP, preserving the folder structure.
3. Open the repository on GitHub.
4. Select **Code → Codespaces → Create codespace on main**.
5. In the Codespaces terminal, run:

```bash
python -m pip install -r requirements.txt
python assignment-1/book_api_sqlite.py --limit 10
```

Start the student-score API in its own terminal (the folder name contains a hyphen,
so run Uvicorn from inside that folder):
```bash
cd assignment-1
uvicorn student_score_api:app --host 0.0.0.0 --port 8000
```

In a **second terminal**, return to the repository root and run:
```bash
cd ..
python assignment-1/student_score_analysis.py
python assignment-1/csv_to_sqlite.py
python assignment-1/advanced_python/job_eligibility_analyzer.py
python assignment-1/database/database_demo.py
```

For the knowledge assistant:
```bash
streamlit run assignment-3/app.py --server.address 0.0.0.0
```
Codespaces will offer to open the forwarded Streamlit port (8501).

### Option B: GitHub Actions
A basic automated test workflow is included at `.github/workflows/python-tests.yml`.
It runs the unit tests on pushes and pull requests. Actions are for automated checks;
they are not a persistent interactive development environment.

## Assignment 1 notes
- `book_api_sqlite.py` uses the Open Library Search API and stores returned books in SQLite.
- `student_score_api.py` exposes a small REST API backed by sample student records.
- `student_score_analysis.py` calls that API, calculates averages, and saves a bar chart.
  Start the API first in one terminal, then run the analysis script in another.
- `csv_to_sqlite.py` imports `users.csv` using parameterized SQL and transactions.
- `database/` demonstrates relational schema design, constraints, joins, aggregation,
  indexes, and parameterized access.

## Assignment 2 notes
See `assignment-2/responses.md`. The self-rating is a conservative suggested draft.
Edit it so it truthfully reflects your ability to code independently.

## Assignment 3 notes
The document assistant is a small retrieval-augmented demo. It extracts text from uploaded
TXT/PDF files, retrieves relevant chunks using TF-IDF, and returns evidence snippets.
It does **not** generate answers with an LLM by default. This distinction is stated
intentionally. A real LLM can be connected later, with appropriate API-key handling.

## Security and engineering choices
- SQL values use placeholders rather than string concatenation.
- CSV rows are validated before insertion.
- API calls use timeouts and check HTTP status codes.
- Secrets should be stored in environment variables, never committed to Git.
- Uploaded files are processed in memory in the demo; production systems need file-size,
  type, malware, access-control, and retention controls.
