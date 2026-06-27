import pandas as pd
import io
import math
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models import Candidate, User
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/candidates", tags=["Candidates"])

def safe_str(val):
    """Convert pandas NaN or empty values to None for the database."""
    if pd.isna(val) or val == "":
        return None
    return str(val).strip()

def safe_float(val):
    """Convert pandas NaN or strings to float, fallback to 0.0."""
    try:
        if pd.isna(val):
            return 0.0
        return float(val)
    except (ValueError, TypeError):
        return 0.0

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_candidates_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a CSV file containing candidate profiles.
    Expects specific column headers but gracefully handles missing data.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Required base column to ensure the CSV isn't entirely invalid
        if "Full_Name" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain a 'Full_Name' column.")
            
        candidates_added = 0
        
        # Batch insert for hackathon efficiency
        for _, row in df.iterrows():
            candidate = Candidate(
                full_name=safe_str(row.get("Full_Name")),
                email=safe_str(row.get("Email")),
                phone=safe_str(row.get("Phone")),
                location=safe_str(row.get("Location")),
                skills=safe_str(row.get("Skills")),
                experience_years=safe_float(row.get("Experience_Years")),
                education=safe_str(row.get("Education")),
                projects=safe_str(row.get("Projects")),
                certifications=safe_str(row.get("Certifications")),
                previous_companies=safe_str(row.get("Previous_Companies")),
                resume_summary=safe_str(row.get("Resume_Summary")),
                linkedin_url=safe_str(row.get("LinkedIn_URL")),
                github_url=safe_str(row.get("GitHub_URL")),
                portfolio_url=safe_str(row.get("Portfolio_URL")),
            )
            db.add(candidate)
            candidates_added += 1
            
        db.commit()
        
        return {
            "message": f"Successfully uploaded and parsed CSV.",
            "candidates_processed": candidates_added,
            "filename": file.filename
        }
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="The uploaded CSV file is empty.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")