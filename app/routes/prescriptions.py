from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse, PrescriptionUpdate
from app.controllers.prescription_controller import (
    create_prescription, get_prescription_by_id, get_prescriptions_by_doctor,
    get_prescriptions_by_patient, update_prescription, delete_prescription, update_prescription_file
)
from app.controllers.patient_controller import get_patient_by_id
from app.utils.security import get_current_user
from app.schemas.token import TokenData
from app.utils.file_handler import upload_prescription_file
from typing import List

router = APIRouter()

@router.post("/", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_new_prescription(
    prescription: PrescriptionCreate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new prescription
    """
    # Set the doctor_id to the current user's ID
    prescription.doctor_id = current_user.user_id
    
    # Check if the patient exists and belongs to the current doctor
    patient = await get_patient_by_id(db, prescription.patient_id)
    if patient.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create a prescription for this patient"
        )
    
    return await create_prescription(db, prescription)

@router.get("/me", response_model=List[PrescriptionResponse])
async def read_my_prescriptions(
    skip: int = 0,
    limit: int = 100,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get all prescriptions for the current doctor
    """
    return await get_prescriptions_by_doctor(db, current_user.user_id, skip, limit)

@router.get("/patient/{patient_id}", response_model=List[PrescriptionResponse])
async def read_patient_prescriptions(
    patient_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get all prescriptions for a specific patient
    """
    # Check if the patient belongs to the current doctor
    patient = await get_patient_by_id(db, patient_id)
    if patient.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this patient's prescriptions"
        )
    
    return await get_prescriptions_by_patient(db, patient_id, skip, limit)

@router.get("/{prescription_id}", response_model=PrescriptionResponse)
async def read_prescription(
    prescription_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get prescription by ID
    """
    prescription = await get_prescription_by_id(db, prescription_id)
    
    # Check if the prescription belongs to the current doctor
    if prescription.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this prescription"
        )
    
    return prescription

@router.put("/{prescription_id}", response_model=PrescriptionResponse)
async def update_prescription_info(
    prescription_id: int,
    prescription_update: PrescriptionUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Update prescription information
    """
    prescription = await get_prescription_by_id(db, prescription_id)
    
    # Check if the prescription belongs to the current doctor
    if prescription.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this prescription"
        )
    
    return await update_prescription(db, prescription_id, prescription_update)

@router.delete("/{prescription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prescription_record(
    prescription_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Delete prescription
    """
    prescription = await get_prescription_by_id(db, prescription_id)
    
    # Check if the prescription belongs to the current doctor
    if prescription.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this prescription"
        )
    
    await delete_prescription(db, prescription_id)
    return None

@router.post("/{prescription_id}/file", response_model=PrescriptionResponse)
async def upload_prescription_document(
    prescription_id: int,
    file: UploadFile = File(...),
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Upload file for a prescription
    """
    prescription = await get_prescription_by_id(db, prescription_id)
    
    # Check if the prescription belongs to the current doctor
    if prescription.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this prescription"
        )
    
    file_url = await upload_prescription_file(file, prescription_id)
    return await update_prescription_file(db, prescription_id, file_url)