from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, HTTPException, status
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
from app.services.cloudinary_service import upload_image

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
    category_id: int = Form(...),
    name: str = Form(...),
    price: Decimal = Form(...),
    description: Optional[str] = Form(None),
    stock_quantity: int = Form(0),
    image_url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
):
    if file:
        try:
            uploaded_data = upload_image(file, is_admin=True)
            image_url = uploaded_data["url"]
            image_public_id = uploaded_data["public_id"]
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except RuntimeError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    payload = ProductCreate(
        category_id=category_id,
        name=name,
        price=price,
        description=description,
        stock_quantity=stock_quantity,
        image_url=image_url,
        image_public_id=image_public_id if 'image_public_id' in locals() else None
    )
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

