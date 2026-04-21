from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database import Base


class BouquetItem(Base):
    __tablename__ = "bouquet_items"

    id = Column(Integer, primary_key=True)
    bouquet_id = Column(Integer, ForeignKey("bouquets.id", ondelete="CASCADE"), nullable=False)
    flower_type = Column(String(100), nullable=False)
    color = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False, server_default=text("1"))
    unit_price = Column(Numeric(10, 2), nullable=False, server_default=text("0.00"))
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    __table_args__ = (
        UniqueConstraint("bouquet_id", "flower_type", "color", name="uq_bouquet_item_unique"),
    )

    bouquet = relationship("Bouquet")

