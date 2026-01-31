from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email (for login)"""
        result = await self.db.execute(
            select(User).where(User.email == email, User.is_active == True)
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(
            select(User).where(User.id == user_id, User.is_active == True)
        )
        return result.scalar_one_or_none()

    async def create_user(self, email: str, hashed_password: str, display_name: Optional[str] = None) -> User:
        """Create a new user"""

        if email is None:
            raise ValueError("Email must be provided.")

        if await self.get_user_by_email(email) is not None:
            raise ValueError("A user with this email already exists.")

        new_user = User(
            email=email,
            password_hash=hashed_password,
            display_name=display_name
        )
        self.db.add(new_user)
        try:
            await self.db.commit()
            await self.db.refresh(new_user)
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("A user with this email already exists.")

        return new_user

    async def update_user_last_login(self, user_id: UUID) -> None:
        """Update the last login timestamp for a user"""
        if user_id is None:
            raise ValueError("User ID must be provided.")
        try:
            # Strip timezone info to match TIMESTAMP WITHOUT TIME ZONE column
            await self.db.execute(update(User).where(User.id == user_id).values(last_login=datetime.now(timezone.utc).replace(tzinfo=None)))
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("Failed to update last login timestamp.")

    async def delete_user(self, user_id: UUID) -> None:
        """Soft delete a user by setting is_active to False"""
        if user_id is None:
            raise ValueError("User ID must be provided.")
        try:
            await self.db.execute(update(User).where(User.id == user_id).values(is_active=False))
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("Failed to delete user.")

