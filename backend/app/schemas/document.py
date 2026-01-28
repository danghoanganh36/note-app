from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


# ============== Document Schemas ==============

class DocumentBase(BaseModel):
    """Base schema for Document"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    content: str = Field(default="")
    category: Optional[str] = None
    folder_id: Optional[UUID] = None
    is_pinned: bool = False


class DocumentCreate(DocumentBase):
    """Schema for creating a new document"""
    pass


class DocumentUpdate(BaseModel):
    """Schema for updating a document"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    folder_id: Optional[UUID] = None
    is_pinned: Optional[bool] = None


class DocumentResponse(DocumentBase):
    """Schema for document response"""
    id: UUID
    owner_id: UUID
    access_level: str
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class DocumentDetail(DocumentResponse):
    """Schema for detailed document response with versions"""
    versions: list["DocumentVersionResponse"] = []


# ============== DocumentVersion Schemas ==============

class DocumentVersionResponse(BaseModel):
    """Schema for document version response"""
    id: UUID
    document_id: UUID
    version: int
    content: str
    changed_by: Optional[UUID] = None
    change_summary: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============== Folder Schemas ==============

class FolderBase(BaseModel):
    """Base schema for Folder"""
    name: str = Field(..., min_length=1, max_length=255)
    parent_id: Optional[UUID] = None
    sort_order: int = 0


class FolderCreate(FolderBase):
    """Schema for creating a new folder"""
    pass


class FolderUpdate(BaseModel):
    """Schema for updating a folder"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    parent_id: Optional[UUID] = None
    sort_order: Optional[int] = None


class FolderResponse(FolderBase):
    """Schema for folder response"""
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class FolderWithChildren(FolderResponse):
    """Schema for folder with nested children"""
    children: list["FolderWithChildren"] = []
    documents: list[DocumentResponse] = []
