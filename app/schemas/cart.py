from pydantic import BaseModel


class CartAddItem(BaseModel):
    product_id: int
    quantity: int = 1


class CartUpdateItem(BaseModel):
    quantity: int


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_image: str | None
    price: float
    quantity: int
    subtotal: float


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total: float
    count: int

