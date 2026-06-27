from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    jobs = relationship("Job", back_populates="recruiter")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    recruiter = relationship("User", back_populates="jobs")
    analysis_results = relationship("AnalysisResult", back_populates="job")

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, index=True)
    phone = Column(String)
    location = Column(String)
    skills = Column(Text) 
    experience_years = Column(Float, default=0.0)
    education = Column(Text)
    projects = Column(Text)
    certifications = Column(Text)
    previous_companies = Column(Text)
    resume_summary = Column(Text)
    linkedin_url = Column(String)
    github_url = Column(String)
    portfolio_url = Column(String)

    analysis_results = relationship("AnalysisResult", back_populates="candidate")

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    
    # Core AI Scoring
    overall_score = Column(Float, nullable=False)
    ai_confidence = Column(Float, nullable=False)
    
    # Explainable AI Fields (Stored as JSON arrays/objects)
    matched_skills = Column(JSON)
    missing_skills = Column(JSON)
    transferable_skills = Column(JSON)
    xai_report = Column(Text, nullable=False) 
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    job = relationship("Job", back_populates="analysis_results")
    candidate = relationship("Candidate", back_populates="analysis_results")