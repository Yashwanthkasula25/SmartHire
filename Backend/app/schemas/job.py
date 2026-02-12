from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class JobCreate(BaseModel):
    title: str
    role: Optional[str] = None
    description: Optional[str] = None
    package: Optional[str] = None
    location: Optional[str] = None
    mode: Optional[str] = None
    experience_required: Optional[int] = None

    resume_min_score: Optional[int] = None
    interview_min_score: Optional[int] = None


class JobResponse(BaseModel):
    id: int
    title: str
    role: Optional[str] = None
    description: Optional[str] = None
    package: Optional[str] = None
    location: Optional[str] = None
    mode: Optional[str] = None
    experience_required: Optional[int] = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
