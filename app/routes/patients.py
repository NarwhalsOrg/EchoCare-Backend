from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from app.controllers.patient_controller import (
    create_patient, get_patient_by_id, get_patients_by_doctor,
    get_all_patients, update_patient, delete_patient, update_patient_avatar
)
from app.utils.security import get_current_user, get_admin_user
from app.schemas.token import TokenData
from app.utils.file_handler import upload_patient_avatar
from typing import List

router = APIRouter()

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_new_patient(
    patient: PatientCreate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new patient
    """
    # Set the doctor_id to the current user's ID if not provided
    if not patient.doctor_id:
        patient.doctor_id = current_user.user_id
    
    # Only admins can create patients for other doctors
    if patient.doctor_id != current_user.user_id and not current_user.is_admin:
        patient.doctor_id = current_user.user_id
    
    return await create_patient(db, patient)

@router.get("/me", response_model=List[PatientResponse])
async def read_my_patients(
    skip: int = 0,
    limit: int = 100,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get all patients for the current doctor
    """
    return await get_patients_by_doctor(db, current_user.user_id, skip, limit)

@router.get("/{patient_id}", response_model=PatientResponse)
async def read_patient(
    patient_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get patient by ID
    """
    patient = await get_patient_by_id(db, patient_id)
    
    # Check if the patient belongs to the current doctor or if the user is an admin
    if patient.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this patient"
        )
    
    return patient

@router.get("/", response_model=List[PatientResponse])
async def read_patients(
    skip: int = 0,
    limit: int = 100,
    current_user: TokenData = Depends(get_admin_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get all patients (admin only)
    """
    return await get_all_patients(db, skip, limit)

@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient_info(
    patient_id: int,
    patient_update: PatientUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Update patient information
    """
    patient = await get_patient_by_id(db, patient_id)
    
    # Check if the patient belongs to the current doctor or if the user is an admin
    if patient.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this patient"
        )
    
    # Only admins can change the doctor_id
    if patient_update.doctor_id is not None and patient_update.doctor_id != patient.doctor_id and not current_user.is_admin:
        patient_update.doctor_id = patient.doctor_id
    
    return await update_patient(db, patient_id, patient_update)

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient_record(
    patient_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Delete patient
    """
    patient = await get_patient_by_id(db, patient_id)
    
    # Check if the patient belongs to the current doctor or if the user is an admin
    if patient.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this patient"
        )
    
    await delete_patient(db, patient_id)
    return None

@router.post("/{patient_id}/avatar", response_model=PatientResponse)
async def upload_patient_profile_image(
    patient_id: int,
    file: UploadFile = File(...),
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Upload avatar for a patient
    """
    patient = await get_patient_by_id(db, patient_id)
    
    # Check if the patient belongs to the current doctor or if the user is an admin
    if patient.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this patient"
        )
    
    avatar_url = await upload_patient_avatar(file, patient_id)
    return await update_patient_avatar(db, patient_id, avatar_url)