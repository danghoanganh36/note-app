from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


# Login request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Token response (after login/refresh)
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until expiration


# Token refresh request
class RefreshTokenRequest(BaseModel):
    refresh_token: str


# Session info response
class SessionResponse(BaseModel):
    id: UUID
    device_info: Optional[str]
    ip_address: Optional[str]
    created_at: datetime
    expires_at: datetime
    is_current: bool = False
    
    class Config:
        from_attributes = True


# Password reset request
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# Password reset (with token)
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


# Change password (authenticated)
class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
