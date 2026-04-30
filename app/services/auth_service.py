from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user import TokenResponse, UserLogin, UserRegister, UserResponse


def register_user(db: Session, payload: UserRegister) -> User:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    user = User(
        full_name=payload.full_name,
        email=str(payload.email),
        password=hash_password(payload.password),
        phone=payload.phone,
        address=payload.address,
        role="customer",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    try:
        profile = UserProfile(
            user_id=user.id,
            full_name=payload.full_name,
            phone=payload.phone or "",
            address=payload.address or "",
            is_profile_completed=False,
        )
        db.add(profile)
        db.commit()
    except Exception as e:
        print(f"PROFILE CREATION FAILED: {e}")
        db.rollback()
    return user


def login_user(db: Session, payload: UserLogin) -> TokenResponse:
    return login_user_with_credentials(
        db=db,
        email=str(payload.email),
        password=payload.password,
    )


def login_user_with_credentials(db: Session, email: str, password: str) -> TokenResponse:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    token = create_access_token(data={"sub": str(user.id), "role": user.role})

    # Override user response with profile data if available
    user_data = {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "address": user.address,
        "role": user.role,
        "is_admin": user.is_admin,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "profile_image": None
    }
    
    if user.profile:
        user_data["full_name"] = user.profile.full_name or user_data["full_name"]
        user_data["phone"] = user.profile.phone or user_data["phone"]
        user_data["address"] = user.profile.address or user_data["address"]
        user_data["profile_image"] = user.profile.profile_image

    user_response = UserResponse(**user_data)

    return TokenResponse(access_token=token, token_type="bearer", user=user_response)


def toggle_user_active(db: Session, user_id: int) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = not user.is_active
    db.commit()
    return {"message": f"User {'activated' if user.is_active else 'deactivated'}"}


def list_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def ban_user(db: Session, user_id: int) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"message": "User banned successfully"}


def make_user_admin(db: Session, user_id: int) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = True
    user.role = "admin"
    db.commit()
    return {"message": "User is now an admin"}
