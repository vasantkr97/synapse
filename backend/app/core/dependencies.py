from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from app.core.db import get_db
from app.core.security import decode_token
from app.models.user import User

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

async def 