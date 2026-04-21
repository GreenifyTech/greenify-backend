from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database import Base


class AIConsultation(Base):
    __tablename__ = "ai_consultations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    symptoms = Column(Text, nullable=False)
    possible_disease = Column(Text, nullable=False)
    cause = Column(Text, nullable=False)
    treatment = Column(Text, nullable=False)
    confidence = Column(Enum("high", "medium", "low"), nullable=False)
    disclaimer = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship("User")

