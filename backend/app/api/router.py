from fastapi import APIRouter
from app.api.v1.auth import auth as auth_endpoints

api_router = APIRouter()

api_router.include_router(auth_endpoints.router, prefix="/auth", tags=["Auth"])