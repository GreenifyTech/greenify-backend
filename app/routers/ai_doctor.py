from fastapi import APIRouter

from app.schemas.ai import DiagnoseRequest, DiagnoseResponse
from app.services.ai_service import diagnose_plant

router = APIRouter(prefix="/api/ai", tags=["AI Plant Doctor"])


@router.post("/diagnose", response_model=DiagnoseResponse)
def diagnose(payload: DiagnoseRequest):
    return diagnose_plant(payload.symptoms)

