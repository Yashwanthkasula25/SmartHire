from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ApplicationCreate(BaseModel):
    job_id: int
    resume_url: str


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    resume_url: str | None
    resume_score: int | None
    voice_score: int | None
    final_score: int | None
    status: str
    interview_completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateApplicationStatus(BaseModel):
    status: str
