from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.analytics_logs import DiagnosticLog
from app.schemas.ai import DiagnoseRequest, DiagnoseResponse
from app.services.ai_service import diagnose_plant

router = APIRouter(prefix="/api/ai", tags=["AI Plant Doctor"])


@router.post("/diagnose", response_model=DiagnoseResponse)
def diagnose(payload: DiagnoseRequest, db: Session = Depends(get_db)):
    result = diagnose_plant(payload.symptoms)
    
    # Log the request for analytics
    new_log = DiagnosticLog(
        symptoms=payload.symptoms,
        detected_disease=result.get("possible_disease"),
        # We could also get user_id from token if we wanted to make it authenticated
    )
    db.add(new_log)
    db.commit()
    
    return result

