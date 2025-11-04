from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.schema.user import UserResponse
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common Fields"""
    username: str =  Field(..., min_length=3, max_length=50)
    email: EmailStr

class SigninSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class SignupSchema(UserBase):
    password: str = Field(..., min_length=8, max_length=50)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AuthResponse(BaseModel):
    message: str
    token: str
    user: UserResponse

class MeResponse(BaseModel):
    user: UserResponse