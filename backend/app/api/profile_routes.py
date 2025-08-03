from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import profile_schemas, profile_models, profile_utils
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.database import get_db

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/", response_model=profile_schemas.ProfileResponse)
def create_user_profile(profile: profile_schemas.ProfileCreate,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    existing_profile = db.query(profile_models.UserProfile).filter_by(user_id=current_user.id).first()
    if existing_profile:
        for key, value in profile.dict().items():
            setattr(existing_profile, key, value)
        targets = profile_utils.compute_daily_targets(profile.dict())
        for key, value in targets.items():
            setattr(existing_profile, key, value)
        db.commit()
        db.refresh(existing_profile)
        return existing_profile
    else:
        targets = profile_utils.compute_daily_targets(profile.dict())
        db_profile = profile_models.UserProfile(
            user_id=current_user.id,
            **profile.dict(),
            **targets
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "id": current_user.id}

@router.get("/my_profile", response_model=profile_schemas.ProfileResponse)
def get_my_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(profile_models.UserProfile).filter_by(user_id=current_user.id).first()
    if profile:
        return profile
    return {"detail": "Profile not found", "username": current_user.username, "id": current_user.id}
