from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, OrderCreateResponse
from app.services.order_service import get_my_orders, get_order_by_id, place_order, upload_payment_proof

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/", response_model=OrderCreateResponse, status_code=201)
def orders_place(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    order = place_order(db=db, user=user, payload=payload)
    return {
        "order_id": order.id, 
        "total": order.total_amount,
        "payment_method": order.payment_method,
        "payment_status": order.payment_status,
        "payment_details": getattr(order, "payment_details", None)
    }

from enum import Enum
from typing import Optional
from fastapi import Query
from pydantic import BaseModel
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderResponse

class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class PaginatedOrderResponse(BaseModel):
    items: list[OrderResponse]
    total: int
    page: int
    page_size: int

@router.get("/me", response_model=PaginatedOrderResponse)
def orders_me(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    status: Optional[OrderStatus] = Query(None)
):
    base_query = db.query(Order).filter(Order.user_id == user.id)
    if status is not None:
        base_query = base_query.filter(Order.status == status.value)

    total = db.query(func.count(Order.id)).filter(Order.user_id == user.id)
    if status is not None:
        total = total.filter(Order.status == status.value)
    total_count = total.scalar() or 0

    items = (
        base_query
        .options(
            selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.category)
        )
        .order_by(Order.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PaginatedOrderResponse(
        items=items,
        total=total_count,
        page=page,
        page_size=page_size
    )


@router.get("/{order_id}", response_model=OrderResponse)
def orders_get(
    order_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return get_order_by_id(db=db, user=user, order_id=order_id)


@router.post("/{order_id}/upload-proof")
def orders_upload_proof(
    order_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    proof_url = upload_payment_proof(db=db, user=user, order_id=order_id, file=file)
    return {
        "message": "Proof uploaded successfully",
        "proof_url": proof_url
    }

