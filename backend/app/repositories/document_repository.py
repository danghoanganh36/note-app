from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from typing import Optional, List
from uuid import UUID

from app.models.document import Document, DocumentVersion
from app.models.folder import Folder
from app.schemas.document import DocumentCreate, DocumentUpdate


class DocumentRepository:
    """Repository for Document database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ============== Document CRUD ==============
    
    async def create(self, doc: DocumentCreate, owner_id: UUID) -> Document:
        """Create a new document"""
        new_doc = Document(
            **doc.model_dump(exclude_unset=True),
            owner_id=owner_id
        )
        self.db.add(new_doc)
        await self.db.commit()
        await self.db.refresh(new_doc)
        return new_doc
    
    async def get_by_id(
        self,
        doc_id: UUID,
        include_versions: bool = False
    ) -> Optional[Document]:
        """Get document by ID"""
        query = select(Document).where(
            and_(
                Document.id == doc_id,
                Document.deleted_at.is_(None)
            )
        )
        
        if include_versions:
            query = query.options(selectinload(Document.versions))
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_owner(
        self,
        owner_id: UUID,
        folder_id: Optional[UUID] = None,
        category: Optional[str] = None,
        search: Optional[str] = None,
        pinned_only: bool = False,
        skip: int = 0,
        limit: int = 50
    ) -> List[Document]:
        """Get documents by owner with filters"""
        query = select(Document).where(
            and_(
                Document.owner_id == owner_id,
                Document.deleted_at.is_(None)
            )
        )
        
        if folder_id is not None:
            query = query.where(Document.folder_id == folder_id)
        
        if category:
            query = query.where(Document.category == category)
        
        if pinned_only:
            query = query.where(Document.is_pinned == True)
        
        if search:
            search_filter = or_(
                Document.title.ilike(f"%{search}%"),
                Document.content.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        query = query.order_by(Document.updated_at.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def update(self, doc_id: UUID, doc_update: DocumentUpdate) -> Optional[Document]:
        """Update document"""
        document = await self.get_by_id(doc_id)
        if not document:
            return None
        
        update_data = doc_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(document, field, value)
        
        await self.db.commit()
        await self.db.refresh(document)
        return document
    
    async def soft_delete(self, doc_id: UUID) -> bool:
        """Soft delete document"""
        document = await self.get_by_id(doc_id)
        if not document:
            return False
        
        document.soft_delete()
        await self.db.commit()
        return True
    
    async def permanent_delete(self, doc_id: UUID) -> bool:
        """Permanently delete document"""
        document = await self.get_by_id(doc_id)
        if not document:
            return False
        
        await self.db.delete(document)
        await self.db.commit()
        return True
    
    # ============== Version Management ==============
    
    async def create_version(
        self,
        doc_id: UUID,
        content: str,
        version: int,
        changed_by: UUID,
        change_summary: Optional[str] = None
    ) -> DocumentVersion:
        """Create a version snapshot"""
        version = DocumentVersion(
            document_id=doc_id,
            content=content,
            version=version,
            changed_by=changed_by,
            change_summary=change_summary
        )
        self.db.add(version)
        await self.db.commit()
        await self.db.refresh(version)
        return version
    
    async def get_versions(self, doc_id: UUID) -> List[DocumentVersion]:
        """Get all versions of a document"""
        result = await self.db.execute(
            select(DocumentVersion)
            .where(DocumentVersion.document_id == doc_id)
            .order_by(DocumentVersion.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def get_version_by_id(self, version_id: UUID) -> Optional[DocumentVersion]:
        """Get specific version"""
        result = await self.db.execute(
            select(DocumentVersion).where(DocumentVersion.id == version_id)
        )
        return result.scalar_one_or_none()
    
    # ============== Statistics ==============
    
    async def count_by_owner(self, owner_id: UUID) -> int:
        """Count documents by owner"""
        result = await self.db.execute(
            select(func.count(Document.id)).where(
                and_(
                    Document.owner_id == owner_id,
                    Document.deleted_at.is_(None)
                )
            )
        )
        return result.scalar() or 0


class FolderRepository:
    """Repository for Folder database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, name: str, owner_id: UUID, parent_id: Optional[UUID] = None) -> Folder:
        """Create a new folder"""
        folder = Folder(name=name, owner_id=owner_id, parent_id=parent_id)
        self.db.add(folder)
        await self.db.commit()
        await self.db.refresh(folder)
        return folder
    
    async def get_by_id(self, folder_id: UUID) -> Optional[Folder]:
        """Get folder by ID"""
        result = await self.db.execute(
            select(Folder).where(Folder.id == folder_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_owner(
        self,
        owner_id: UUID,
        parent_id: Optional[UUID] = None
    ) -> List[Folder]:
        """Get folders by owner"""
        query = select(Folder).where(Folder.owner_id == owner_id)
        
        if parent_id is not None:
            query = query.where(Folder.parent_id == parent_id)
        else:
            query = query.where(Folder.parent_id.is_(None))
        
        query = query.order_by(Folder.sort_order, Folder.name)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def delete(self, folder_id: UUID) -> bool:
        """Delete folder (documents will have folder_id set to NULL)"""
        folder = await self.get_by_id(folder_id)
        if not folder:
            return False
        
        await self.db.delete(folder)
        await self.db.commit()
        return True
