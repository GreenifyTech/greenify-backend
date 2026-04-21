from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(
        Enum("pending", "processing", "shipped", "delivered", "cancelled"),
        nullable=False,
        server_default=text("'pending'"),
    )
    payment_method = Column(
        Enum("cash_on_delivery", "online_payment"),
        nullable=False,
        server_default=text("'cash_on_delivery'"),
    )
    payment_status = Column(
        Enum("unpaid", "paid"),
        nullable=False,
        server_default=text("'unpaid'"),
    )
    shipping_address = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_orders_user", "user_id"),
        Index("idx_orders_status", "status"),
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True
    )
    bouquet_id = Column(
        Integer, ForeignKey("bouquets.id", ondelete="SET NULL"), nullable=True
    )
    item_name = Column(String(200), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, server_default=text("1"))
    subtotal = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
    bouquet = relationship("Bouquet")
