import json
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.bouquet import Bouquet
from app.models.order import Order, OrderItem
from app.models.user import User
from app.schemas.bouquet import BouquetCreate


FLOWER_PRICES: dict[str, float] = {
    "Rose": 15.0,
    "Lily": 12.0,
    "Tulip": 10.0,
    "Sunflower": 8.0,
    "Carnation": 7.0,
    "Orchid": 20.0,
}


def calculate_price(flower_types: list[str], quantity: int) -> Decimal:
    if not flower_types or quantity <= 0:
        return Decimal("0.00")
    base = sum(FLOWER_PRICES.get(f, 10.0) for f in flower_types)
    price = (base / len(flower_types)) * quantity
    return Decimal(str(round(price, 2))).quantize(Decimal("0.01"))




def create_bouquet(db: Session, user: User, payload: BouquetCreate) -> Bouquet:
    if payload.total_quantity <= 0:
        raise HTTPException(status_code=400, detail="total_quantity must be positive")
    price = calculate_price(payload.flower_types, payload.total_quantity)
    
    # 1. Create the Bouquet
    bouquet = Bouquet(
        user_id=user.id,
        name=payload.name,
        flower_types=json.dumps(payload.flower_types),
        colors=json.dumps(payload.colors),
        total_quantity=payload.total_quantity,
        estimated_price=price,
        notes=payload.notes,
        status="ordered" # Set to ordered immediately
    )
    db.add(bouquet)
    db.flush() # Get the bouquet ID

    # 2. Create the Order
    order = Order(
        user_id=user.id,
        total_amount=price,
        status="pending",
        payment_method=payload.payment_method,
        payment_status="unpaid",
        shipping_address=payload.shipping_address,
        notes=f"Custom Bouquet Order: {payload.name}. " + (payload.notes or "")
    )
    db.add(order)
    db.flush() # Get the order ID

    # 3. Create Order Item
    item = OrderItem(
        order_id=order.id,
        bouquet_id=bouquet.id,
        item_name=f"Custom Bouquet: {payload.name}",
        unit_price=price,
        quantity=1,
        subtotal=price
    )
    db.add(item)
    
    db.commit()
    db.refresh(bouquet)
    return bouquet


def list_my_bouquets(db: Session, user: User) -> list[Bouquet]:
    return db.query(Bouquet).filter(Bouquet.user_id == user.id).all()


def delete_bouquet(db: Session, user: User, bouquet_id: int) -> None:
    bouquet = (
        db.query(Bouquet).filter(Bouquet.id == bouquet_id, Bouquet.user_id == user.id).first()
    )
    if not bouquet:
        raise HTTPException(status_code=404, detail="Bouquet not found")
    db.delete(bouquet)
    db.commit()

