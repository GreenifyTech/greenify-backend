from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel
from app.schemas.product import ProductResponse


class OrderItemCreate(BaseModel):
    product_id: Optional[int] = None
    bouquet_id: Optional[int] = None
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    payment_method: str = "cash_on_delivery"
    transaction_id: Optional[str] = None
    shipping_address: Optional[str] = "Default Address"
    notes: Optional[str] = None


from app.schemas.bouquet import BouquetResponse

class OrderItemResponse(BaseModel):
    id: int
    item_name: str
    unit_price: Decimal
    quantity: int
    subtotal: Decimal
    product: Optional[ProductResponse] = None
    bouquet: Optional[BouquetResponse] = None

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    total_amount: Decimal
    status: str
    payment_method: str
    payment_status: str
    payment_proof: Optional[str] = None
    payment_verified: bool = False
    transaction_id: Optional[str] = None
    shipping_address: str
    notes: Optional[str]
    items: List[OrderItemResponse]
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreateResponse(BaseModel):
    order_id: int
    total: Decimal
    payment_method: str
    payment_status: str
    payment_details: Optional[dict] = None

