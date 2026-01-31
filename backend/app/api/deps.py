from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.document_repository import DocumentRepository, FolderRepository
from app.repositories.user_repository import UserRepository
from app.repositories.session_repository import SessionRepository
from app.services.document_service import DocumentService, FolderService
from app.services.auth_service import AuthService
from app.schemas.user import UserResponse


# ============== Security ==============

security = HTTPBearer()


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


def get_user_repository(
    db: AsyncSession = Depends(get_db)
) -> UserRepository:
    """Get UserRepository instance"""
    return UserRepository(db)


def get_session_repository(
    db: AsyncSession = Depends(get_db)
) -> SessionRepository:
    """Get SessionRepository instance"""
    return SessionRepository(db)


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


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    session_repo: SessionRepository = Depends(get_session_repository)
) -> AuthService:
    """Get AuthService instance"""
    return AuthService(user_repo, session_repo)


# ============== Auth Dependencies ==============

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """
    Get current authenticated user from JWT token
    
    Validates:
    - Token signature
    - Token expiration
    - Session exists in database
    - User is active
    """
    try:
        token = credentials.credentials
        user = await auth_service.get_current_user_from_token(token)
        return UserResponse.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

