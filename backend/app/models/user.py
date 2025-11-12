from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from cuid import cuid
from datetime import datetime
from sqlalchemy.sql import func
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.project import Project


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        default=cuid,
        doc="unique cuid-based user identifier"
    )

    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="Public display name for the user"
    )

    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
        doc="User's unique email address"
    )

    password: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="Bcrypt hashed password"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Timestamp for the user was created"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Timestamp for the last user update"
    )

    projects: Mapped[List["Project"]] = relationship(
        "Project",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        doc="List of projects created by this user"
    )

    def __repr__(self) -> str:
        return (
            f"<User id={self.id!r}, username={self.username!r}, email={self.email!r}>"
        )
    

