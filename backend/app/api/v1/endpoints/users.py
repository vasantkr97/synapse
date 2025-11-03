from fastapi import APIRouter, Depends, status
from sqlalchemy import Session
from typing import List
from app.core.db import get_db
from app.schema.user import UserResonse, UserUpdate
from app.models.user import User
from app.services.user_service import UserServices

router = APIRouter(prefix="/users", tags=["Users"])

