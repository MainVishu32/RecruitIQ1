from app.db.models import Candidate, Job
from typing import Dict, List, Any
import re

def generate_xai_report(candidate: Candidate, job: Job, overall_score: float) -> Dict[str, Any]:
    """
    Analyzes terms between Candidate Skills and Job Descriptions to map:
    - Matched Skills
    - Missing Skills
    - Transferable Skills
    Generates a localized natural-language evaluation report.
    """
    job_desc_lower = job.description.lower()
    candidate_skills = [s.strip() for s in (candidate.skills or "").split(",") if s.strip()]
    
    matched = []
    missing = []
    transferable = []

    # Basic skill categorization logic
    for skill in candidate_skills:
        skill_lower = skill.lower()
        if skill_lower in job_desc_lower:
            matched.append(skill)
        else:
            # Simple heuristic for transferable skills (cross-domain tools)
            if any(tech in skill_lower for tech in ["python", "sql", "aws", "docker", "git", "linux"]):
                transferable.append(skill)

    # Heuristic parsing to find common JD keywords missing in candidate profile
    common_keywords = ["react", "next.js", "fastapi", "kubernetes", "typescript", "tailwind", "redis", "postgres", "nosql", "machine learning"]
    for kw in common_keywords:
        if kw in job_desc_lower and kw not in [s.lower() for s in candidate_skills]:
            missing.append(kw.capitalize())

    # Compile natural language explanation template
    if overall_score >= 80:
        summary_text = (
            f"{candidate.full_name} is an exceptional match for the {job.title} position, scoring {overall_score}%. "
            f"Their background explicitly aligns with key requirements, showing strong proficiency in {', '.join(matched[:3]) if matched else 'core domains'}. "
            f"Furthermore, their experience of {candidate.experience_years} years brings substantial operational stability."
        )
    elif overall_score >= 50:
        summary_text = (
            f"{candidate.full_name} demonstrates solid foundational alignment for the role, scoring {overall_score}%. "
            f"While they carry relevant expertise in {', '.join(matched[:2]) if matched else 'some domains'}, bridging gaps in "
            f"{', '.join(missing[:2]) if missing else 'specialized skills'} would maximize position alignment."
        )
    else:
        summary_text = (
            f"{candidate.full_name} shows minimal contextual overlap for this specific opening. "
            f"Their profile highlights skills like {', '.join(candidate_skills[:2]) if candidate_skills else 'general experience'}, "
            f"which do not tightly cross-reference with the primary tech stack outlines in the current job blueprint."
        )

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "transferable_skills": transferable,
        "xai_report": summary_text
    }