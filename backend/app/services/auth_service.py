from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.core.security import verify_password


class AuthService:
    """Authentication utilities."""

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Return the user if the credentials are valid; otherwise None."""
        user = db.query(User).filter(User.email == email).first()
        if user and verify_password(password, user.password):
            return user
        return None