"""Fetch scores from the Student Scores API, calculate average, and plot a bar chart.

Start the API first:
    uvicorn assignment-1.student_score_api:app --host 0.0.0.0 --port 8000
Then run:
    python assignment-1/student_score_analysis.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Save a chart in headless cloud environments.
import matplotlib.pyplot as plt
import requests

API_URL = "http://127.0.0.1:8000/students"
OUTPUT_PATH = Path(__file__).with_name("student_scores.png")


def main():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    students = response.json().get("students", [])

    if not students:
        raise ValueError("The API returned no student records.")

    names = [student["name"] for student in students]
    scores = [float(student["score"]) for student in students]
    average = sum(scores) / len(scores)

    print(f"Number of students: {len(students)}")
    print(f"Average score: {average:.2f}")

    plt.figure(figsize=(8, 5))
    bars = plt.bar(names, scores)
    plt.title("Student Test Scores")
    plt.xlabel("Student")
    plt.ylabel("Score")
    plt.ylim(0, 100)
    plt.axhline(average, linestyle="--", label=f"Average: {average:.1f}")
    plt.bar_label(bars, padding=3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=150)
    print(f"Chart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
