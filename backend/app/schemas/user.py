from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional


# Base schema with common fields
class UserBase(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


# For user registration (includes password)
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    display_name: Optional[str] = Field(None, max_length=255)


# For user updates (all optional)
class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = None
    avatar_url: Optional[str] = Field(None, max_length=500)


# For responses (NO password, includes timestamps)
class UserResponse(UserBase):
    id: UUID
    role: str
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# For public profiles (minimal info)
class UserPublic(BaseModel):
    id: UUID
    email: EmailStr
    display_name: Optional[str]
    avatar_url: Optional[str]

    model_config = ConfigDict(from_attributes=True)