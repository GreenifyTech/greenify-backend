from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database import Base


class Bouquet(Base):
    __tablename__ = "bouquets"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(
        String(200),
        nullable=False,
        server_default=text("'My Custom Bouquet'"),
    )
    flower_types = Column(String(500), nullable=False)
    colors = Column(String(500), nullable=False)
    total_quantity = Column(Integer, nullable=False, server_default=text("1"))
    estimated_price = Column(
        Numeric(10, 2), nullable=False, server_default=text("0.00")
    )
    notes = Column(Text, nullable=True)
    status = Column(
        Enum("draft", "ordered"),
        nullable=False,
        server_default=text("'draft'"),
    )
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    user = relationship("User", back_populates="bouquets")
