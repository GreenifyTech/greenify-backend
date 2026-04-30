from pydantic import BaseModel


class DiagnoseRequest(BaseModel):
    symptoms: str


class DiagnoseResponse(BaseModel):
    possible_disease: str
    possible_disease_ar: str
    cause: str
    cause_ar: str
    treatment: str
    treatment_ar: str
    confidence: str
    disclaimer: str

