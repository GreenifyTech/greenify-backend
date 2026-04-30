from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime
    is_for_admin: bool

    class Config:
        from_attributes = True

class NotificationCreate(BaseModel):
    title: str
    message: str
    user_id: Optional[int] = None
    is_for_admin: bool = False
