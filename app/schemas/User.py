from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    user_id: str
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
