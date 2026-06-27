from pydantic import BaseModel
from typing import Optional

class CandidateResponse(BaseModel):
    id: int
    full_name: str
    email: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    skills: Optional[str]
    experience_years: Optional[float]
    education: Optional[str]
    projects: Optional[str]
    certifications: Optional[str]
    previous_companies: Optional[str]
    resume_summary: Optional[str]
    linkedin_url: Optional[str]
    github_url: Optional[str]
    portfolio_url: Optional[str]

    class Config:
        from_attributes = True