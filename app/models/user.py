from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from pydantic import EmailStr, validator
import uuid

class UserBase(SQLModel):
    email: EmailStr
    full_name: str
    is_active: bool = True
    is_admin: bool = False
    avatar_url: Optional[str] = None

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str
    password_confirm: str
    
    @validator('password_confirm')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    avatar_url: Optional[str] = None

class UserInDB(UserBase):
    id: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime