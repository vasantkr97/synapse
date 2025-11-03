from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.core.security import create_access_token, get_password_hash
from app.core.config import settings
from app.models.user import User
from app.schema.user import Token, UserResponse, UserCreate
from app.schema.auth import SigninRequest, SignoutResponse, SignupResponse
from app.services.auth_service import AuthService
from datetime import timedelta


router = APIRouter()


@router.post("/signin", response_model=Token, status_code=status.HTTP_200_OK)
def signin(payload: SigninRequest, db: Session = Depends(get_db), response: Response = None):
    user = AuthService.authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    # Set HttpOnly cookie for the access token
    max_age = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES) * 60
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=max_age,
        httponly=True,
        samesite="lax",
        secure=False,
        path="/",
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signout", response_model=SignoutResponse, status_code=status.HTTP_200_OK)
def signout(response: Response):
    response.delete_cookie(key="access_token", path="/")
    return {"message": "Signed out"}


@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    # Check for existing email or username
    existing_email = db.query(User).filter(User.email == payload.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Optional: enforce unique username if you want to prevent duplicates
    existing_username = db.query(User).filter(User.username == payload.username).first()
    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    new_user = User(
        username=payload.username,
        email=payload.email,
        password=get_password_hash(payload.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": new_user}


