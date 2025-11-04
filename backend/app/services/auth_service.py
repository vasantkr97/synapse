from sqlalchemy.orm import Session
from app.models.user import User
from typing import Optional
from app.core.security import verify_password


class AuthService:

    @staticmethod
    def authenticate_user(db:Session, email:str , password: str) -> Optional[User]:
        """verify the user and return user or None"""
        user = db.query(User).filter(User.email == email).first()
        if user and verify_password(password, user.password):
            return user
        return None