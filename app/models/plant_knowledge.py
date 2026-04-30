from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import text
from app.database import Base

class PlantKnowledge(Base):
    __tablename__ = "plant_knowledge"

    id = Column(Integer, primary_key=True)
    common_name = Column(String(100), nullable=False)
    scientific_name = Column(String(100), nullable=True)
    classification = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    medical_benefits = Column(Text, nullable=True)
    care_tips = Column(Text, nullable=True) # JSON or formatted string
    symptoms_handled = Column(Text, nullable=True) # comma separated or keywords
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

class DiseaseInfo(Base):
    __tablename__ = "diseases"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    symptoms = Column(Text, nullable=False)
    cause = Column(String(200), nullable=True)
    treatment_keywords = Column(String(200), nullable=True) # To link with medicine target_pest
    description = Column(Text, nullable=True)
