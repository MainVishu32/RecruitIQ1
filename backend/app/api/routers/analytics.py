from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db
from app.db.models import Job, Candidate, AnalysisResult, User
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/")
def get_platform_metrics(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Aggregates global metrics for the recruiter dashboard.
    """
    total_jobs = db.query(func.count(Job.id)).filter(Job.user_id == current_user.id).scalar()
    total_candidates = db.query(func.count(Candidate.id)).scalar()
    
    # Calculate average platform-wide AI confidence score
    avg_score = db.query(func.avg(AnalysisResult.overall_score)).join(Job).filter(Job.user_id == current_user.id).scalar()
    
    # Count total analyses performed
    total_analyses = db.query(func.count(AnalysisResult.id)).join(Job).filter(Job.user_id == current_user.id).scalar()

    return {
        "total_jobs_posted": total_jobs or 0,
        "total_candidates_pooled": total_candidates or 0,
        "average_match_score": round(avg_score or 0, 2),
        "total_computations_run": total_analyses or 0
    }