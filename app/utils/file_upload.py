from fastapi import UploadFile, HTTPException, status
from app.core.config import settings
from app.db.supabase import get_supabase_storage
import io

async def upload_avatar(file: UploadFile, filename: str) -> str:
    """
    Upload avatar to Supabase storage and return the public URL
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Get storage client
        storage = get_supabase_storage()
        
        # Create bucket if it doesn't exist
        try:
            storage.create_bucket(settings.SUPABASE_BUCKET_AVATARS)
        except Exception:
            # Bucket might already exist, continue
            pass
        
        # Upload file
        storage.from_(settings.SUPABASE_BUCKET_AVATARS).upload(
            path=filename,
            file=contents,
            file_options={"content-type": file.content_type}
        )
        
        # Get public URL
        file_url = storage.from_(settings.SUPABASE_BUCKET_AVATARS).get_public_url(filename)
        
        return file_url
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading avatar: {str(e)}"
        )
    finally:
        # Reset file pointer for potential reuse
        await file.seek(0)

async def upload_prescription(file: UploadFile, filename: str) -> str:
    """
    Upload prescription file to Supabase storage and return the public URL
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Get storage client
        storage = get_supabase_storage()
        
        # Create bucket if it doesn't exist
        try:
            storage.create_bucket(settings.SUPABASE_BUCKET_PRESCRIPTIONS)
        except Exception:
            # Bucket might already exist, continue
            pass
        
        # Upload file
        storage.from_(settings.SUPABASE_BUCKET_PRESCRIPTIONS).upload(
            path=filename,
            file=contents,
            file_options={"content-type": file.content_type}
        )
        
        # Get public URL
        file_url = storage.from_(settings.SUPABASE_BUCKET_PRESCRIPTIONS).get_public_url(filename)
        
        return file_url
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading prescription file: {str(e)}"
        )
    finally:
        # Reset file pointer for potential reuse
        await file.seek(0)