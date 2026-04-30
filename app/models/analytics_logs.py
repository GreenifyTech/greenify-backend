from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import text
from app.database import Base

class SearchLog(Base):
    __tablename__ = "search_logs"

    id = Column(Integer, primary_key=True)
    query = Column(String(255), nullable=False)
    source = Column(String(50), nullable=False) # e.g., 'encyclopedia', 'shop'
    user_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

class DiagnosticLog(Base):
    __tablename__ = "diagnostic_logs"

    id = Column(Integer, primary_key=True)
    symptoms = Column(Text, nullable=False)
    detected_disease = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
