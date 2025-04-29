from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PrescriptionBase(BaseModel):
    patient_id: int
    doctor_id: int
    diagnosis: str
    medications: str
    instructions: Optional[str] = None

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionUpdate(BaseModel):
    diagnosis: Optional[str] = None
    medications: Optional[str] = None
    instructions: Optional[str] = None
    file_url: Optional[str] = None

class PrescriptionInDB(PrescriptionBase):
    id: int
    file_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PrescriptionResponse(PrescriptionInDB):
    pass