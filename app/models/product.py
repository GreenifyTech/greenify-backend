from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
    )
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    discount_price = Column(Numeric(10, 2), nullable=True)
    stock = Column(
        Integer, nullable=False, server_default=text("0")
    )
    slug = Column(String(250), unique=True, index=True, nullable=True)
    is_featured = Column(
        Boolean, nullable=False, server_default=text("false")
    )
    image_url = Column(String(500), nullable=True)
    image_public_id = Column(String(200), nullable=True)
    is_active = Column(
        Boolean, nullable=False, server_default=text("true")
    )
    product_type = Column(String(50), nullable=False, server_default=text("'PLANT'"))
    target_pest = Column(String(200), nullable=True)
    usage_instructions = Column(Text, nullable=True)
    phi = Column(String(100), nullable=True)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")

    __table_args__ = (
        Index("idx_products_name", "name"),
        Index("idx_products_category", "category_id"),
        Index("idx_products_price", "price"),
        Index("idx_products_slug", "slug"),
    )
