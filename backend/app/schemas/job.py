from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class JobCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="The job title")
    description: str = Field(..., min_length=20, description="Detailed job description and requirements")

class JobResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True