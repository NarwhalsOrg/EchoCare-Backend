from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.PatientData import PatientData


class ChatRequest(BaseModel):
    session_id: str
    message: str
    patient_data: PatientData

class ChatMessage(BaseModel):
    sender: str  # 'user' or 'ai'
    message: str
    timestamp: Optional[str] = None

