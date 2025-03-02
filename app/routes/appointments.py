from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.dependencies import get_current_active_user
from app.db.orm import CRUDBase
from app.models.user import User
from app.models.appointment import Appointment, AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.db.supabase import get_supabase_client

router = APIRouter()
appointment_crud = CRUDBase(Appointment)

@router.post("/appointments", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment_in: AppointmentCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new appointment
    """
    try:
        # Validate appointment date is in the future
        if appointment_in.appointment_date < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment date must be in the future"
            )
            
        # Create appointment
        new_appointment = await appointment_crud.create(obj_in=appointment_in.dict())
        return new_appointment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating appointment: {str(e)}"
        )

@router.get("/appointments", response_model=List[AppointmentResponse])
async def read_appointments(
    skip: int = 0,
    limit: int = 100,
    patient_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    status: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve appointments with filtering options
    """
    try:
        supabase = get_supabase_client()
        query = supabase.table("appointments").select("*")
        
        # Apply filters
        if patient_id:
            query = query.eq("patient_id", patient_id)
        if doctor_id:
            query = query.eq("doctor_id", doctor_id)
        if status:
            query = query.eq("status", status)
        if from_date:
            query = query.gte("appointment_date", from_date.isoformat())
        if to_date:
            query = query.lte("appointment_date", to_date.isoformat())
            
        # Apply pagination
        response = query.range(skip, skip + limit - 1).execute()
        
        return [Appointment(**item) for item in response.data]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving appointments: {str(e)}"
        )

@router.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def read_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific appointment by id
    """
    try:
        appointment = await appointment_crud.get(id=appointment_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
        return appointment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving appointment: {str(e)}"
        )

@router.put("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: str,
    appointment_update: AppointmentUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an appointment
    """
    try:
        # Check if appointment exists
        existing_appointment = await appointment_crud.get(id=appointment_id)
        if not existing_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
            
        update_data = appointment_update.dict(exclude_unset=True)
        
        # Validate appointment date if being updated
        if "appointment_date" in update_data and update_data["appointment_date"] < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment date must be in the future"
            )
            
        updated_appointment = await appointment_crud.update(id=appointment_id, obj_in=update_data)
        return updated_appointment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating appointment: {str(e)}"
        )

@router.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete an appointment
    """
    try:
        # Check if appointment exists
        existing_appointment = await appointment_crud.get(id=appointment_id)
        if not existing_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
            
        success = await appointment_crud.delete(id=appointment_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete appointment"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting appointment: {str(e)}"
        )