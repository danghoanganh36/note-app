import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.db import Base

if TYPE_CHECKING:
    from app.models.document import Document, DocumentVersion
    from app.models.folder import Folder

class User(Base):
    __tablename__ = "users"

    # Fields
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(255))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500))
    bio: Mapped[Optional[str]]
    role: Mapped[str] = mapped_column(String(50), default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[Optional[datetime.datetime]]

    # Relationships (back_populates must match Document/Folder models)
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="owner",
                                                       foreign_keys="[Document.owner_id]")
    folders: Mapped[list["Folder"]] = relationship("Folder", back_populates="owner")
    document_versions: Mapped[list["DocumentVersion"]] = relationship("DocumentVersion", back_populates="user",
                                                                      foreign_keys="[DocumentVersion.changed_by]")
    sessions: Mapped[list["UserSession"]] = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")


class UserSession(Base):
    __tablename__ = "user_sessions"

    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    access_token: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True, index=True)
    refresh_token: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True, index=True)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    device_info: Mapped[Optional[str]] = mapped_column(String(500))
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="sessions")
