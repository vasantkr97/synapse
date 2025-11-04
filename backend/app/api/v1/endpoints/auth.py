from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from jose import jwt
from datetime import timedelta
from app.core.db import get_db
from app.core.config import settings
from app.services.auth_service import AuthService
from app.core.dependencies import require_user
from app.core.security import get_password_hash
from app.models.user import User
from app.schema.auth import AuthResponse, SignupSchema, SigninSchema, UserResponse, MeResponse
from app.core.security import create_access_token, verify_password
from app.core.dependencies import get_current_user


router = APIRouter()

@router.post("/signup", response_model=AuthResponse, status_code = status.HTTP_201_CREATED)
async def signup(payload: SignupSchema, response: Response, db: Session = Depends(get_db)):
    """Signing up new user"""
    
    existing_user = await db.quey(User).filter(User.email == payload.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User alreay exits"
        )
    
    hashed_password = get_password_hash(payload.password)

    new_user = User(
        email = payload.email,
        username = payload.username,
        password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(
        data={"id": str(new_user.id), "email": new_user.email },
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    response.set_cookie(
        key="token",
        value=create_access_token,
        httponly=True,
        samesite="strict",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60,
    )

    return AuthResponse(
        message="user created successfully",
        token= token,
        user=UserResponse.model_validate(new_user)
    )


@router.post('/signin', response_model=AuthResponse)
async def signin(credentials: SigninSchema, response: Response, db:Session = Depends(get_db)):
    """login user and return token"""
    
    user = await db.query(User).filter(User.email == credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    
    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect password"
        )
    
    token = create_access_token(
        data={"id": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    response.set_cookie(
        key="token",
        value="access_token",
        httponly=True,
        samesite="strict",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60
    )

    return AuthResponse(
        message="User logged in Sucessfully",
        token= token,
        user=UserResponse.model_validate(user)
    )


@router.post("/signout")
def signout(response: Response):
    "logout user by clearing the token cookie"

    response.delete_cookie(key="token", httponly=True, samesite=True)

    return { "message": "logout successfully" }


@router.get("/me", response_model=MeResponse)
async def get_me( current_user: User = Depends(get_current_user), db:Session = Depends(get_db)):
    """get current authenticated user information"""

    user = await db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return MeResponse(
        user=UserResponse.model_validate(user)
        )




@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(require_user)):
    return current_user



    # Check for existing email or username
    existing_email = db.query(User).filter(User.email == payload.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

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