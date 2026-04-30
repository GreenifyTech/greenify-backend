import json
from decimal import Decimal
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.user import User
from app.models.bouquet import Bouquet
from app.models.order import Order, OrderItem
from app.schemas.bouquet import BouquetCreate
from app.services.bouquet_service import create_bouquet

db = SessionLocal()
try:
    user = db.query(User).first()
    if not user:
        print("No user found")
    else:
        payload = BouquetCreate(
            name="Test",
            flower_types=["Rose"],
            colors=["Red"],
            total_quantity=1,
            shipping_address="Test Address",
            phone="123456",
            payment_method="cash_on_delivery"
        )
        res = create_bouquet(db, user, payload)
        print(f"Success: {res.id}")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
