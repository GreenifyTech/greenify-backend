from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.cart import CartAddItem, CartResponse, CartUpdateItem
from app.services.cart_service import (
    add_item,
    clear_cart,
    get_cart,
    remove_item,
    update_item,
)

router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.get("/", response_model=CartResponse)
def cart_get(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get all items in the user's cart."""
    return get_cart(db=db, user=user)


@router.post("/add", status_code=201)
def cart_add(
    payload: CartAddItem,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Add a product to the cart. If it already exists, quantity is increased."""
    add_item(db=db, user=user, payload=payload)
    return {"message": "Item added to cart"}


@router.put("/{item_id}")
def cart_update(
    item_id: int,
    payload: CartUpdateItem,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Update the quantity of an item in the cart."""
    update_item(db=db, user=user, item_id=item_id, payload=payload)
    return {"message": "Cart updated"}


@router.delete("/{item_id}", status_code=204)
def cart_remove(
    item_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Remove a specific item from the cart."""
    remove_item(db=db, user=user, item_id=item_id)


@router.delete("/", status_code=204)
def cart_clear(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Clear the entire cart."""
    clear_cart(db=db, user=user)
