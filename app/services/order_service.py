from decimal import Decimal
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func

from app.models.cart_item import CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.models.notification import Notification
from app.schemas.order import OrderCreate
from app.services.cloudinary_service import upload_image


def place_order(db: Session, user: User, payload: OrderCreate) -> Order:
    if not payload.items:
        raise HTTPException(status_code=400, detail="Order items are required")

    total = Decimal("0.00")
    order_items_to_create = []

    for item_data in payload.items:
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product or not product.is_active:
            raise HTTPException(status_code=400, detail=f"Product {item_data.product_id} not found or inactive")
        
        if product.stock < item_data.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        
        unit_price = Decimal(str(product.discount_price or product.price)).quantize(Decimal("0.01"))
        subtotal = (unit_price * item_data.quantity).quantize(Decimal("0.01"))
        total += subtotal
        
        order_items_to_create.append({
            "product_id": product.id,
            "item_name": product.name,
            "unit_price": unit_price,
            "quantity": item_data.quantity,
            "subtotal": subtotal,
            "product_ref": product
        })

    valid_payment_methods = {"cash_on_delivery", "card", "instapay", "wallet"}
    if payload.payment_method not in valid_payment_methods:
        raise HTTPException(status_code=400, detail="Invalid payment method")

    # Payment simulation logic
    payment_status = "pending"
    payment_details = {}

    if payload.payment_method == "cash_on_delivery":
        payment_status = "pending"
    elif payload.payment_method == "card":
        payment_status = "paid"
        import uuid
        transaction_id = payload.transaction_id or f"sim_{uuid.uuid4().hex[:8]}"
        payment_details = {
            "transaction_id": transaction_id,
            "gateway": "Simulated Visa"
        }
    elif payload.payment_method == "instapay":
        payment_status = "pending"
        payment_details = {
            "receiver_name": "Greenify Store",
            "instapay_id": "greenify@instapay",
            "phone_number": "01012345678",
            "amount": float(total),
            "note": "Use InstaPay app to send money instantly"
        }
    elif payload.payment_method == "wallet":
        payment_status = "pending"
        payment_details = {
            "wallet_number": "01098765432",
            "amount": float(total)
        }

    order = Order(
        user_id=user.id,
        total_amount=total.quantize(Decimal("0.01")),
        payment_method=payload.payment_method,
        transaction_id=payload.transaction_id or (payment_details.get("transaction_id") if payload.payment_method == "card" else None),
        shipping_address=payload.shipping_address or "Default Address",
        notes=payload.notes,
        payment_status=payment_status,
    )

    # Attach transient field for response
    order.payment_details = payment_details

    try:
        db.add(order)
        db.flush()

        for item_info in order_items_to_create:
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=item_info["product_id"],
                    item_name=item_info["item_name"],
                    unit_price=item_info["unit_price"],
                    quantity=item_info["quantity"],
                    subtotal=item_info["subtotal"],
                )
            )
            # Deduct stock
            item_info["product_ref"].stock -= item_info["quantity"]

        # Optional: Clear cart if needed, but since items are passed directly, 
        # we might want to clear the cart table if it matches.
        # For now, let's just clear the cart for the user as per original logic.
        db.query(CartItem).filter(CartItem.user_id == user.id).delete()
        
        # Create notification for admin
        notif = Notification(
            user_id=None,
            is_for_admin=True,
            title="New Order Received",
            message=f"Order #{order.id} was placed by {user.full_name} for a total of {order.total_amount} EGP."
        )
        db.add(notif)
        
        db.commit()
    except Exception:
        db.rollback()
        raise

    return (
        db.query(Order)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
        .filter(Order.id == order.id)
        .first()
    )


def get_my_orders(db: Session, user: User) -> list[Order]:
    return (
        db.query(Order)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
        .filter(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .all()
    )


def get_order_by_id(db: Session, user: User, order_id: int) -> Order:
    order = (
        db.query(Order)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
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
    pending_payments = db.query(Order).filter(Order.payment_status == "pending", Order.payment_proof != None).count()  # noqa: E711
    return {
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "total_users": total_users,
        "total_products": total_products,
        "pending_orders": pending_orders,
        "pending_payments": pending_payments,
    }


def admin_all_orders(
    db: Session, status: Optional[str], page: int, page_size: int
) -> list[Order]:
    query = db.query(Order).options(selectinload(Order.items).selectinload(OrderItem.product))
    if status:
        query = query.filter(Order.status == status)
    return (
        query.order_by(Order.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )


def admin_update_order_status(db: Session, order_id: int, status: str) -> None:
    valid_statuses = {"pending", "confirmed", "processing", "shipped", "delivered", "cancelled"}
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()


def admin_update_payment_status(db: Session, order_id: int, payment_status: str) -> None:
    valid_payment_statuses = {"pending", "paid", "failed"}
    if payment_status not in valid_payment_statuses:
        raise HTTPException(status_code=400, detail="Invalid payment status")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.payment_status = payment_status
    db.commit()


def upload_payment_proof(db: Session, user: User, order_id: int, file) -> str:
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.payment_method != "instapay":
        raise HTTPException(status_code=400, detail="Payment proof only required for InstaPay orders")

    try:
        upload_result = upload_image(file)
        proof_url = upload_result.get("url")
        order.payment_proof = proof_url
        db.commit()
        return proof_url
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload proof: {str(e)}")


def verify_payment(db: Session, order_id: int) -> None:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.payment_verified = True
    order.payment_status = "paid"
    db.commit()


def admin_get_pending_payments(db: Session) -> list[Order]:
    return (
        db.query(Order)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
        .filter(Order.payment_status == "pending", Order.payment_proof != None)  # noqa: E711
        .order_by(Order.created_at.desc())
        .all()
    )


def admin_approve_payment(db: Session, order_id: int) -> None:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.payment_status = "paid"
    order.payment_verified = True
    order.status = "processing"
    db.commit()


def admin_reject_payment(db: Session, order_id: int) -> None:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.payment_status = "rejected"
    order.payment_verified = False
    db.commit()
