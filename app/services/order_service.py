from decimal import Decimal
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func

from app.models.cart import Cart
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate


def place_order(db: Session, user: User, payload: OrderCreate) -> Order:
    cart_items = (
        db.query(Cart)
        .options(selectinload(Cart.product))
        .filter(Cart.user_id == user.id)
        .all()
    )
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    if payload.payment_method not in ("cash_on_delivery", "online_payment"):
        raise HTTPException(status_code=400, detail="Invalid payment_method")

    total = Decimal("0.00")
    for item in cart_items:
        if not item.product or not item.product.is_active:
            raise HTTPException(status_code=400, detail="Cart contains invalid product")
        if item.product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock for one or more items")
        total += Decimal(str(item.product.price)) * item.quantity

    order = Order(
        user_id=user.id,
        total_amount=total.quantize(Decimal("0.01")),
        payment_method=payload.payment_method,
        shipping_address=payload.shipping_address,
        notes=payload.notes,
        payment_status="paid" if payload.payment_method == "online_payment" else "unpaid",
    )

    try:
        db.add(order)
        db.flush()

        for cart_item in cart_items:
            unit_price = Decimal(str(cart_item.product.price)).quantize(Decimal("0.01"))
            subtotal = (unit_price * cart_item.quantity).quantize(Decimal("0.01"))
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    item_name=cart_item.product.name,
                    unit_price=unit_price,
                    quantity=cart_item.quantity,
                    subtotal=subtotal,
                )
            )
            cart_item.product.stock_quantity -= cart_item.quantity

        db.query(Cart).filter(Cart.user_id == user.id).delete()
        db.commit()
    except Exception:
        db.rollback()
        raise

    return (
        db.query(Order)
        .options(selectinload(Order.items))
        .filter(Order.id == order.id)
        .first()
    )


def get_my_orders(db: Session, user: User) -> list[Order]:
    return (
        db.query(Order)
        .options(selectinload(Order.items))
        .filter(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .all()
    )


def get_order_by_id(db: Session, user: User, order_id: int) -> Order:
    order = (
        db.query(Order)
        .options(selectinload(Order.items))
        .filter(Order.id == order_id, Order.user_id == user.id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def admin_dashboard_stats(db: Session) -> dict:
    total_orders = db.query(Order).count()
    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0
    total_users = db.query(User).filter(User.role == "customer").count()
    total_products = db.query(Product).filter(Product.is_active == True).count()  # noqa: E712
    pending_orders = db.query(Order).filter(Order.status == "pending").count()
    return {
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "total_users": total_users,
        "total_products": total_products,
        "pending_orders": pending_orders,
    }


def admin_all_orders(
    db: Session, status: Optional[str], page: int, page_size: int
) -> list[Order]:
    query = db.query(Order).options(selectinload(Order.items))
    if status:
        query = query.filter(Order.status == status)
    return (
        query.order_by(Order.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )


def admin_update_order_status(db: Session, order_id: int, status: str) -> None:
    valid_statuses = {"pending", "processing", "shipped", "delivered", "cancelled"}
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()

