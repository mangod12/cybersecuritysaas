"""
Authentication router for user registration, login, and JWT token management.
Handles user authentication, password hashing, and JWT token creation/validation.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from backend.database.db import get_async_db
from backend.models.user import User, UserCreate, UserResponse, Token, GitHubUserCreate
from backend.services.auth_service import (
    create_access_token,
    verify_password,
    get_password_hash,
    verify_token
)
from backend.services.github_auth_service import github_auth_service
from backend.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify token and get email
    email = verify_token(token)
    if email is None:
        raise credentials_exception
    
    # Get user from database
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Register a new user."""
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        company=user_data.company,
        is_active=True,
        is_verified=False  # Email verification would be implemented here
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    """Authenticate user and return JWT token."""
    # Get user by email
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    # Verify user and password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_active_user)):
    """Get current user profile."""
    return current_user


@router.post("/verify-token")
async def verify_user_token(current_user: User = Depends(get_active_user)):
    """Verify if the current token is valid."""
    return {"valid": True, "user_id": current_user.id, "email": current_user.email}


@router.get("/github/login")
async def github_login():
    """Get GitHub OAuth authorization URL."""
    try:
        auth_url = github_auth_service.get_authorization_url()
        return {"auth_url": auth_url}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate GitHub auth URL: {str(e)}"
        )


@router.get("/github/callback")
async def github_callback(
    code: str,
    state: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db)
):
    """Handle GitHub OAuth callback and create/login user."""
    try:
        # Exchange code for access token
        access_token = await github_auth_service.exchange_code_for_token(code)
        
        # Get user info from GitHub
        github_user_info = await github_auth_service.get_user_info(access_token)
        
        # Check if user exists by GitHub ID
        result = await db.execute(
            select(User).where(User.github_id == str(github_user_info["id"]))
        )
        user = result.scalar_one_or_none()
        
        if user:
            # User exists, update info and return token
            user.github_username = github_user_info["login"]
            user.avatar_url = github_user_info.get("avatar_url")
            user.is_verified = True
            await db.commit()
        else:
            # Check if user exists by email
            if github_user_info["email"]:
                result = await db.execute(
                    select(User).where(User.email == github_user_info["email"])
                )
                existing_user = result.scalar_one_or_none()
                
                if existing_user:
                    # Link existing email account to GitHub
                    existing_user.github_id = str(github_user_info["id"])
                    existing_user.github_username = github_user_info["login"]
                    existing_user.avatar_url = github_user_info.get("avatar_url")
                    existing_user.auth_provider = "github"
                    existing_user.is_verified = True
                    await db.commit()
                    user = existing_user
                else:
                    # Create new user
                    user = User(
                        email=github_user_info["email"],
                        github_id=str(github_user_info["id"]),
                        github_username=github_user_info["login"],
                        full_name=github_user_info.get("name"),
                        company=github_user_info.get("company"),
                        avatar_url=github_user_info.get("avatar_url"),
                        auth_provider="github",
                        is_active=True,
                        is_verified=True
                    )
                    db.add(user)
                    await db.commit()
                    await db.refresh(user)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="GitHub account has no verified email address"
                )
        
        # Create JWT token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        jwt_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "github_username": user.github_username,
                "avatar_url": user.avatar_url
            }
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"GitHub OAuth error: {str(e)}"
        )