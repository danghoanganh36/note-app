from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any, Dict, Optional


class TimestampMixin:
    """Mixin for automatic timestamp tracking"""
    
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            TIMESTAMP(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            nullable=False
        )
    
    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            TIMESTAMP(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False
        )


class UUIDMixin:
    """Mixin for UUID primary key"""
    
    @declared_attr
    def id(cls) -> Mapped[UUID]:
        return mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid4
        )


class SoftDeleteMixin:
    """Mixin for soft delete functionality"""
    
    @declared_attr
    def deleted_at(cls) -> Mapped[Optional[datetime]]:
        return mapped_column(
            TIMESTAMP(timezone=True),
            nullable=True,
            default=None
        )
    
    def soft_delete(self) -> "SoftDeleteMixin":
        """Mark record as deleted"""
        self.deleted_at = datetime.now(timezone.utc)
        return self
    
    def restore(self) -> "SoftDeleteMixin":
        """Restore soft-deleted record"""
        self.deleted_at = None
        return self
    
    @property
    def is_deleted(self) -> bool:
        """Check if record is soft-deleted"""
        return self.deleted_at is not None


class Base(UUIDMixin, TimestampMixin, SoftDeleteMixin, DeclarativeBase):
    """Base class for all SQLAlchemy models
    
    Includes:
    - UUID primary key (id)
    - Automatic timestamps (created_at, updated_at)
    - Soft delete support (deleted_at)
    - Utility methods (to_dict, update_from_dict)
    """
    
    __abstract__ = True
    
    def to_dict(self, exclude: Optional[list] = None) -> Dict[str, Any]:
        """Convert model to dictionary
        
        Args:
            exclude: List of field names to exclude
            
        Returns:
            Dictionary representation of model
        """
        exclude = exclude or []
        result = {}
        
        for column in self.__table__.columns:
            if column.name in exclude:
                continue
                
            value = getattr(self, column.name)
            
            # Convert datetime to ISO string
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            # Convert UUID to string
            elif hasattr(value, 'hex'):
                result[column.name] = str(value)
            else:
                result[column.name] = value
                
        return result
    
    def update_from_dict(self, data: Dict[str, Any]) -> "Base":
        """Update model from dictionary
        
        Args:
            data: Dictionary with field values
            
        Returns:
            Self for method chaining
        """
        for key, value in data.items():
            # Skip if attribute doesn't exist
            if not hasattr(self, key):
                continue
            # Skip primary key
            if key == 'id':
                continue
            # Skip timestamp fields (handled automatically)
            if key in ('created_at', 'updated_at'):
                continue
                
            setattr(self, key, value)
            
        return self
    
    def __repr__(self) -> str:
        """String representation for debugging"""
        return f"<{self.__class__.__name__}(id={self.id})>"
