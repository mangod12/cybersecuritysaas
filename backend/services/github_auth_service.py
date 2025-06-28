"""
GitHub OAuth authentication service.

This module handles GitHub OAuth authentication flow, including:
- Generating authorization URLs
- Exchanging authorization codes for access tokens
- Fetching user information from GitHub
"""

import requests
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from backend.config import settings


class GitHubAuthService:
    """Service for handling GitHub OAuth authentication."""
    
    def __init__(self):
        self.client_id = settings.github_client_id
        self.client_secret = settings.github_client_secret
        self.redirect_uri = settings.github_redirect_uri
        self.github_api_base = "https://api.github.com"
        self.github_auth_base = "https://github.com"
    
    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """
        Generate GitHub OAuth authorization URL.
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            GitHub authorization URL
        """
        if not self.client_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GitHub OAuth not configured"
            )
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "read:user user:email",
            "response_type": "code"
        }
        
        if state:
            params["state"] = state
            
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.github_auth_base}/login/oauth/authorize?{query_string}"
    
    async def exchange_code_for_token(self, code: str) -> str:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from GitHub
            
        Returns:
            GitHub access token
        """
        if not self.client_id or not self.client_secret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GitHub OAuth not configured"
            )
        
        token_url = f"{self.github_auth_base}/login/oauth/access_token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        
        headers = {
            "Accept": "application/json"
        }
        
        try:
            response = requests.post(token_url, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            
            if "error" in token_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"GitHub OAuth error: {token_data.get('error_description', token_data['error'])}"
                )
            
            access_token = token_data.get("access_token")
            if not access_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No access token received from GitHub"
                )
            
            return access_token
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to exchange code for token: {str(e)}"
            )
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        Get user information from GitHub using access token.
        
        Args:
            access_token: GitHub access token
            
        Returns:
            User information dictionary
        """
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            # Get user profile
            user_response = requests.get(f"{self.github_api_base}/user", headers=headers)
            user_response.raise_for_status()
            user_data = user_response.json()
            
            # Get user emails
            emails_response = requests.get(f"{self.github_api_base}/user/emails", headers=headers)
            emails_response.raise_for_status()
            emails_data = emails_response.json()
            
            # Find primary email
            primary_email = None
            for email in emails_data:
                if email.get("primary") and email.get("verified"):
                    primary_email = email["email"]
                    break
            
            # If no primary email found, use the first verified email
            if not primary_email:
                for email in emails_data:
                    if email.get("verified"):
                        primary_email = email["email"]
                        break
            
            # If still no email, use the email from user profile
            if not primary_email:
                primary_email = user_data.get("email")
            
            return {
                "id": user_data["id"],
                "login": user_data["login"],
                "email": primary_email,
                "name": user_data.get("name"),
                "avatar_url": user_data.get("avatar_url"),
                "company": user_data.get("company"),
                "location": user_data.get("location"),
                "bio": user_data.get("bio")
            }
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get user info from GitHub: {str(e)}"
            )


# Global instance
github_auth_service = GitHubAuthService() 