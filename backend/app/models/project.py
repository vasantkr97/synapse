from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_Column, ForeignKey, relationship
from sqlalchemy import String, Text, List, DateTime
from cuid import cuid
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.conversation import ConversationHistory


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_Column(
        String(32),
        nullable=True,
        primary_key=True,
        default=cuid,
        doc="Unique CUID-based project identifier"
    )

    title: Mapped[str] = mapped_Column(
        String(100),
        nullable=False,
        doc="project title"
    )

    initial_prompt: Mapped[str] = mapped_Column(
        Text,
        nullable=False,
        doc="initial project prompt"
    )

    user_id: Mapped[str] = mapped_Column(
        String(32),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Foreign key referencing the project's owner"
    )

    user: Mapped[User] = relationship(
        "User",
        back_populates="projects",
        lazy="joined",
        doc="User who owns this project"
    )

    conversation_history: Mapped[List["ConversationHistory"]] = relationship(
        "ConversationHistory",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        default=list,
        doc="Chronological chat history for this project"
    )

    created_at: Mapped[datetime] = mapped_Column(
        DateTime(timezone=True),
        server_default = func.now(),
        nullable=False,
        doc="Timestamp when the project was created"
    )

    updated_at: Mapped[datetime] = mapped_Column(
        DateTime(timezone=True),
        server_default = func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Timestamp when the projects was udpated"
    )

    def __repr__(self) -> str:
        return (
            f"<Project id={self.id!r}, title={self.title!r}, user_id={self.user_id!r}>"
        )