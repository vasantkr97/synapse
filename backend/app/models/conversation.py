from app.db.core import Base
from sqlalchemy.orm import Mapped, mapped_Column
from sqlalchemy import String, ForeignKey, relationship, Text, List, Dict, Enum as SQLEnum, JSON, DateTime, func
from typing import TYPE_CHECKING, Any
from enum import Enum
from cuid import cuid
from datetime import datetime

if TYPE_CHECKING:
    from app.models.project import Project

class RoleType(str,Enum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class ToolCallType(str, Enum):
    READ_FILE = "read_file"
    WRITE_FILE= "write_file"
    DELETE_FILE = "delete_file"
    UPDATE_FILE = "update_file"


class ConversationHistory(Base):
    __tablename__ = "conversation_history"

    id: Mapped[str] = mapped_Column(
        String(32),
        primary_key=True,
        default=cuid,
        doc="unique cuid-based conversation identifier"
    )
    projectId: Mapped[str] = mapped_Column(
        String(32),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        doc="Foreign key referencing the projects Id"
    )

    Project: Mapped[Project] = relationship(
        "Project",
        back_populates="conversation_history",
        lazy='joined',
        doc="conversation which project owns this"
    )
    
    role: Mapped[RoleType] = mapped_Column(
        SQLEnum(RoleType),
        nullable=False,
        index=True,
        doc="from which the message is coming from (user, assistant, tool)",
    )

    #The text content of the message

    contents: Mapped[str | None] = mapped_Column(
        Text,
        nullable=True,
        doc="Text content: users message and assistant message"
    )

    tool_calls: Mapped[List[Dict[str, Any]] | None] = mapped_Column(
        JSON,
        nullable=True,
        doc="JSon list of tool calls requested by the assistant"
    )

    tool_call_id: Mapped[str | None] = mapped_Column(
        String(64),
        nullable=True,
        index=True,
        doc="ID of the tool call for which tool message is this result for"
    )
    Created_at: Mapped[datetime] = mapped_Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="timeatamp when conversation happened"
    )

    def __repr__(self) -> str:
        return f"<ConversationHistory id={self.id!r} projectId={self.projectId!r}>"