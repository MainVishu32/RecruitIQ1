from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.db.models import Job, User
from app.schemas.job import JobCreate, JobResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.post("/upload", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def upload_job(
    job_in: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a new Job Description manually.
    """
    new_job = Job(
        title=job_in.title,
        description=job_in.description,
        user_id=current_user.id
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/", response_model=List[JobResponse])
def get_jobs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all jobs created by the authenticated recruiter.
    """
    jobs = db.query(Job).filter(Job.user_id == current_user.id).offset(skip).limit(limit).all()
    return jobs