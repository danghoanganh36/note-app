from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from uuid import UUID

from app.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentDetail,
    DocumentVersionResponse,
    FolderCreate,
    FolderResponse
)
from app.services.document_service import DocumentService, FolderService
from app.api.deps import get_document_service, get_folder_service, get_current_user

router = APIRouter()


# ============== Document Endpoints ==============

@router.post(
    "/",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Documents"],
    summary="Create a new document"
)
async def create_document(
    document: DocumentCreate,
    current_user: UUID = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
):
    """
    Create a new document.
    
    - **title**: Document title (required, 1-255 characters)
    - **description**: Optional description
    - **content**: Document content (Markdown supported)
    - **category**: Optional category for organization
    - **folder_id**: Optional parent folder UUID
    - **is_pinned**: Pin to top of list
    """
    return await service.create_document(document, current_user)


@router.get(
    "/",
    response_model=List[DocumentResponse],
    tags=["Documents"],
    summary="List documents"
)
async def list_documents(
    folder_id: Optional[UUID] = Query(None, description="Filter by folder"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in title and content"),
    pinned_only: bool = Query(False, description="Show only pinned documents"),
    skip: int = Query(0, ge=0, description="Number of documents to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum documents to return"),
    current_user: UUID = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
):
    """
    List user's documents with optional filters.
    
    Supports:
    - Folder filtering
    - Category filtering
    - Full-text search
    - Pinned documents only
    - Pagination
    """
    return await service.list_documents(
        user_id=current_user,
        folder_id=folder_id,
        category=category,
        search=search,
        pinned_only=pinned_only,
        skip=skip,
        limit=limit
    )


@router.get(
    "/{document_id}",
    response_model=DocumentDetail,
    tags=["Documents"],
    summary="Get document by ID"
)
async def get_document(
    document_id: UUID,
    current_user: UUID = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
):
    """
    Get a specific document with full details.
    
    Returns document with:
    - Full content
    - Version history
    - Metadata
    """
    return await service.get_document(document_id, current_user, include_versions=True)


@router.put(
    "/{document_id}",
    response_model=DocumentResponse,
    tags=["Documents"],
    summary="Update document"
)
async def update_document(
    document_id: UUID,
    document_update: DocumentUpdate,
    save_version: bool = Query(False, description="Save current state as version"),
    current_user: UUID = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
):
    """
    Update an existing document.
    
    - **save_version**: If true, saves current state before updating
    - All fields are optional - only provided fields will be updated
    """
    return await service.update_document(
        doc_id=document_id,
        doc_update=document_update,
        user_id=current_user,
        save_version=save_version
    )


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Documents"],
    summary="Delete document"
)
async def delete_document(
    document_id: UUID,
    permanent: bool = Query(False, description="Permanently delete (cannot be recovered)"),
    current_user: UUID = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
):
    """
    Delete a document.
    
    - **permanent=false**: Soft delete (recoverable for 30 days)
    - **permanent=true**: Permanent delete (cannot be recovered)
    """
    await service.delete_document(document_id, current_user, permanent)
    return None


# ============== Version Endpoints ==============

@router.get(
    "/{document_id}/versions",
    response_model=List[DocumentVersionResponse],
    tags=["Documents"],
    summary="Get document version history"
)
async def get_document_versions(
    document_id: UUID,
    current_user: UUID = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
):
    """
    Get version history for a document.
    
    Returns all saved versions ordered by creation date (newest first).
    """
    return await service.get_versions(document_id, current_user)


@router.post(
    "/{document_id}/restore/{version_id}",
    response_model=DocumentResponse,
    tags=["Documents"],
    summary="Restore document to previous version"
)
async def restore_document_version(
    document_id: UUID,
    version_id: UUID,
    current_user: UUID = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
):
    """
    Restore document to a previous version.
    
    Current state will be saved as a version before restoring.
    """
    return await service.restore_version(document_id, version_id, current_user)


# ============== Folder Endpoints ==============

@router.post(
    "/folders",
    response_model=FolderResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Folders"],
    summary="Create a new folder"
)
async def create_folder(
    folder: FolderCreate,
    current_user: UUID = Depends(get_current_user),
    service: FolderService = Depends(get_folder_service)
):
    """
    Create a new folder for organizing documents.
    
    - **name**: Folder name (required)
    - **parent_id**: Optional parent folder for nested structure
    """
    return await service.create_folder(folder, current_user)


@router.get(
    "/folders",
    response_model=List[FolderResponse],
    tags=["Folders"],
    summary="List folders"
)
async def list_folders(
    parent_id: Optional[UUID] = Query(None, description="Filter by parent folder"),
    current_user: UUID = Depends(get_current_user),
    service: FolderService = Depends(get_folder_service)
):
    """
    List user's folders.
    
    - Without parent_id: Returns root-level folders
    - With parent_id: Returns child folders
    """
    return await service.list_folders(current_user, parent_id)


@router.delete(
    "/folders/{folder_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Folders"],
    summary="Delete folder"
)
async def delete_folder(
    folder_id: UUID,
    current_user: UUID = Depends(get_current_user),
    service: FolderService = Depends(get_folder_service)
):
    """
    Delete a folder.
    
    Documents in the folder will have their folder_id set to NULL.
    """
    await service.delete_folder(folder_id, current_user)
    return None