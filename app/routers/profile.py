from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from pydantic import BaseModel
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileResponse, UserProfileUpdate
from app.services.cloudinary_service import upload_image

router = APIRouter(prefix="/api/profile", tags=["Profile"])


class ProfileImageUpload(BaseModel):
    image_url: str


def _get_or_create_profile(db: Session, user: User) -> UserProfile:
    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    except ProgrammingError:
        raise HTTPException(
            status_code=503,
            detail="user_profiles table is missing. Run user_profiles.sql in MySQL.",
        )
    if profile:
        return profile

    profile = UserProfile(
        user_id=user.id,
        full_name=user.full_name,
        phone=user.phone or "",
        address=user.address or "",
        is_profile_completed=False,
    )
    try:
        db.add(profile)
        db.commit()
        db.refresh(profile)
    except ProgrammingError:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="user_profiles table is missing. Run user_profiles.sql in MySQL.",
        )
    return profile


@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return _get_or_create_profile(db=db, user=user)


@router.put("/me", response_model=UserProfileResponse)
def update_my_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = _get_or_create_profile(db=db, user=user)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
        # Sync full_name back to User model if it's updated
        if field == "full_name":
            user.full_name = value

    required_filled = all(
        [
            (profile.full_name or "").strip(),
            (profile.phone or "").strip(),
            (profile.address or "").strip(),
        ]
    )
    profile.is_profile_completed = bool(required_filled)

    db.commit()
    db.refresh(profile)
    return profile


@router.post("/me/image/", response_model=UserProfileResponse)
def upload_my_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        upload_result = upload_image(file)
        image_url = upload_result.get("url")
        
        profile = _get_or_create_profile(db=db, user=user)
        profile.profile_image = image_url
        db.commit()
        db.refresh(profile)
        return profile
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")


@router.post("/upload-image", response_model=UserProfileResponse)
def upload_profile_image(
    payload: ProfileImageUpload,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not payload.image_url.strip():
        raise HTTPException(status_code=400, detail="image_url is required")

    profile = _get_or_create_profile(db=db, user=user)
    profile.profile_image = payload.image_url.strip()
    db.commit()
    db.refresh(profile)
    return profile
