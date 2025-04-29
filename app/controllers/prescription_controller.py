from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.prescription import Prescription
from app.schemas.prescription import PrescriptionCreate, PrescriptionUpdate
from app.utils.exceptions import DatabaseError, NotFoundError
from typing import List

async def create_prescription(db: AsyncSession, prescription: PrescriptionCreate) -> Prescription:
    """
    Create a new prescription in the database
    """
    try:
        db_prescription = Prescription(
            patient_id=prescription.patient_id,
            doctor_id=prescription.doctor_id,
            diagnosis=prescription.diagnosis,
            medications=prescription.medications,
            instructions=prescription.instructions
        )
        db.add(db_prescription)
        await db.commit()
        await db.refresh(db_prescription)
        return db_prescription
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))

async def get_prescription_by_id(db: AsyncSession, prescription_id: int) -> Prescription:
    """
    Get a prescription by ID
    """
    result = await db.execute(select(Prescription).filter(Prescription.id == prescription_id))
    prescription = result.scalars().first()
    if not prescription:
        raise NotFoundError("Prescription", prescription_id)
    return prescription

async def get_prescriptions_by_doctor(db: AsyncSession, doctor_id: int, skip: int = 0, limit: int = 100) -> List[Prescription]:
    """
    Get all prescriptions for a specific doctor
    """
    result = await db.execute(
        select(Prescription)
        .filter(Prescription.doctor_id == doctor_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_prescriptions_by_patient(db: AsyncSession, patient_id: int, skip: int = 0, limit: int = 100) -> List[Prescription]:
    """
    Get all prescriptions for a specific patient
    """
    result = await db.execute(
        select(Prescription)
        .filter(Prescription.patient_id == patient_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def update_prescription(db: AsyncSession, prescription_id: int, prescription_update: PrescriptionUpdate) -> Prescription:
    """
    Update a prescription's information
    """
    try:
        db_prescription = await get_prescription_by_id(db, prescription_id)
        
        update_data = prescription_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_prescription, key, value)
            
        await db.commit()
        await db.refresh(db_prescription)
        return db_prescription
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))

async def delete_prescription(db: AsyncSession, prescription_id: int) -> bool:
    """
    Delete a prescription
    """
    try:
        db_prescription = await get_prescription_by_id(db, prescription_id)
        await db.delete(db_prescription)
        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))

async def update_prescription_file(db: AsyncSession, prescription_id: int, file_url: str) -> Prescription:
    """
    Update a prescription's file URL
    """
    try:
        db_prescription = await get_prescription_by_id(db, prescription_id)
        db_prescription.file_url = file_url
        await db.commit()
        await db.refresh(db_prescription)
        return db_prescription
    except Exception as e:
        await db.rollback()
        raise DatabaseError(str(e))