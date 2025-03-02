from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class PatientBase(SQLModel):
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: str
    phone_number: str
    address: Optional[str] = None
    email: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None

class Patient(PatientBase, table=True):
    __tablename__ = "patients"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(foreign_key="users.id")

class PatientCreate(PatientBase):
    pass

class PatientUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None

class PatientResponse(PatientBase):
    id: str
    created_at: datetime
    updated_at: datetime
    created_by: str