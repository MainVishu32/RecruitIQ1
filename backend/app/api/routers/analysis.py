from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from app.api.deps import get_db
from app.db.models import Job, AnalysisResult, Candidate
from app.ai.engine import ai_pipeline_engine
from app.ai.xai import generate_xai_report
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/analysis", tags=["AI Analysis Engine"])

@router.post("/run/{job_id}", status_code=status.HTTP_200_OK)
def run_job_analysis(
    job_id: int, 
    db: Session = Depends(get_db), 
    current_user: Any = Depends(get_current_user)
):
    """
    Triggers the dense vector match, handles cross-encoder reranking, 
    builds the XAI metadata report, and persists matches to the local database.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Target job definition not found.")
        
    try:
        # 1. Run local embedding discovery and reranking
        ranked_outputs = ai_pipeline_engine.run_matching_pipeline(db, job_id)
        
        # Clear existing analysis items for this job to avoid duplicates
        db.query(AnalysisResult).filter(AnalysisResult.job_id == job_id).delete()
        
        # 2. Iterate through calculations, build XAI reports, and save
        for output in ranked_outputs:
            cand = output["candidate"]
            score = output["overall_score"]
            conf = output["ai_confidence"]
            
            xai_data = generate_xai_report(cand, job, score)
            
            result_entry = AnalysisResult(
                job_id=job_id,
                candidate_id=cand.id,
                overall_score=score,
                ai_confidence=conf,
                matched_skills=xai_data["matched_skills"],
                missing_skills=xai_data["missing_skills"],
                transferable_skills=xai_data["transferable_skills"],
                xai_report=xai_data["xai_report"]
            )
            db.add(result_entry)
            
        db.commit()
        return {"status": "success", "candidates_analyzed": len(ranked_outputs)}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"AI Pipeline Engine Error: {str(e)}")

@router.get("/results/{job_id}")
def get_analysis_results(
    job_id: int, 
    db: Session = Depends(get_db), 
    current_user: Any = Depends(get_current_user)
):
    """Returns the fully computed semantic search roster for the recruiter UI."""
    results = db.query(AnalysisResult).filter(AnalysisResult.job_id == job_id).order_by(AnalysisResult.overall_score.desc()).all()
    
    payload = []
    for r in results:
        cand = db.query(Candidate).filter(Candidate.id == r.candidate_id).first()
        payload.append({
            "result_id": r.id,
            "overall_score": r.overall_score,
            "ai_confidence": r.ai_confidence,
            "matched_skills": r.matched_skills,
            "missing_skills": r.missing_skills,
            "transferable_skills": r.transferable_skills,
            "xai_report": r.xai_report,
            "candidate": {
                "id": cand.id,
                "full_name": cand.full_name,
                "email": cand.email,
                "skills": cand.skills,
                "experience_years": cand.experience_years,
                "resume_summary": cand.resume_summary
            }
        })
    return payload