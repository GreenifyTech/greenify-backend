from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel


class BouquetCreate(BaseModel):
    name: str = "My Custom Bouquet"
    flower_types: List[str]
    colors: List[str]
    total_quantity: int = 1
    notes: Optional[str] = None
    # Shipping info for immediate order creation
    shipping_address: str
    phone: str
    payment_method: str = "cash_on_delivery"


class BouquetResponse(BaseModel):
    id: int
    name: str
    flower_types: str
    colors: str
    total_quantity: int
    estimated_price: Decimal
    notes: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

