from typing import Generator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.document_repository import DocumentRepository, FolderRepository
from app.services.document_service import DocumentService, FolderService


# ============== Repository Dependencies ==============

def get_document_repository(
    db: AsyncSession = Depends(get_db)
) -> DocumentRepository:
    """Get DocumentRepository instance"""
    return DocumentRepository(db)


def get_folder_repository(
    db: AsyncSession = Depends(get_db)
) -> FolderRepository:
    """Get FolderRepository instance"""
    return FolderRepository(db)


# ============== Service Dependencies ==============

def get_document_service(
    doc_repo: DocumentRepository = Depends(get_document_repository),
    folder_repo: FolderRepository = Depends(get_folder_repository)
) -> DocumentService:
    """Get DocumentService instance"""
    return DocumentService(doc_repo, folder_repo)


def get_folder_service(
    folder_repo: FolderRepository = Depends(get_folder_repository)
) -> FolderService:
    """Get FolderService instance"""
    return FolderService(folder_repo)


# ============== Auth Dependencies (Placeholder) ==============
# TODO: Implement after User model is ready

from uuid import UUID

async def get_current_user() -> UUID:
    """
    Get current authenticated user
    
    TODO: Implement actual JWT authentication
    For now, returns a mock user ID for testing
    """
    # Mock user ID for development
    return UUID("00000000-0000-0000-0000-000000000001")
