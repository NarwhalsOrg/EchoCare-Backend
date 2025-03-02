from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
import uuid

class AppointmentBase(SQLModel):
    patient_id: str = Field(foreign_key="patients.id")
    doctor_id: str = Field(foreign_key="users.id")
    appointment_date: datetime
    reason: str
    status: str = "scheduled"  # scheduled, completed, cancelled
    notes: Optional[str] = None

class Appointment(AppointmentBase, table=True):
    __tablename__ = "appointments"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(SQLModel):
    appointment_date: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: str
    created_at: datetime
    updated_at: datetime