from sqlalchemy import String, Text, Integer, Boolean, Index, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.folder import Folder


class Document(Base):
    __tablename__ = 'documents'
    
    # Base đã có: id, created_at, updated_at, deleted_at
    # Chỉ khai báo fields riêng của Document
    
    owner_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False, default='')
    access_level: Mapped[str] = mapped_column(String(50), nullable=False, default='private')
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    folder_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('folders.id', ondelete='SET NULL'), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    owner: Mapped["User"] = relationship(back_populates="documents")
    folder: Mapped[Optional["Folder"]] = relationship(back_populates="documents")
    versions: Mapped[list["DocumentVersion"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_documents_owner_id', 'owner_id'),
        Index('idx_documents_folder_id', 'folder_id'),
        Index('idx_documents_created_at', 'created_at'),
        CheckConstraint("access_level IN ('private', 'shared', 'public')", name='check_access_level'),
    )

class DocumentVersion(Base):
    __tablename__ = 'document_versions'

    document_id: Mapped[UUID] = mapped_column(ForeignKey('documents.id', ondelete='CASCADE'), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    changed_by: Mapped[Optional[UUID]] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    change_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    document: Mapped["Document"] = relationship(back_populates="versions")
    user: Mapped[Optional["User"]] = relationship()

    __table_args__ = (
        Index('idx_document_versions_document_id', 'document_id'),
        Index('idx_document_versions_version', 'version'),
    )