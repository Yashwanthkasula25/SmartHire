from pydantic import BaseModel, ConfigDict
from datetime import datetime

class JobCreate(BaseModel):
    title: str
    role: str | None = None
    description: str | None = None
    package: str | None = None
    location: str | None = None
    mode: str | None = None
    experience_required: int | None = None

    resume_min_score: int | None = None
    interview_min_score: int | None = None



class JobResponse(BaseModel):
    id: int
    title: str
    role: str | None
    description: str | None
    package: str | None
    location: str | None
    mode: str | None
    experience_required: int | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
