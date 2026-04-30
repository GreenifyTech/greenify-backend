from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.plant_knowledge import DiseaseInfo
from app.models.product import Product
from app.schemas.diagnosis import DiagnosisRequest, DiagnosisResponse, DiseaseResponse

from app.models.analytics_logs import DiagnosticLog

router = APIRouter(prefix="/api/diagnosis", tags=["Diagnosis"])

@router.post("/search", response_model=DiagnosisResponse)
def search_diagnosis(payload: DiagnosisRequest, db: Session = Depends(get_db)):
    query = payload.query.lower()
    
    # 1. Search for a matching disease based on symptoms
    disease = db.query(DiseaseInfo).filter(
        or_(
            DiseaseInfo.symptoms.ilike(f"%{query}%"),
            DiseaseInfo.name.ilike(f"%{query}%")
        )
    ).first()
    
    # Log the request for BI
    new_log = DiagnosticLog(
        symptoms=query,
        detected_disease=disease.name if disease else "Not Found"
    )
    db.add(new_log)
    db.commit()
    
    if not disease:
        raise HTTPException(status_code=404, detail="Could not identify the issue. Please try describing the symptoms differently.")
    
    # 2. Cross-reference with medicines
    # We use the disease.treatment_keywords to search for target_pest in products
    medicines = []
    if disease.treatment_keywords:
        keywords = [k.strip() for k in disease.treatment_keywords.split(",")]
        # Create a dynamic OR filter for all keywords
        medicine_query = db.query(Product).filter(Product.product_type == "MEDICINE")
        filters = [Product.target_pest.ilike(f"%{k}%") for k in keywords]
        medicines = medicine_query.filter(or_(*filters)).all()
    
    return {
        "diagnosis": disease,
        "recommended_products": medicines,
        "explanation": f"Based on the symptoms '{query}', we identified '{disease.name}'. This is often caused by {disease.cause or 'environmental factors'}."
    }
