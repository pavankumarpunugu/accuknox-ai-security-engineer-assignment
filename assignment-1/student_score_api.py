"""Small REST API serving sample student scores.

Start with:
    uvicorn assignment-1.student_score_api:app --host 0.0.0.0 --port 8000
API docs: http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI

app = FastAPI(title="Student Scores API", version="1.0.0")

STUDENTS = [
    {"name": "Asha", "score": 88},
    {"name": "Rahul", "score": 76},
    {"name": "Meera", "score": 93},
    {"name": "Kiran", "score": 69},
    {"name": "Sanjay", "score": 81},
]


@app.get("/")
def home():
    return {"message": "Student Scores API", "students_endpoint": "/students"}


@app.get("/students")
def get_students():
    return {"count": len(STUDENTS), "students": STUDENTS}
