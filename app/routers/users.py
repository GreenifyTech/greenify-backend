from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRoleUpdate

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.patch("/{user_id}/role")
def update_user_role(
    user_id: int, 
    role_data: UserRoleUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_admin)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Map incoming role to database Enum values
    # MEMBER -> customer, ADMINISTRATOR -> admin
    # Or just use the lowercase if that's what's sent
    role_map = {
        "ADMIN": "admin",
        "ADMINISTRATOR": "admin",
        "MEMBER": "customer",
        "CUSTOMER": "customer"
    }
    
    new_role = role_map.get(role_data.role.upper(), role_data.role.lower())
    
    if new_role not in ["customer", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'customer' or 'admin'.")
        
    db_user.role = new_role
    # Also sync is_admin field for backward compatibility or if used elsewhere
    db_user.is_admin = (new_role == "admin")
    
    db.commit()
    return {"message": f"User role updated to {db_user.role}", "role": db_user.role}
