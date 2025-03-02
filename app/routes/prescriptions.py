from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List, Optional
from app.core.dependencies import get_current_active_user
from app.db.orm import CRUDBase
from app.models.user import User
from app.models.prescription import Prescription, PrescriptionCreate, PrescriptionUpdate, PrescriptionWithMedications, Medication
from app.utils.file_upload import upload_prescription
from app.db.supabase import get_supabase_client
import uuid

router = APIRouter()
prescription_crud = CRUDBase(Prescription)
medication_crud = CRUDBase(Medication)

@router.post("/prescriptions", response_model=PrescriptionWithMedications, status_code=status.HTTP_201_CREATED)
async def create_prescription(
    prescription_in: PrescriptionCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new prescription with medications
    """
    try:
        supabase = get_supabase_client()
        
        # Create prescription
        prescription_data = prescription_in.dict(exclude={"medications"})
        
        # Ensure doctor_id is set to current user if not specified
        if "doctor_id" not in prescription_data or not prescription_data["doctor_id"]:
            prescription_data["doctor_id"] = current_user.id
            
        new_prescription = await prescription_crud.create(obj_in=prescription_data)
        
        # Create medications
        medications = []
        for med in prescription_in.medications:
            med_data = med.dict()
            med_data["prescription_id"] = new_prescription.id
            
            response = supabase.table("medications").insert(med_data).execute()
            medications.append(response.data[0])
            
        # Return combined result
        result = new_prescription.dict()
        result["medications"] = medications
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating prescription: {str(e)}"
        )

@router.post("/prescriptions/{prescription_id}/upload", response_model=PrescriptionWithMedications)
async def upload_prescription_file(
    prescription_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload a prescription file (PDF, image, etc.)
    """
    try:
        # Check if prescription exists
        prescription = await prescription_crud.get(id=prescription_id)
        if not prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prescription not found"
            )
            
        # Generate unique filename
        file_ext = file.filename.split(".")[-1] if "." in file.filename else "pdf"
        filename = f"{prescription_id}_{uuid.uuid4()}.{file_ext}"
        
        # Upload file to Supabase storage
        file_url = await upload_prescription(file, filename)
        
        # Update prescription with file URL
        update_data = {"file_url": file_url}
        updated_prescription = await prescription_crud.update(id=prescription_id, obj_in=update_data)
        
        # Get medications for this prescription
        supabase = get_supabase_client()
        medications_response = supabase.table("medications").select("*").eq("prescription_id", prescription_id).execute()
        
        # Return combined result
        result = updated_prescription.dict()
        result["medications"] = medications_response.data
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading prescription file: {str(e)}"
        )

@router.get("/prescriptions", response_model=List[PrescriptionWithMedications])
async def read_prescriptions(
    skip: int = 0,
    limit: int = 100,
    patient_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve prescriptions with filtering options
    """
    try:
        supabase = get_supabase_client()
        query = supabase.table("prescriptions").select("*")
        
        # Apply filters
        if patient_id:
            query = query.eq("patient_id", patient_id)
        if doctor_id:
            query = query.eq("doctor_id", doctor_id)
            
        # Apply pagination
        prescriptions_response = query.range(skip, skip + limit - 1).execute()
        
        # Get medications for each prescription
        result = []
        for prescription_data in prescriptions_response.data:
            prescription = Prescription(**prescription_data)
            
            medications_response = supabase.table("medications").select("*").eq("prescription_id", prescription.id).execute()
            
            prescription_dict = prescription.dict()
            prescription_dict["medications"] = medications_response.data
            
            result.append(prescription_dict)
            
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving prescriptions: {str(e)}"
        )

@router.get("/prescriptions/{prescription_id}", response_model=PrescriptionWithMedications)
async def read_prescription(
    prescription_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific prescription by id with its medications
    """
    try:
        prescription = await prescription_crud.get(id=prescription_id)
        if not prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prescription not found"
            )
            
        # Get medications for this prescription
        supabase = get_supabase_client()
        medications_response = supabase.table("medications").select("*").eq("prescription_id", prescription_id).execute()
        
        # Return combined result
        result = prescription.dict()
        result["medications"] = medications_response.data
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving prescription: {str(e)}"
        )

@router.put("/prescriptions/{prescription_id}", response_model=PrescriptionWithMedications)
async def update_prescription(
    prescription_id: str,
    prescription_update: PrescriptionUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a prescription and its medications
    """
    try:
        # Check if prescription exists
        existing_prescription = await prescription_crud.get(id=prescription_id)
        if not existing_prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prescription not found"
            )
            
        supabase = get_supabase_client()
        
        # Update prescription
        prescription_data = prescription_update.dict(exclude={"medications"}, exclude_unset=True)
        if prescription_data:
            updated_prescription = await prescription_crud.update(id=prescription_id, obj_in=prescription_data)
        else:
            updated_prescription = existing_prescription
            
        # Update medications if provided
        if prescription_update.medications is not None:
            # Delete existing medications
            supabase.table("medications").delete().eq("prescription_id", prescription_id).execute()
            
            # Create new medications
            for med in prescription_update.medications:
                med_data = med.dict()
                med_data["prescription_id"] = prescription_id
                supabase.table("medications").insert(med_data).execute()
                
        # Get updated medications
        medications_response = supabase.table("medications").select("*").eq("prescription_id", prescription_id).execute()
        
        # Return combined result
        result = updated_prescription.dict()
        result["medications"] = medications_response.data
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating prescription: {str(e)}"
        )

@router.delete("/prescriptions/{prescription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prescription(
    prescription_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a prescription and its medications
    """
    try:
        # Check if prescription exists
        existing_prescription = await prescription_crud.get(id=prescription_id)
        if not existing_prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prescription not found"
            )
            
        supabase = get_supabase_client()
        
        # Delete medications first
        supabase.table("medications").delete().eq("prescription_id", prescription_id).execute()
        
        # Delete prescription
        success = await prescription_crud.delete(id=prescription_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete prescription"
            )
            
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting prescription: {str(e)}"
        )