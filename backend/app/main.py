from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from app.core.security import decode_token
from app.core.db import SessionLocal
from app.models.user import User
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="synapse"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS.split(",") if settings.BACKEND_CORS_ORIGINS else ["*"]
)

app.include_router(api_router, prefix="/api/v1")

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1].strip()
    if not token:
        token = request.cookies.get("access_token")
    if token:
        try:
            payload = decode_token(token, token_type="access")
            user_id = int(payload.get("sub"))
            db = SessionLocal()
            try:
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    request.state.user = user
            finally:
                db.close()
        except Exception:
            # Silently ignore invalid tokens; route-level deps can enforce auth
            pass
    response = await call_next(request)
    return response

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "FastAPI Synapse.ai"
    }


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    return {"status": "healthy"}






