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
    page_size: int = Query(12, ge=1, le=100),
    is_featured: Optional[bool] = Query(None),
    product_type: Optional[str] = Query(None),
    include_inactive: bool = Query(False),
):
    return list_products(
        db=db,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=page_size,
        is_featured=is_featured,
        product_type=product_type,
        include_inactive=include_inactive,
    )


@router.get("/{product_id}/", response_model=ProductResponse)
def product_get(product_id: int, db: Session = Depends(get_db)):
    return get_product(db=db, product_id=product_id)


@router.post("/", response_model=ProductResponse, status_code=201)
def product_create(
    category_id: int = Form(...),
    name: str = Form(...),
    price: Decimal = Form(...),
    discount_price: Optional[Decimal] = Form(None),
    description: Optional[str] = Form(None),
    stock: int = Form(0),
    is_featured: bool = Form(False),
    image_url: Optional[str] = Form(None),
    product_type: str = Form("PLANT"),
    target_pest: Optional[str] = Form(None),
    usage_instructions: Optional[str] = Form(None),
    phi: Optional[str] = Form(None),
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
        discount_price=discount_price,
        description=description,
        stock=stock,
        is_featured=is_featured,
        image_url=image_url,
        image_public_id=image_public_id if 'image_public_id' in locals() else None,
        product_type=product_type,
        target_pest=target_pest,
        usage_instructions=usage_instructions,
        phi=phi
    )
    return create_product(db=db, payload=payload)


@router.put("/{product_id}/", response_model=ProductResponse)
def product_update(
    product_id: int,
    name: Optional[str] = Form(None),
    price: Optional[Decimal] = Form(None),
    discount_price: Optional[Decimal] = Form(None),
    category_id: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    stock: Optional[int] = Form(None),
    is_featured: Optional[bool] = Form(None),
    image_url: Optional[str] = Form(None),
    product_type: Optional[str] = Form(None),
    target_pest: Optional[str] = Form(None),
    usage_instructions: Optional[str] = Form(None),
    phi: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
):
    # Verify product exists first
    get_product(db, product_id)
    
    image_url = None
    if file:
        try:
            uploaded_data = upload_image(file, is_admin=True)
            image_url = uploaded_data["url"]
        except (ValueError, RuntimeError) as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Construct update payload manually from Form fields
    update_data = {}
    if name is not None: update_data["name"] = name
    if price is not None: update_data["price"] = price
    if discount_price is not None: update_data["discount_price"] = discount_price
    if category_id is not None: update_data["category_id"] = category_id
    if description is not None: update_data["description"] = description
    if stock is not None: update_data["stock"] = stock
    if is_featured is not None: update_data["is_featured"] = is_featured
    if image_url is not None: update_data["image_url"] = image_url
    if product_type is not None: update_data["product_type"] = product_type
    if target_pest is not None: update_data["target_pest"] = target_pest
    if usage_instructions is not None: update_data["usage_instructions"] = usage_instructions
    if phi is not None: update_data["phi"] = phi

    payload = ProductUpdate(**update_data)
    return update_product(db=db, product_id=product_id, payload=payload)


@router.delete("/{product_id}/", status_code=204)
def product_delete(
    product_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
):
    soft_delete_product(db=db, product_id=product_id)
