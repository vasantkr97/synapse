from sqlalchemy import String, Integer, DateTime
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



class Projects(Base):
    __tablenames__ = "projects"

    