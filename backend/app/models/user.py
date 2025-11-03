from sqlalchemy import String, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    #Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True )

    username: Mapped[str] = mapped_column( String(50), nullable=False )

    email: Mapped[str] = mapped_column( String(100), unique=True, nullable=False, index=True )

    password: Mapped[str] = mapped_column( String(255), nullable=False )

    created_at: Mapped[datetime] = mapped_column( DateTime(timezone=True), server_default=func.now(), nullable=False )

    updated_at: Mapped[datetime] = mapped_column( DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False )

    def __repr__(self):
        return f"<User (id={self.id}, username={self.username}, email={self.email})>"
    

class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, is_revoked={self.is_revoked})>"

   


