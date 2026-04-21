from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)

    city = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    profile_image = Column(String(255), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    preferred_language = Column(String(10), nullable=True, server_default=text("'en'"))
    default_address_id = Column(Integer, nullable=True)

    is_profile_completed = Column(Boolean, nullable=True, server_default=text("false"))
    created_at = Column(DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    user = relationship("User", back_populates="profile")
