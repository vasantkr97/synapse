from fastapi import APIRouter
from app.api.auth import auth as auth_endpoints
from app.api.projects import generate as generate_endpoints

api_router = APIRouter()

api_router.include_router(auth_endpoints.router, prefix="/auth", tags=["Auth"])
api_router.include_router(generate_endpoints.router, prefix="/generate", tags=["Projects"])