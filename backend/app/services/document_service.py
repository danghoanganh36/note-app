from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException, status

from app.repositories.document_repository import DocumentRepository, FolderRepository
from app.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentDetail,
    FolderCreate,
    FolderResponse
)
from app.models.document import Document
from app.models.folder import Folder


class DocumentService:
    """Service for Document business logic"""
    
    def __init__(
        self,
        doc_repo: DocumentRepository,
        folder_repo: FolderRepository
    ):
        self.doc_repo = doc_repo
        self.folder_repo = folder_repo
    
    # ============== Document Operations ==============
    
    async def create_document(
        self,
        doc: DocumentCreate,
        user_id: UUID
    ) -> Document:
        """Create a new document with validation"""
        # Validate folder ownership if folder_id provided
        if doc.folder_id:
            folder = await self.folder_repo.get_by_id(doc.folder_id)
            if not folder:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Folder not found"
                )
            if folder.owner_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have access to this folder"
                )
        
        return await self.doc_repo.create(doc, user_id)
    
    async def get_document(
        self,
        doc_id: UUID,
        user_id: UUID,
        include_versions: bool = False
    ) -> Document:
        """Get document with ownership check"""
        document = await self.doc_repo.get_by_id(doc_id, include_versions)
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Check ownership (will add sharing check later)
        if document.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this document"
            )
        
        return document
    
    async def list_documents(
        self,
        user_id: UUID,
        folder_id: Optional[UUID] = None,
        category: Optional[str] = None,
        search: Optional[str] = None,
        pinned_only: bool = False,
        skip: int = 0,
        limit: int = 50
    ) -> List[Document]:
        """List user's documents with filters"""
        return await self.doc_repo.get_by_owner(
            owner_id=user_id,
            folder_id=folder_id,
            category=category,
            search=search,
            pinned_only=pinned_only,
            skip=skip,
            limit=limit
        )
    
    async def update_document(
        self,
        doc_id: UUID,
        doc_update: DocumentUpdate,
        user_id: UUID,
        save_version: bool = False
    ) -> Document:
        """Update document with ownership check and optional version save"""
        # Check ownership
        document = await self.get_document(doc_id, user_id)
        
        # Save version if content changed
        if save_version and doc_update.content and doc_update.content != document.content:
            await self.doc_repo.create_version(
                doc_id=document.id,
                content=document.content,
                version=document.version,
                changed_by=user_id,
                change_summary="Version before update"
            )
        
        # Update document
        updated_doc = await self.doc_repo.update(doc_id, doc_update)
        
        if not updated_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        return updated_doc
    
    async def delete_document(
        self,
        doc_id: UUID,
        user_id: UUID,
        permanent: bool = False
    ) -> None:
        """Delete document (soft or permanent)"""
        # Check ownership
        await self.get_document(doc_id, user_id)
        
        if permanent:
            success = await self.doc_repo.permanent_delete(doc_id)
        else:
            success = await self.doc_repo.soft_delete(doc_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
    
    # ============== Version Operations ==============
    
    async def get_versions(self, doc_id: UUID, user_id: UUID) -> List:
        """Get document version history"""
        # Check ownership
        await self.get_document(doc_id, user_id)
        
        return await self.doc_repo.get_versions(doc_id)
    
    async def restore_version(
        self,
        doc_id: UUID,
        version_id: UUID,
        user_id: UUID
    ) -> Document:
        """Restore document to a previous version"""
        # Check ownership
        document = await self.get_document(doc_id, user_id)
        
        # Get version
        version = await self.doc_repo.get_version_by_id(version_id)
        if not version or version.document_id != doc_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Version not found"
            )
        
        # Save current state as version
        await self.doc_repo.create_version(
            doc_id=document.id,
            content=document.content,
            version=document.version,
            changed_by=user_id,
            change_summary="Before restore"
        )
        
        # Restore content
        doc_update = DocumentUpdate(content=version.content)
        document = await self.doc_repo.update(doc_id, doc_update)
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to restore version"
            )
        
        document.version += 1
        await self.doc_repo.db.commit()
        
        return document
    
    # ============== Statistics ==============
    
    async def get_document_count(self, user_id: UUID) -> int:
        """Get total document count for user"""
        return await self.doc_repo.count_by_owner(user_id)


class FolderService:
    """Service for Folder business logic"""
    
    def __init__(self, folder_repo: FolderRepository):
        self.folder_repo = folder_repo
    
    async def create_folder(
        self,
        folder: FolderCreate,
        user_id: UUID
    ) -> Folder:
        """Create a new folder with validation"""
        # Validate parent folder ownership if provided
        if folder.parent_id:
            parent = await self.folder_repo.get_by_id(folder.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent folder not found"
                )
            if parent.owner_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have access to parent folder"
                )
        
        return await self.folder_repo.create(
            name=folder.name,
            owner_id=user_id,
            parent_id=folder.parent_id
        )
    
    async def list_folders(
        self,
        user_id: UUID,
        parent_id: Optional[UUID] = None
    ) -> List[Folder]:
        """List user's folders"""
        return await self.folder_repo.get_by_owner(user_id, parent_id)
    
    async def delete_folder(
        self,
        folder_id: UUID,
        user_id: UUID
    ) -> None:
        """Delete folder with ownership check"""
        folder = await self.folder_repo.get_by_id(folder_id)
        
        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Folder not found"
            )
        
        if folder.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this folder"
            )
        
        success = await self.folder_repo.delete(folder_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Folder not found"
            )
