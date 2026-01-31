from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials

from app.api.deps import get_auth_service, get_current_user, security
from app.services.auth_service import AuthService
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    SessionResponse
)
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


def get_client_info(request: Request):
    """Extract client information from request"""
    return {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "device_info": request.headers.get("user-agent")  # Could be parsed for better info
    }


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user account
    
    **Requirements:**
    - Email must be unique and valid
    - Password minimum 8 characters
    - Display name optional
    
    **Returns:**
    - User profile (without password)
    """
    client_info = get_client_info(request)
    return await auth_service.register(
        user_data=user_data,
        **client_info
    )


@router.post("/signin", response_model=TokenResponse)
async def signin(
    login_data: LoginRequest,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Authenticate user and create session
    
    **Returns:**
    - access_token: Short-lived JWT for API requests (15-30 min)
    - refresh_token: Long-lived token for getting new access tokens (7 days)
    - token_type: Always "bearer"
    - expires_in: Access token expiration in seconds
    
    **Usage:**
    ```
    Authorization: Bearer <access_token>
    ```
    
    **Security:**
    - Session stored in database
    - Tokens can be revoked server-side
    - Device and IP tracked for security
    """
    client_info = get_client_info(request)
    return await auth_service.login(
        email=login_data.email,
        password=login_data.password,
        **client_info
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Refresh access token using refresh token
    
    **When to use:**
    - Access token expired (401 error)
    - Proactively before expiration
    
    **Returns:**
    - New access_token and refresh_token
    - Both tokens are rotated for security
    """
    return await auth_service.refresh_access_token(refresh_data.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Logout current session
    
    **Effect:**
    - Deletes session from database
    - Access token immediately invalidated
    - Must login again to get new tokens
    """
    token = credentials.credentials
    success = await auth_service.logout(token)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return None


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all_devices(
    current_user: UserResponse = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Logout from all devices
    
    **Effect:**
    - Deletes ALL sessions for current user
    - All devices must re-authenticate
    - Useful for security incidents
    """
    count = await auth_service.logout_all_sessions(current_user.id)
    return None


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get current user profile
    
    **Protected:** Requires valid access token
    
    **Returns:**
    - User profile with all fields except password
    """
    return current_user


@router.get("/sessions", response_model=List[SessionResponse])
async def get_active_sessions(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: UserResponse = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    List all active sessions for current user
    
    **Use cases:**
    - See where you're logged in
    - Detect unauthorized access
    - Manage device sessions
    
    **Returns:**
    - List of active sessions with device info
    - Current session marked with is_current=True
    """
    sessions = await auth_service.get_active_sessions(current_user.id)
    current_token = credentials.credentials
    
    session_responses = []
    for session in sessions:
        is_current = session.access_token == current_token
        session_responses.append(
            SessionResponse(
                id=session.id,
                device_info=session.device_info,
                ip_address=session.ip_address,
                created_at=session.created_at,
                expires_at=session.expires_at,
                is_current=is_current
            )
        )
    
    return session_responses
