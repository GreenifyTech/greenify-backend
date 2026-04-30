from pydantic import BaseModel
from typing import List, Optional
from app.schemas.product import ProductResponse

class DiagnosisRequest(BaseModel):
    query: str # e.g. "yellow spots on leaves"

class DiseaseResponse(BaseModel):
    id: int
    name: str
    symptoms: str
    cause: Optional[str] = None
    description: Optional[str] = None

class DiagnosisResponse(BaseModel):
    diagnosis: DiseaseResponse
    recommended_products: List[ProductResponse]
    explanation: str
