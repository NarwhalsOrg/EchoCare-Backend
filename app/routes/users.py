from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List, Optional
from app.core.dependencies import get_current_active_user, get_current_admin_user
from app.core.security import get_password_hash
from app.db.orm import CRUDBase
from app.models.user import User, UserUpdate, UserResponse
from app.utils.file_upload import upload_avatar
import uuid

router = APIRouter()
user_crud = CRUDBase(User)

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information
    """
    return current_user

@router.put("/users/me", response_model=UserResponse)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update current user information
    """
    try:
        update_data = user_update.dict(exclude_unset=True)
        
        # Hash the password if it's being updated
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # Don't allow users to change their admin status
        if "is_admin" in update_data:
            del update_data["is_admin"]
            
        updated_user = await user_crud.update(id=current_user.id, obj_in=update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )

@router.post("/users/me/avatar", response_model=UserResponse)
async def upload_user_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload user avatar
    """
    try:
        # Generate unique filename
        file_ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        filename = f"{current_user.id}_{uuid.uuid4()}.{file_ext}"
        
        # Upload file to Supabase storage
        avatar_url = await upload_avatar(file, filename)
        
        # Update user with new avatar URL
        update_data = {"avatar_url": avatar_url}
        updated_user = await user_crud.update(id=current_user.id, obj_in=update_data)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading avatar: {str(e)}"
        )

# Admin routes
@router.get("/users", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Retrieve users (admin only)
    """
    try:
        users = await user_crud.get_multi(skip=skip, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving users: {str(e)}"
        )

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: str,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Get a specific user by id (admin only)
    """
    try:
        user = await user_crud.get(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user: {str(e)}"
        )

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Update a user (admin only)
    """
    try:
        update_data = user_update.dict(exclude_unset=True)
        
        # Hash the password if it's being updated
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
            
        updated_user = await user_crud.update(id=user_id, obj_in=update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Delete a user (admin only)
    """
    try:
        # Prevent deleting yourself
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own user account"
            )
            
        success = await user_crud.delete(id=user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )