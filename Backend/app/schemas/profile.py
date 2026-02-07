from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ProfileCreate(BaseModel):
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    experience_years: Optional[int] = None
    skills: Optional[str] = None



class ProfileResponse(ProfileCreate):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
