from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.core.security import create_access_token
from app.models.user import User
from app.schema.user import Token, UserResponse, MessageResponse
from app.services.auth_service import AuthService


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


router = APIRouter()


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def logout():
    # Stateless JWT: client should discard the token
    return {"message": "Logged out"}


@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


