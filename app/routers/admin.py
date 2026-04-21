from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.database import get_db
from app.models.user import User
from app.schemas.order import OrderResponse
from app.schemas.user import UserResponse
from app.services.auth_service import list_customers, toggle_user_active
from app.services.order_service import (
    admin_all_orders,
    admin_dashboard_stats,
    admin_update_order_status,
)

router = APIRouter(prefix="/api/admin", tags=["Admin"])


class OrderStatusUpdate(BaseModel):
    status: str


@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return admin_dashboard_stats(db=db)


@router.get("/orders", response_model=list[OrderResponse])
def all_orders(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return admin_all_orders(db=db, status=status, page=page, page_size=page_size)


@router.put("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    admin_update_order_status(db=db, order_id=order_id, status=payload.status)
    return {"message": f"Order #{order_id} status updated to {payload.status}"}


@router.get("/users", response_model=list[UserResponse])
def all_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return list_customers(db=db)


@router.put("/users/{user_id}/toggle-active")
def admin_toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return toggle_user_active(db=db, user_id=user_id)
