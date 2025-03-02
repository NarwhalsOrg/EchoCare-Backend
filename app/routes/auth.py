from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from datetime import timedelta
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, verify_password, get_password_hash
from app.db.orm import CRUDBase
from app.models.user import User, UserCreate, UserResponse
from app.models.auth import Token, LoginRequest
from app.db.supabase import get_supabase_client
from jose import jwt, JWTError

router = APIRouter()
user_crud = CRUDBase(User)

@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    """
    Register a new user
    """
    try:
        # Check if user already exists
        supabase = get_supabase_client()
        response = supabase.table("users").select("*").eq("email", user_in.email).execute()
        
        if response.data and len(response.data) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user_data = user_in.dict(exclude={"password", "password_confirm"})
        user_data["hashed_password"] = get_password_hash(user_in.password)
        
        new_user = await user_crud.create(obj_in=user_data)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.post("/auth/login", response_model=Token)
async def login(response: Response, login_data: LoginRequest):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        supabase = get_supabase_client()
        db_response = supabase.table("users").select("*").eq("email", login_data.email).execute()
        
        if not db_response.data or len(db_response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = User(**db_response.data[0])
        
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(user.id, expires_delta=access_token_expires)
        
        # Create refresh token
        refresh_token = create_refresh_token(user.id)
        
        # Set refresh token as HttpOnly cookie if remember_me is True
        if login_data.remember_me:
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
                samesite="lax",
                secure=True,
            )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )

@router.post("/auth/refresh", response_model=Token)
async def refresh_token(response: Response, refresh_token: Optional[str] = Cookie(None)):
    """
    Refresh access token
    """
    try:
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token missing",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        try:
            payload = jwt.decode(
                refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            user_id: str = payload.get("sub")
            token_type: str = payload.get("type")
            
            if user_id is None or token_type != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(user_id, expires_delta=access_token_expires)
        
        # Create new refresh token
        new_refresh_token = create_refresh_token(user_id)
        
        # Set new refresh token as HttpOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
            samesite="lax",
            secure=True,
        )
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh error: {str(e)}"
        )

@router.post("/auth/logout")
async def logout(response: Response):
    """
    Logout user by clearing the refresh token cookie
    """
    response.delete_cookie(key="refresh_token")
    return {"detail": "Successfully logged out"}