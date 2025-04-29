from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.utils.exceptions import DatabaseError, NotFoundError
from typing import List
from datetime import datetime

async def create_appointment(db: AsyncSession, appointment: AppointmentCreate) -> Appointment:
    """
    Create a new appointment in the database
    """
    try:
        db_appointment = Appointment(
            patient_id=appointment.patient_id,
            doctor_id=appointment.doctor_id,
            appointment_date=appointment.appointment_date,
            reason=appointment.reason,
            notes=appointment.notes
        )
        db.add(db_appointment)
        await db.commit()
        await db.refresh(db_appointment)
        return db_appointment
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))

async def get_appointment_by_id(db: AsyncSession, appointment_id: int) -> Appointment:
    """
    Get an appointment by ID
    """
    result = await db.execute(select(Appointment).filter(Appointment.id == appointment_id))
    appointment = result.scalars().first()
    if not appointment:
        raise NotFoundError("Appointment", appointment_id)
    return appointment

async def get_appointments_by_doctor(db: AsyncSession, doctor_id: int, skip: int = 0, limit: int = 100) -> List[Appointment]:
    """
    Get all appointments for a specific doctor
    """
    result = await db.execute(
        select(Appointment)
        .filter(Appointment.doctor_id == doctor_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_appointments_by_patient(db: AsyncSession, patient_id: int, skip: int = 0, limit: int = 100) -> List[Appointment]:
    """
    Get all appointments for a specific patient
    """
    result = await db.execute(
        select(Appointment)
        .filter(Appointment.patient_id == patient_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_upcoming_appointments(db: AsyncSession, doctor_id: int, skip: int = 0, limit: int = 100) -> List[Appointment]:
    """
    Get upcoming appointments for a doctor
    """
    now = datetime.now()
    result = await db.execute(
        select(Appointment)
        .filter(Appointment.doctor_id == doctor_id)
        .filter(Appointment.appointment_date > now)
        .order_by(Appointment.appointment_date)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def update_appointment(db: AsyncSession, appointment_id: int, appointment_update: AppointmentUpdate) -> Appointment:
    """
    Update an appointment's information
    """
    try:
        db_appointment = await get_appointment_by_id(db, appointment_id)
        
        update_data = appointment_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_appointment, key, value)
            
        await db.commit()
        await db.refresh(db_appointment)
        return db_appointment
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))

async def delete_appointment(db: AsyncSession, appointment_id: int) -> bool:
    """
    Delete an appointment
    """
    try:
        db_appointment = await get_appointment_by_id(db, appointment_id)
        await db.delete(db_appointment)
        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))