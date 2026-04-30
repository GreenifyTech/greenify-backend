from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.database import get_db
from app.models.user import User
from app.schemas.order import OrderResponse
from app.schemas.user import UserResponse
from app.services.auth_service import (
    list_all_users,
    ban_user,
    make_user_admin,
    toggle_user_active,
)
from app.services.order_service import (
    admin_all_orders,
    admin_dashboard_stats,
    admin_get_pending_payments,
    admin_approve_payment,
    admin_reject_payment,
    admin_update_order_status,
    admin_update_payment_status,
    verify_payment,
)

router = APIRouter(prefix="/api/admin", tags=["Admin"])


class OrderStatusUpdate(BaseModel):
    status: str


class PaymentStatusUpdate(BaseModel):
    payment_status: str


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


@router.get("/payments/pending", response_model=list[OrderResponse])
def pending_payments(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return admin_get_pending_payments(db=db)


@router.patch("/orders/{order_id}/approve-payment")
def approve_payment(
    order_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    admin_approve_payment(db=db, order_id=order_id)
    return {"message": f"Payment for order #{order_id} approved"}


@router.patch("/orders/{order_id}/reject-payment")
def reject_payment(
    order_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    admin_reject_payment(db=db, order_id=order_id)
    return {"message": f"Payment for order #{order_id} rejected"}


@router.put("/orders/{order_id}/status")
@router.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    admin_update_order_status(db=db, order_id=order_id, status=payload.status)
    return {"message": f"Order #{order_id} status updated to {payload.status}"}


@router.patch("/orders/{order_id}/payment")
def update_payment_status(
    order_id: int,
    payload: PaymentStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    admin_update_payment_status(db=db, order_id=order_id, payment_status=payload.payment_status)
    return {"message": f"Order #{order_id} payment status updated to {payload.payment_status}"}


@router.put("/orders/{order_id}/verify-payment")
def admin_verify_payment(
    order_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    verify_payment(db=db, order_id=order_id)
    return {"message": f"Payment for order #{order_id} verified successfully"}


@router.get("/users", response_model=list[UserResponse])
def all_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return list_all_users(db=db)


@router.patch("/users/{user_id}/ban")
def admin_ban_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return ban_user(db=db, user_id=user_id)


@router.patch("/users/{user_id}/make-admin")
def admin_make_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return make_user_admin(db=db, user_id=user_id)


@router.put("/users/{user_id}/toggle-active")
def admin_toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return toggle_user_active(db=db, user_id=user_id)
