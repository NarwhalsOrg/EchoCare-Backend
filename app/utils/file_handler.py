import os
import uuid
from fastapi import UploadFile, HTTPException
from app.db.supabase import supabase, AVATAR_BUCKET, PRESCRIPTION_BUCKET
from typing import Optional

async def upload_avatar(file: UploadFile, user_id: int) -> str:
    """
    Upload avatar to Supabase storage and return the file URL
    """
    return await upload_file(file, AVATAR_BUCKET, f"user_{user_id}")

async def upload_patient_avatar(file: UploadFile, patient_id: int) -> str:
    """
    Upload patient avatar to Supabase storage and return the file URL
    """
    return await upload_file(file, AVATAR_BUCKET, f"patient_{patient_id}")

async def upload_prescription_file(file: UploadFile, prescription_id: int) -> str:
    """
    Upload prescription file to Supabase storage and return the file URL
    """
    return await upload_file(file, PRESCRIPTION_BUCKET, f"prescription_{prescription_id}")


async def upload_file(file: UploadFile, bucket: str, prefix: str) -> str:
    """
    Generic file upload function for Supabase storage
    """
    try:
        # Validate file type
        file_extension = os.path.splitext(file.filename)[1].lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Read file content
        contents = await file.read()
        
        # Generate unique filename
        unique_filename = f"{prefix}_{uuid.uuid4()}{file_extension}"
        
        # Upload to Supabase
        response = supabase.storage.from_(bucket).upload(
            unique_filename,
            contents,
            {"content-type": file.content_type}
        )
        
        # Get public URL
        file_url = supabase.storage.from_(bucket).get_public_url(unique_filename)
        
        return file_url
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

async def delete_file(file_path: str, bucket: str) -> bool:
    """
    Delete file from Supabase storage
    """
    try:
        # Extract filename from URL or path
        filename = file_path.split("/")[-1]
        
        # Delete from Supabase
        supabase.storage.from_(bucket).remove(filename)
        
        return True
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File deletion failed: {str(e)}")