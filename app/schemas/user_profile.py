from datetime import datetime, date
from typing import Optional, Literal

from pydantic import BaseModel


class UserProfileCreate(BaseModel):
    full_name: str
    phone: str = ""
    address: str = ""
    city: Optional[str] = None
    postal_code: Optional[str] = None
    profile_image: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Literal["male", "female"]] = None
    preferred_language: str = "en"
    default_address_id: Optional[int] = None
    is_profile_completed: bool = False


class UserProfileUpdate(BaseModel):
    full_name: str
    phone: str
    address: str
    city: Optional[str] = None
    postal_code: Optional[str] = None
    profile_image: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Literal["male", "female"]] = None
    preferred_language: str = "en"
    default_address_id: Optional[int] = None


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone: str
    address: str
    city: Optional[str]
    postal_code: Optional[str]
    profile_image: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[str]
    preferred_language: str
    default_address_id: Optional[int]
    is_profile_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

