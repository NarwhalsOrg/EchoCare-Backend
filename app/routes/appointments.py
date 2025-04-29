from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session
from app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from app.controllers.appointment_controller import (
    create_appointment, get_appointment_by_id, get_appointments_by_doctor,
    get_appointments_by_patient, get_upcoming_appointments, update_appointment, delete_appointment
)
from app.controllers.patient_controller import get_patient_by_id
from app.utils.security import get_current_user
from app.schemas.token import TokenData
from typing import List

router = APIRouter()

@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_new_appointment(
    appointment: AppointmentCreate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new appointment
    """
    # Set the doctor_id to the current user's ID
    appointment.doctor_id = current_user.user_id
    
    # Check if the patient exists and belongs to the current doctor
    patient = await get_patient_by_id(db, appointment.patient_id)
    if patient.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create an appointment for this patient"
        )
    
    return await create_appointment(db, appointment)

@router.get("/me", response_model=List[AppointmentResponse])
async def read_my_appointments(
    skip: int = 0,
    limit: int = 100,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get all appointments for the current doctor
    """
    return await get_appointments_by_doctor(db, current_user.user_id, skip, limit)

@router.get("/upcoming", response_model=List[AppointmentResponse])
async def read_upcoming_appointments(
    skip: int = 0,
    limit: int = 100,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get upcoming appointments for the current doctor
    """
    return await get_upcoming_appointments(db, current_user.user_id, skip, limit)

@router.get("/patient/{patient_id}", response_model=List[AppointmentResponse])
async def read_patient_appointments(
    patient_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get all appointments for a specific patient
    """
    # Check if the patient belongs to the current doctor
    patient = await get_patient_by_id(db, patient_id)
    if patient.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this patient's appointments"
        )
    
    return await get_appointments_by_patient(db, patient_id, skip, limit)

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def read_appointment(
    appointment_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get appointment by ID
    """
    appointment = await get_appointment_by_id(db, appointment_id)
    
    # Check if the appointment belongs to the current doctor
    if appointment.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this appointment"
        )
    
    return appointment

@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment_info(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Update appointment information
    """
    appointment = await get_appointment_by_id(db, appointment_id)
    
    # Check if the appointment belongs to the current doctor
    if appointment.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this appointment"
        )
    
    return await update_appointment(db, appointment_id, appointment_update)

@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment_record(
    appointment_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Delete appointment
    """
    appointment = await get_appointment_by_id(db, appointment_id)
    
    # Check if the appointment belongs to the current doctor
    if appointment.doctor_id != current_user.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this appointment"
        )
    
    await delete_appointment(db, appointment_id)
    return None