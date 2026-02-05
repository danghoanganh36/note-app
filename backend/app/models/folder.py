from sqlalchemy import String, Integer, Index, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.document import Document


class Folder(Base):
    __tablename__ = "folders"

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("folders.id", ondelete="CASCADE"), nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="folders")
    parent: Mapped[Optional["Folder"]] = relationship(
        "Folder", 
        back_populates="children", 
        remote_side="[Folder.id]"
    )
    children: Mapped[list["Folder"]] = relationship(
        "Folder",
        back_populates="parent", 
        cascade="all, delete-orphan"
    )
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="folder")

    __table_args__ = (
        Index('idx_folders_owner_id', 'owner_id'),
        Index('idx_folders_parent_id', 'parent_id'),
    )
