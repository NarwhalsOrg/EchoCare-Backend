from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.controllers.user_controller import create_user, get_user_by_email
from app.utils.security import verify_password, create_access_token
from app.utils.exceptions import AuthenticationError
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
    """
    Register a new user
    """
    # Check if email already exists
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    return await create_user(db, user)

@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    """
    Authenticate a user and return a JWT token
    """
    # Get user by email
    user = await get_user_by_email(db, form_data.username)  # OAuth2 form uses username field for email
    
    # Check if user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise AuthenticationError()
    
    # Check if user is active
    if not user.is_active:
        raise AuthenticationError("User account is disabled")
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "is_admin": user.is_admin},
        expires_delta=access_token_expires
    )
    
    # Set cookie with token
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,  # 30 minutes
        expires=1800,
        samesite="lax",
        secure=False  # Set to True in production with HTTPS
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(response: Response):
    """
    Logout a user by clearing the cookie
    """
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}