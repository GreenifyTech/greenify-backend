from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.database import get_db
from app.schemas.product import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.product_service import create_category, list_categories, update_category


@router.get("/", response_model=list[CategoryResponse])
def categories_list(db: Session = Depends(get_db)):
    return list_categories(db=db)


@router.post("/", response_model=CategoryResponse, status_code=201)
def categories_create(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
):
    return create_category(db=db, payload=payload)


@router.put("/{category_id}", response_model=CategoryResponse)
def categories_update(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
):
    return update_category(db=db, category_id=category_id, payload=payload)

