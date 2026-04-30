from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, field_validator, model_validator


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    discount_price: Optional[Decimal] = None
    stock: int = 0
    is_featured: bool = False
    image_url: Optional[str] = None
    image_public_id: Optional[str] = None
    product_type: str = "PLANT"
    target_pest: Optional[str] = None
    usage_instructions: Optional[str] = None
    phi: Optional[str] = None

    @field_validator("stock")
    @classmethod
    def stock_must_be_positive(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Stock must be greater than or equal to 0")
        return v

    @model_validator(mode="after")
    def validate_discount_price(self) -> "ProductCreate":
        if self.discount_price is not None and self.discount_price >= self.price:
            raise ValueError("Discount price must be less than price")
        return self


class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    discount_price: Optional[Decimal] = None
    stock: Optional[int] = None
    is_featured: Optional[bool] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    product_type: Optional[str] = None
    target_pest: Optional[str] = None
    usage_instructions: Optional[str] = None
    phi: Optional[str] = None

    @field_validator("stock")
    @classmethod
    def stock_must_be_positive(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 0:
            raise ValueError("Stock must be greater than or equal to 0")
        return v

    @model_validator(mode="after")
    def validate_discount_price(self) -> "ProductUpdate":
        price = self.price
        discount_price = self.discount_price
        
        # This validation is tricky during partial updates. 
        # In a real app, you might need to fetch the current price from DB if not provided.
        # For now, we validate only if both are provided in the update.
        if price is not None and discount_price is not None:
            if discount_price >= price:
                raise ValueError("Discount price must be less than price")
        return self


class ProductResponse(BaseModel):
    id: int
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    price: Decimal
    discount_price: Optional[Decimal] = None
    image_url: Optional[str] = None
    category_id: int
    category: Optional[CategoryResponse] = None
    stock: int
    is_featured: bool
    is_active: bool
    product_type: str
    target_pest: Optional[str] = None
    usage_instructions: Optional[str] = None
    phi: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    page_size: int
