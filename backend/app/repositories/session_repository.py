from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserSession


class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(
        self,
        user_id: UUID,
        access_token: str,
        refresh_token: str,
        expires_at: datetime,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> UserSession:
        """Create a new user session"""
        session = UserSession(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            device_info=device_info,
            ip_address=ip_address,
            user_agent=user_agent
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_session_by_access_token(self, access_token: str) -> Optional[UserSession]:
        """Get session by access token"""
        result = await self.db.execute(
            select(UserSession).where(UserSession.access_token == access_token)
        )
        return result.scalar_one_or_none()

    async def get_session_by_refresh_token(self, refresh_token: str) -> Optional[UserSession]:
        """Get session by refresh token"""
        result = await self.db.execute(
            select(UserSession).where(UserSession.refresh_token == refresh_token)
        )
        return result.scalar_one_or_none()

    async def get_active_sessions_by_user(self, user_id: UUID) -> List[UserSession]:
        """Get all active sessions for a user (not expired)"""
        now = datetime.now(timezone.utc)
        result = await self.db.execute(
            select(UserSession)
            .where(UserSession.user_id == user_id)
            .where(UserSession.expires_at > now)
            .order_by(UserSession.created_at.desc())
        )
        return list(result.scalars().all())

    async def update_session_tokens(
        self,
        session_id: UUID,
        new_access_token: str,
        new_refresh_token: str,
        new_expires_at: datetime
    ) -> Optional[UserSession]:
        """Update session tokens (for token refresh)"""
        session = await self.db.get(UserSession, session_id)
        if session:
            session.access_token = new_access_token
            session.refresh_token = new_refresh_token
            session.expires_at = new_expires_at
            await self.db.commit()
            await self.db.refresh(session)
        return session

    async def delete_session(self, session_id: UUID) -> bool:
        """Delete a specific session (logout)"""
        result = await self.db.execute(
            delete(UserSession).where(UserSession.id == session_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def delete_session_by_access_token(self, access_token: str) -> bool:
        """Delete session by access token"""
        result = await self.db.execute(
            delete(UserSession).where(UserSession.access_token == access_token)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def delete_all_user_sessions(self, user_id: UUID) -> int:
        """Delete all sessions for a user (logout all devices)"""
        result = await self.db.execute(
            delete(UserSession).where(UserSession.user_id == user_id)
        )
        await self.db.commit()
        return result.rowcount

    async def delete_expired_sessions(self) -> int:
        """Delete all expired sessions (cleanup task)"""
        now = datetime.now(timezone.utc)
        result = await self.db.execute(
            delete(UserSession).where(UserSession.expires_at <= now)
        )
        await self.db.commit()
        return result.rowcount
