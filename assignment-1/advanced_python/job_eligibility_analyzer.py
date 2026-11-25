"""A small, testable job eligibility analyzer using Python data structures."""
from dataclasses import dataclass


@dataclass
class Candidate:
    name: str
    skills: set[str]
    experience_years: float


@dataclass
class Job:
    title: str
    required_skills: set[str]
    minimum_experience: float = 0


def analyze_match(candidate: Candidate, job: Job) -> dict:
    matched = candidate.skills & job.required_skills
    missing = job.required_skills - candidate.skills
    skill_score = (
        len(matched) / len(job.required_skills) * 100
        if job.required_skills else 100.0
    )
    experience_ok = candidate.experience_years >= job.minimum_experience

    return {
        "candidate": candidate.name,
        "job": job.title,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "skill_match_percent": round(skill_score, 2),
        "experience_requirement_met": experience_ok,
        "eligible_by_rules": experience_ok and not missing,
    }


def main():
    candidate = Candidate(
        name="Pavan",
        skills={"python", "sql", "html", "css", "javascript"},
        experience_years=0,
    )
    job = Job(
        title="Python Developer - Fresher",
        required_skills={"python", "sql", "html"},
        minimum_experience=0,
    )

    result = analyze_match(candidate, job)
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
