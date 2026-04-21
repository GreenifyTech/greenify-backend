from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartAddItem, CartUpdateItem


def get_cart(db: Session, user: User) -> dict:
    items = db.query(Cart).filter(Cart.user_id == user.id).all()
    result = []
    total = 0.0
    for item in items:
        price = float(item.product.price)
        subtotal = price * item.quantity
        total += subtotal
        result.append(
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product.name,
                "product_image": item.product.image_url,
                "price": price,
                "quantity": item.quantity,
                "subtotal": round(subtotal, 2),
            }
        )
    return {"items": result, "total": round(total, 2), "count": len(result)}


def add_item(db: Session, user: User, payload: CartAddItem) -> None:
    if payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    product = (
        db.query(Product)
        .filter(Product.id == payload.product_id, Product.is_active == True)  # noqa: E712
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock_quantity < payload.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    existing = (
        db.query(Cart)
        .filter(Cart.user_id == user.id, Cart.product_id == payload.product_id)
        .first()
    )
    if existing:
        if product.stock_quantity < existing.quantity + payload.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        existing.quantity += payload.quantity
    else:
        db.add(Cart(user_id=user.id, product_id=payload.product_id, quantity=payload.quantity))
    db.commit()


def update_item(db: Session, user: User, item_id: int, payload: CartUpdateItem) -> None:
    item = db.query(Cart).filter(Cart.id == item_id, Cart.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if payload.quantity <= 0:
        db.delete(item)
        db.commit()
        return

    product = (
        db.query(Product)
        .filter(Product.id == item.product_id, Product.is_active == True)  # noqa: E712
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock_quantity < payload.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    item.quantity = payload.quantity
    db.commit()


def remove_item(db: Session, user: User, item_id: int) -> None:
    item = db.query(Cart).filter(Cart.id == item_id, Cart.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()


def clear_cart(db: Session, user: User) -> None:
    db.query(Cart).filter(Cart.user_id == user.id).delete()
    db.commit()

