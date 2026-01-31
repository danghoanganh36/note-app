from datetime import timedelta, datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.repositories.user_repository import UserRepository
from app.repositories.session_repository import SessionRepository
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse, UserCreate
from app.models.user import User


class AuthService:
    def __init__(self, user_repo: UserRepository, session_repo: SessionRepository):
        self.user_repo = user_repo
        self.session_repo = session_repo

    async def register(
        self,
        user_data: UserCreate,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> UserResponse:
        """Register a new user"""
        # Check if email already exists
        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = hash_password(user_data.password)

        try:
            # Create user
            user = await self.user_repo.create_user(
                email=user_data.email,
                hashed_password=hashed_password,
                display_name=user_data.display_name
            )
            return UserResponse.model_validate(user)
        except ValueError as e:
            # Handle duplicate email (raised by repository)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            import traceback
            print(f"ERROR creating user: {e}")
            print(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )

    async def login(
        self,
        email: str,
        password: str,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> TokenResponse:
        """Login user and create session"""
        # Get user by email
        user = await self.user_repo.get_user_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated"
            )

        # Update last login
        await self.user_repo.update_user_last_login(user.id)

        # Generate tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        # Calculate expiration
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        # Store session in database
        await self.session_repo.create_session(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            device_info=device_info,
            ip_address=ip_address,
            user_agent=user_agent
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token"""
        # Decode refresh token
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # Get session from database
        session = await self.session_repo.get_session_by_refresh_token(refresh_token)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session not found"
            )

        # Check if session expired
        if session.expires_at < datetime.now(timezone.utc):
            await self.session_repo.delete_session(session.id)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired"
            )

        # Get user
        user_id = UUID(payload.get("sub"))
        
        # Generate new tokens
        new_access_token = create_access_token(data={"sub": str(user_id)})
        new_refresh_token = create_refresh_token(data={"sub": str(user_id)})
        new_expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        # Update session
        await self.session_repo.update_session_tokens(
            session_id=session.id,
            new_access_token=new_access_token,
            new_refresh_token=new_refresh_token,
            new_expires_at=new_expires_at
        )

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    async def logout(self, access_token: str) -> bool:
        """Logout user by deleting session"""
        return await self.session_repo.delete_session_by_access_token(access_token)

    async def logout_all_sessions(self, user_id: UUID) -> int:
        """Logout user from all devices"""
        return await self.session_repo.delete_all_user_sessions(user_id)

    async def get_current_user_from_token(self, access_token: str) -> User:
        """Get current user from access token"""
        # Decode token
        payload = decode_token(access_token)
        if not payload or payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )

        # Verify session exists in database
        session = await self.session_repo.get_session_by_access_token(access_token)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session not found or expired"
            )

        # Check if session expired
        if session.expires_at < datetime.now(timezone.utc):
            await self.session_repo.delete_session(session.id)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired"
            )

        # Get user
        user_id = UUID(payload.get("sub"))
        user = await self.user_repo.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return user

    async def get_active_sessions(self, user_id: UUID):
        """Get all active sessions for a user"""
        return await self.session_repo.get_active_sessions_by_user(user_id)
