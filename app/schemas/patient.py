from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    contact_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None

class PatientCreate(PatientBase):
    doctor_id: int

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None
    avatar_url: Optional[str] = None
    doctor_id: Optional[int] = None

class PatientInDB(PatientBase):
    id: int
    doctor_id: int
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PatientResponse(PatientInDB):
    pass