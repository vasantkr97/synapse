from pydantic import BaseModel, EmailStr, Field
from app.schema.user import UserResponse

class SigninRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class SignoutResponse(BaseModel):
    message: str

class SingupResponse(BaseModel):
    message: str
    user: UserResponse
