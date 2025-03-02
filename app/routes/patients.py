from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.core.dependencies import get_current_active_user
from app.db.orm import CRUDBase
from app.models.user import User
from app.models.patient import Patient, PatientCreate, PatientUpdate, PatientResponse
from app.db.supabase import get_supabase_client

router = APIRouter()
patient_crud = CRUDBase(Patient)

@router.post("/patients", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient_in: PatientCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new patient
    """
    try:
        patient_data = patient_in.dict()
        patient_data["created_by"] = current_user.id
        
        new_patient = await patient_crud.create(obj_in=patient_data)
        return new_patient
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating patient: {str(e)}"
        )

@router.get("/patients", response_model=List[PatientResponse])
async def read_patients(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve patients with optional search
    """
    try:
        supabase = get_supabase_client()
        query = supabase.table("patients").select("*")
        
        if search:
            query = query.or_(f"first_name.ilike.%{search}%,last_name.ilike.%{search}%")
            
        response = query.range(skip, skip + limit - 1).execute()
        
        return [Patient(**item) for item in response.data]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving patients: {str(e)}"
        )

@router.get("/patients/{patient_id}", response_model=PatientResponse)
async def read_patient(
    patient_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific patient by id
    """
    try:
        patient = await patient_crud.get(id=patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        return patient
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving patient: {str(e)}"
        )

@router.put("/patients/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: str,
    patient_update: PatientUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a patient
    """
    try:
        update_data = patient_update.dict(exclude_unset=True)
        
        # Check if patient exists
        existing_patient = await patient_crud.get(id=patient_id)
        if not existing_patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
            
        updated_patient = await patient_crud.update(id=patient_id, obj_in=update_data)
        return updated_patient
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating patient: {str(e)}"
        )

@router.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a patient
    """
    try:
        # Check if patient exists
        existing_patient = await patient_crud.get(id=patient_id)
        if not existing_patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
            
        success = await patient_crud.delete(id=patient_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete patient"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting patient: {str(e)}"
        )