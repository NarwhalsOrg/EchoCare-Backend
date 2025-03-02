from sqlmodel import Field, SQLModel
from typing import Optional, List
from datetime import datetime
import uuid

class MedicationBase(SQLModel):
    name: str
    dosage: str
    frequency: str
    duration: str
    instructions: Optional[str] = None

class PrescriptionBase(SQLModel):
    patient_id: str = Field(foreign_key="patients.id")
    doctor_id: str = Field(foreign_key="users.id")
    diagnosis: str
    notes: Optional[str] = None
    file_url: Optional[str] = None
    medications: List[MedicationBase]

class Prescription(SQLModel, table=True):
    __tablename__ = "prescriptions"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    patient_id: str = Field(foreign_key="patients.id")
    doctor_id: str = Field(foreign_key="users.id")
    diagnosis: str
    notes: Optional[str] = None
    file_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Medication(SQLModel, table=True):
    __tablename__ = "medications"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    prescription_id: str = Field(foreign_key="prescriptions.id")
    name: str
    dosage: str
    frequency: str
    duration: str
    instructions: Optional[str] = None

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionUpdate(SQLModel):
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    file_url: Optional[str] = None
    medications: Optional[List[MedicationBase]] = None

class PrescriptionWithMedications(PrescriptionBase):
    id: str
    created_at: datetime
    updated_at: datetime