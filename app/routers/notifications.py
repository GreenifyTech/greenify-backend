from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.notification import Notification
from app.schemas.notification import NotificationResponse

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])

@router.get("/", response_model=list[NotificationResponse])
def get_notifications(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = db.query(Notification)
    
    if user.role == "admin":
        # Admins see admin notifications and their own personal ones
        query = query.filter((Notification.is_for_admin == True) | (Notification.user_id == user.id))
    else:
        # Normal users see only their personal notifications
        query = query.filter(Notification.user_id == user.id)
        
    return query.order_by(Notification.created_at.desc()).limit(50).all()

@router.patch("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    # Check authorization
    if notif.is_for_admin and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    if not notif.is_for_admin and notif.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    notif.is_read = True
    db.commit()
    return {"message": "Notification marked as read"}
