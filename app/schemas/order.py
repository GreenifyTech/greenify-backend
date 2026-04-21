from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product_id: Optional[int] = None
    bouquet_id: Optional[int] = None
    quantity: int


class OrderCreate(BaseModel):
    payment_method: str = "cash_on_delivery"
    shipping_address: str
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: int
    item_name: str
    unit_price: Decimal
    quantity: int
    subtotal: Decimal

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    total_amount: Decimal
    status: str
    payment_method: str
    payment_status: str
    shipping_address: str
    notes: Optional[str]
    items: List[OrderItemResponse]
    created_at: datetime

    class Config:
        from_attributes = True

