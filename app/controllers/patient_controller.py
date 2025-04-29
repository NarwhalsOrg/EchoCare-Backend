from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from app.utils.exceptions import DatabaseError, NotFoundError
from typing import List

async def create_patient(db: AsyncSession, patient: PatientCreate) -> Patient:
    """
    Create a new patient in the database
    """
    try:
        db_patient = Patient(
            first_name=patient.first_name,
            last_name=patient.last_name,
            date_of_birth=patient.date_of_birth,
            gender=patient.gender,
            contact_number=patient.contact_number,
            email=patient.email,
            address=patient.address,
            medical_history=patient.medical_history,
            doctor_id=patient.doctor_id
        )
        db.add(db_patient)
        await db.commit()
        await db.refresh(db_patient)
        return db_patient
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))

async def get_patient_by_id(db: AsyncSession, patient_id: int) -> Patient:
    """
    Get a patient by ID
    """
    result = await db.execute(select(Patient).filter(Patient.id == patient_id))
    patient = result.scalars().first()
    if not patient:
        raise NotFoundError("Patient", patient_id)
    return patient

async def get_patients_by_doctor(db: AsyncSession, doctor_id: int, skip: int = 0, limit: int = 100) -> List[Patient]:
    """
    Get all patients for a specific doctor
    """
    result = await db.execute(
        select(Patient)
        .filter(Patient.doctor_id == doctor_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_all_patients(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Patient]:
    """
    Get all patients with pagination
    """
    result = await db.execute(select(Patient).offset(skip).limit(limit))
    return result.scalars().all()

async def update_patient(db: AsyncSession, patient_id: int, patient_update: PatientUpdate) -> Patient:
    """
    Update a patient's information
    """
    try:
        db_patient = await get_patient_by_id(db, patient_id)
        
        update_data = patient_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_patient, key, value)
            
        await db.commit()
        await db.refresh(db_patient)
        return db_patient
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))

async def delete_patient(db: AsyncSession, patient_id: int) -> bool:
    """
    Delete a patient
    """
    try:
        db_patient = await get_patient_by_id(db, patient_id)
        await db.delete(db_patient)
        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))

async def update_patient_avatar(db: AsyncSession, patient_id: int, avatar_url: str) -> Patient:
    """
    Update a patient's avatar URL
    """
    try:
        db_patient = await get_patient_by_id(db, patient_id)
        db_patient.avatar_url = avatar_url
        await db.commit()
        await db.refresh(db_patient)
        return db_patient
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))