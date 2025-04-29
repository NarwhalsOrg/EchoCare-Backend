from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session
from app.schemas.user import UserResponse, UserUpdate
from app.controllers.user_controller import get_user_by_id, get_all_users, update_user, delete_user, update_user_avatar
from app.utils.security import get_current_user, get_admin_user
from app.schemas.token import TokenData
from app.utils.file_handler import upload_avatar
from typing import List

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get current user information
    """
    return await get_user_by_id(db, current_user.user_id)

@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_update: UserUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Update current user information
    """
    # Prevent user from changing admin status
    if hasattr(user_update, "is_admin") and user_update.is_admin is not None:
        user_update.is_admin = None
    
    return await update_user(db, current_user.user_id, user_update)

@router.post("/me/avatar", response_model=UserResponse)
async def upload_user_avatar(
    file: UploadFile = File(...),
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Upload avatar for current user
    """
    avatar_url = await upload_avatar(file, current_user.user_id)
    return await update_user_avatar(db, current_user.user_id, avatar_url)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    current_user: TokenData = Depends(get_admin_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get user by ID (admin only)
    """
    return await get_user_by_id(db, user_id)

@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: TokenData = Depends(get_admin_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Get all users (admin only)
    """
    return await get_all_users(db, skip, limit)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_by_id(
    user_id: int,
    user_update: UserUpdate,
    current_user: TokenData = Depends(get_admin_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Update user by ID (admin only)
    """
    return await update_user(db, user_id, user_update)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    user_id: int,
    current_user: TokenData = Depends(get_admin_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Delete user by ID (admin only)
    """
    # Prevent admin from deleting themselves
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    await delete_user(db, user_id)
    return None