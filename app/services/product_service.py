from typing import Optional

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.category import Category
from app.models.product import Product
from app.schemas.product import CategoryCreate, ProductCreate, ProductUpdate
from app.core.utils import slugify


def list_categories(db: Session) -> list[Category]:
    return db.query(Category).order_by(Category.name.asc()).all()


def create_category(db: Session, payload: CategoryCreate) -> Category:
    existing = db.query(Category).filter(Category.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    category = Category(name=payload.name, description=payload.description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def list_products(
    db: Session,
    search: Optional[str],
    category_id: Optional[int],
    min_price: Optional[float],
    max_price: Optional[float],
    page: int,
    page_size: int,
    is_featured: Optional[bool] = None,
    product_type: Optional[str] = None,
    include_inactive: bool = False,
) -> dict:
    query = db.query(Product).options(joinedload(Product.category))
    
    if not include_inactive:
        query = query.filter(Product.is_active == True)  # noqa: E712
    
    if product_type:
        query = query.filter(Product.product_type == product_type)

    if search:
        query = query.filter(
            or_(Product.name.ilike(f"%{search}%"), Product.description.ilike(f"%{search}%"))
        )
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if is_featured is not None:
        query = query.filter(Product.is_featured == is_featured)

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def get_product(db: Session, product_id: int) -> Product:
    product = (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.id == product_id, Product.is_active == True)  # noqa: E712
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def create_product(db: Session, payload: ProductCreate) -> Product:
    category = db.query(Category).filter(Category.id == payload.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")
    
    product_data = payload.model_dump()
    # Generate slug from name
    product_data["slug"] = slugify(product_data["name"])
    
    product = Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, payload: ProductUpdate) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    data = payload.model_dump(exclude_unset=True)
    
    if "category_id" in data:
        category = db.query(Category).filter(Category.id == data["category_id"]).first()
        if not category:
            raise HTTPException(status_code=400, detail="Invalid category_id")
            
    if "name" in data:
        data["slug"] = slugify(data["name"])
            
    for field, value in data.items():
        setattr(product, field, value)
        
    db.commit()
    db.refresh(product)
    return product


def soft_delete_product(db: Session, product_id: int) -> None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.is_active = False
    db.commit()
