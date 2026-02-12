from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from .job import JobResponse


class ApplicationCreate(BaseModel):
    job_id: int
    resume_url: str


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    resume_url: Optional[str] = None
    resume_score: Optional[int] = None
    voice_score: Optional[int] = None
    status: str
    interview_completed: bool
    created_at: datetime

    job: JobResponse

    model_config = ConfigDict(from_attributes=True)


class UpdateApplicationStatus(BaseModel):
    status: str
