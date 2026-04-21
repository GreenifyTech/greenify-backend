from pydantic import BaseModel


class DiagnoseRequest(BaseModel):
    symptoms: str


class DiagnoseResponse(BaseModel):
    possible_disease: str
    cause: str
    treatment: str
    confidence: str
    disclaimer: str

