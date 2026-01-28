import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.document import Document, DocumentVersion, Folder

class User(Base):
    __table__ = "users"

    # Fields
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(255))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500))
    bio: Mapped[Optional[str]]
    role: Mapped[str] = mapped_column(String(50), default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[Optional[datetime]]

    # Relationships (back_populates must match Document/Folder models)
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="owner",
                                                       foreign_keys="[Document.owner_id]")
    folders: Mapped[list["Folder"]] = relationship("Folder", back_populates="owner")
    document_versions: Mapped[list["DocumentVersion"]] = relationship("DocumentVersion", back_populates="user",
                                                                      foreign_keys="[DocumentVersion.changed_by]")
