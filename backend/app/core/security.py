from datetime import datetime, timedelta, timezone
from typing import Optional 
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, hash_password: str) -> bool:
    return pwd_context.verify(password, hash_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access Token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({ 'exp': expire, "type": "access" })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create JWT refresh Token."""
    
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    """Decode and verify JWT Token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return payload
    except JWTError:
        return None