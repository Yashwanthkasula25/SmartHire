from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..models.profile import Profile
from ..schemas.profile import ProfileCreate, ProfileResponse
from ..core.auth import get_current_user

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.post("/", response_model=ProfileResponse)
def create_or_update_profile(
    data: ProfileCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    if profile:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(profile, key, value)
    else:
        profile = Profile(user_id=user_id, **data.dict())
        db.add(profile)

    db.commit()
    db.refresh(profile)
    return profile


@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile
