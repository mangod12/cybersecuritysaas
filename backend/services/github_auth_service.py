"""
GitHub OAuth authentication service.

This module provides GitHub OAuth integration for user authentication.
It handles the OAuth flow including authorization URL generation,
token exchange, and user information retrieval.
"""

import httpx
from typing import Optional, Dict, Any
from fastapi import HTTPException, Request
from backend.config import settings
from backend.services.auth_service import create_access_token
from backend.models.user import User
from backend.database.db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

class GitHubAuthService:
    """Service for handling GitHub OAuth authentication."""
    
    def __init__(self):
        self.client_id = settings.github_client_id
        self.client_secret = settings.github_client_secret
        self.redirect_uri = settings.github_redirect_uri
        
        if not self.client_id or not self.client_secret:
            logger.warning("GitHub OAuth credentials not configured")
    
    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """
        Generate GitHub OAuth authorization URL.
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            GitHub authorization URL
        """
        if not self.client_id:
            raise ValueError("GitHub client ID not configured")
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "read:user user:email",
            "response_type": "code"
        }
        
        if state:
            params["state"] = state
            
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://github.com/login/oauth/authorize?{query_string}"
    
    async def exchange_code_for_token(self, code: str, session_state: str, state: str) -> Optional[str]:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from GitHub
            session_state: State from the user's session
            state: State from the GitHub callback
            
        Returns:
            Access token or None if exchange failed
        """
        print(f"GitHub callback initiated. Received state: {state}, session state: {session_state}")

        if not state or state != session_state:
            print("Error: State mismatch in GitHub callback.")
            raise HTTPException(status_code=400, detail="Invalid state")

        if not self.client_id or not self.client_secret:
            raise ValueError("GitHub OAuth credentials not configured")
        
        print(f"Requesting access token from GitHub with code: {code}")
        async with httpx.AsyncClient() as client:
            headers = {"Accept": "application/json"}
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": self.redirect_uri,
            }
            print(f"Sending data to GitHub: {data}")
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers=headers,
                json=data,
            )
            print(f"GitHub response status code: {response.status_code}")
            print(f"GitHub response content: {response.text}")

            if response.status_code != 200:
                print(f"Error fetching access token from GitHub: {response.text}")
                raise HTTPException(status_code=400, detail="Could not fetch access token from GitHub")

            response_data = response.json()
            print(f"GitHub response data: {response_data}")
            access_token = response_data.get("access_token")

            if not access_token:
                print("Error: No access token received from GitHub.")
                raise HTTPException(status_code=400, detail="No access token received from GitHub")
            
            return access_token
    
    async def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get user information from GitHub using access token.
        
        Args:
            access_token: GitHub access token
            
        Returns:
            User information dictionary or None if failed
        """
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"token {access_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            # Get user profile
            response = await client.get("https://api.github.com/user", headers=headers)
            if response.status_code != 200:
                logger.error(f"Failed to get user info: {response.text}")
                print(f"Failed to get user info: {response.text}")
                return None
            user_data = response.json()
            # Get user emails
            email_response = await client.get("https://api.github.com/user/emails", headers=headers)
            if email_response.status_code == 200:
                emails = email_response.json()
                primary_email = next((email["email"] for email in emails if email["primary"]), None)
                if primary_email:
                    user_data["email"] = primary_email
            return user_data
    
    async def authenticate_user(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Complete GitHub OAuth authentication flow.
        
        Args:
            code: Authorization code from GitHub
            
        Returns:
            Authentication result with user info and JWT token
        """
        try:
            # Exchange code for token
            access_token = await self.exchange_code_for_token(code)
            if not access_token:
                print("No access token received from GitHub.")
                return None
            # Get user information
            user_info = await self.get_user_info(access_token)
            if not user_info:
                print("No user info received from GitHub.")
                return None
            # Get or create user
            async with AsyncSessionLocal() as session:
                user = await self._get_or_create_user(session, user_info)
                if not user:
                    print("Failed to get or create user from GitHub info.")
                    return None
                
                # Generate JWT token
                token_data = {
                    "sub": user.email,
                    "is_active": user.is_active
                }
                
                jwt_token = create_access_token(token_data)
                
                return {
                    "access_token": jwt_token,
                    "token_type": "bearer",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "is_active": user.is_active
                    }
                }
                
        except Exception as e:
            logger.error(f"GitHub authentication failed: {e}")
            print(f"GitHub authentication failed: {e}")
            return None
    
    async def _get_or_create_user(self, session: AsyncSession, user_info: Dict[str, Any]) -> Optional[User]:
        """
        Get existing user or create new user from GitHub info.
        
        Args:
            session: Database session
            user_info: GitHub user information
            
        Returns:
            User object or None if creation failed
        """
        email = user_info.get("email")
        if not email:
            logger.error("No email found in GitHub user info")
            print("No email found in GitHub user info")
            return None
        
        # Check if user exists
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if user:
            # Update user info if needed
            if not user.name and user_info.get("name"):
                user.name = user_info["name"]
            await session.commit()
            return user
        
        # Create new user
        try:
            user = User(
                email=email,
                name=user_info.get("name", ""),
                is_active=True,
                is_verified=True  # GitHub users are considered verified
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            print(f"Failed to create user: {e}")
            await session.rollback()
            return None

# Global instance
github_auth_service = GitHubAuthService()

async def github_callback(code: str, state: str):
    """
    GitHub OAuth2 callback endpoint.
    
    Args:
        code: Authorization code received from GitHub
        state: CSRF protection state parameter
    
    Returns:
        Redirect response or error message
    """
    print(f"GitHub callback initiated. Received state: {state}, session state: {session_state}")

    if not state or state != session_state:
        print("Error: State mismatch in GitHub callback.")
        raise HTTPException(status_code=400, detail="Invalid state")

    print(f"Requesting access token from GitHub with code: {code}")
    async with httpx.AsyncClient() as client:
        headers = {"Accept": "application/json"}
        data = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_REDIRECT_URI,
        }
        print(f"Sending data to GitHub: {data}")
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers=headers,
            json=data,
        )
        print(f"GitHub response status code: {response.status_code}")
        print(f"GitHub response content: {response.text}")

        if response.status_code != 200:
            print(f"Error fetching access token from GitHub: {response.text}")
            raise HTTPException(status_code=400, detail="Could not fetch access token from GitHub")

        response_data = response.json()
        print(f"GitHub response data: {response_data}")
        access_token = response_data.get("access_token")

        if not access_token:
            print("Error: No access token received from GitHub.")
            raise HTTPException(status_code=400, detail="No access token received from GitHub")

        # Proceed with user authentication
        result = await github_auth_service.authenticate_user(access_token)
        if not result:
            print("Error: User authentication failed.")
            raise HTTPException(status_code=400, detail="User authentication failed")

        # Successful authentication, redirect or respond with user info
        print("GitHub authentication successful")
        return result