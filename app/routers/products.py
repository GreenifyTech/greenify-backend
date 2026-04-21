from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.database import get_db
from app.schemas.product import ProductCreate, ProductListResponse, ProductResponse, ProductUpdate
from app.services.product_service import (
    create_product,
    get_product,
    list_products,
    soft_delete_product,
    update_product,
)

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("/", response_model=ProductListResponse)
def products_list(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
):
    return list_products(
        db=db,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=page_size,
    )


@router.get("/{product_id}", response_model=ProductResponse)
def product_get(product_id: int, db: Session = Depends(get_db)):
    return get_product(db=db, product_id=product_id)


@router.post("/", response_model=ProductResponse, status_code=201)
def product_create(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
):
    return create_product(db=db, payload=payload)


@router.put("/{product_id}", response_model=ProductResponse)
def product_update(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
):
    return update_product(db=db, product_id=product_id, payload=payload)


@router.delete("/{product_id}", status_code=204)
def product_delete(
    product_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
):
    soft_delete_product(db=db, product_id=product_id)

