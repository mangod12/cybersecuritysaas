# GitHub OAuth Setup Guide

This guide will help you set up GitHub OAuth authentication for the CyberSec Alert SaaS application.

## Prerequisites

- A GitHub account
- The application running locally on `http://localhost:8001`

## Step 1: Create a GitHub OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in the application details:
   - **Application name**: `CyberSec Alert SaaS` (or any name you prefer)
   - **Homepage URL**: `http://localhost:8001`
   - **Application description**: `Cybersecurity vulnerability monitoring dashboard`
   - **Authorization callback URL**: `http://localhost:8001/api/v1/auth/github/callback`

4. Click "Register application"
5. Note down your **Client ID** and **Client Secret**

## Step 2: Configure Environment Variables

Create or update your `.env` file in the project root with the GitHub OAuth credentials:

```env
# GitHub OAuth Configuration
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here
GITHUB_REDIRECT_URI=http://localhost:8001/api/v1/auth/github/callback
```

## Step 3: Restart the Application

After adding the environment variables, restart your application:

```bash
# Stop the current server (Ctrl+C)
# Then restart it
python scripts/start_server.py
# or
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

## Step 4: Test the Integration

1. Open your browser and go to `http://localhost:8001`
2. Click the "Login with GitHub" button
3. You should be redirected to GitHub for authorization
4. After authorizing, you'll be redirected back to the application
5. You should be logged in and see the dashboard

## How It Works

### OAuth Flow

1. **User clicks "Login with GitHub"** → Frontend calls `/api/v1/auth/github/login`
2. **Backend generates auth URL** → Returns GitHub authorization URL
3. **User redirected to GitHub** → User authorizes the application
4. **GitHub redirects back** → With authorization code
5. **Backend exchanges code for token** → Gets GitHub access token
6. **Backend gets user info** → Fetches user profile from GitHub
7. **User created/logged in** → Creates new user or links existing account
8. **JWT token returned** → User is authenticated

### User Management

- **New users**: Automatically created with GitHub profile information
- **Existing users**: If a user with the same email exists, the GitHub account is linked
- **Verified accounts**: GitHub users are automatically marked as verified
- **Profile data**: Name, email, company, and avatar are imported from GitHub

## Security Features

- **CSRF protection**: State parameter support (can be enhanced)
- **Secure token exchange**: Server-side code exchange
- **Email verification**: Only users with verified GitHub emails can login
- **Account linking**: Existing email accounts can be linked to GitHub

## Troubleshooting

### Common Issues

1. **"GitHub OAuth not configured"**
   - Make sure you've set the environment variables
   - Restart the application after setting them

2. **"Invalid redirect URI"**
   - Ensure the callback URL in GitHub matches exactly: `http://localhost:8001/api/v1/auth/github/callback`

3. **"GitHub account has no verified email address"**
   - The user must have a verified email address on their GitHub account
   - They need to verify their email in GitHub settings

4. **"Failed to exchange code for token"**
   - Check that your Client ID and Client Secret are correct
   - Ensure the redirect URI matches exactly

### Debug Mode

To enable debug logging, set in your `.env`:

```env
DEBUG=true
```

## Production Deployment

For production deployment:

1. **Update callback URL**: Change to your production domain
2. **Use HTTPS**: GitHub requires HTTPS for production OAuth apps
3. **Secure secrets**: Store Client Secret securely (use environment variables)
4. **Rate limiting**: Be aware of GitHub API rate limits
5. **Error handling**: Implement proper error handling for OAuth failures

### Example Production Configuration

```env
GITHUB_CLIENT_ID=your_production_client_id
GITHUB_CLIENT_SECRET=your_production_client_secret
GITHUB_REDIRECT_URI=https://yourdomain.com/api/v1/auth/github/callback
```

## API Endpoints

- `GET /api/v1/auth/github/login` - Get GitHub authorization URL
- `GET /api/v1/auth/github/callback` - Handle OAuth callback

## Database Schema

The following fields are added to the User model:

- `github_id` - GitHub user ID (unique)
- `github_username` - GitHub username
- `avatar_url` - GitHub profile picture URL
- `auth_provider` - Authentication provider ("email" or "github")
- `hashed_password` - Now nullable (for OAuth users)

## Support

If you encounter issues:

1. Check the application logs for detailed error messages
2. Verify your GitHub OAuth app configuration
3. Ensure all environment variables are set correctly
4. Test with a GitHub account that has a verified email address 