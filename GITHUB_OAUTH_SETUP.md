# GitHub OAuth Setup Guide

This guide will help you set up GitHub OAuth authentication for the CyberSec Alert SaaS application.

## Prerequisites

- A GitHub account
- Access to GitHub Developer Settings
- The CyberSec Alert SaaS application running locally or deployed

## Step 1: Create a GitHub OAuth App

1. **Go to GitHub Developer Settings**
   - Log in to your GitHub account
   - Navigate to [GitHub Developer Settings](https://github.com/settings/developers)
   - Click on "OAuth Apps" in the left sidebar
   - Click "New OAuth App"

2. **Fill in the OAuth App Details**
   ```
   Application name: CyberSec Alert SaaS
   Homepage URL: http://localhost:8001 (for local development)
   Application description: Cybersecurity monitoring and alert system
   Authorization callback URL: http://localhost:8001/api/v1/auth/github/callback
   ```

3. **Register the Application**
   - Click "Register application"
   - Note down the **Client ID** and **Client Secret**

## Step 2: Configure Environment Variables

1. **Create or update your `.env` file**
   ```env
   # GitHub OAuth Configuration
   GITHUB_CLIENT_ID=your_github_client_id_here
   GITHUB_CLIENT_SECRET=your_github_client_secret_here
   GITHUB_REDIRECT_URI=http://localhost:8001/api/v1/auth/github/callback
   
   # Other required settings
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///./cybersec_alerts.db
   ```

2. **For Production Deployment**
   ```env
   # Update these URLs for your production domain
   GITHUB_REDIRECT_URI=https://yourdomain.com/api/v1/auth/github/callback
   ```

## Step 3: Update GitHub OAuth App for Production

If deploying to production, update your GitHub OAuth App settings:

1. **Go back to GitHub Developer Settings**
2. **Edit your OAuth App**
3. **Update the URLs:**
   ```
   Homepage URL: https://yourdomain.com
   Authorization callback URL: https://yourdomain.com/api/v1/auth/github/callback
   ```

## Step 4: Test the Integration

1. **Start the application**
   ```bash
   python scripts/start_server.py
   ```

2. **Navigate to the login page**
   - Go to `http://localhost:8001`
   - You should see the login form with a "Continue with GitHub" button

3. **Test GitHub login**
   - Click "Continue with GitHub"
   - You should be redirected to GitHub for authorization
   - After authorizing, you should be redirected back and logged in

## Step 5: Troubleshooting

### Common Issues

1. **"GitHub OAuth not configured" error**
   - Check that `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` are set in your `.env` file
   - Restart the application after updating environment variables

2. **"Redirect URI mismatch" error**
   - Ensure the callback URL in your GitHub OAuth App matches exactly
   - Check for trailing slashes or protocol mismatches

3. **"Invalid client" error**
   - Verify your Client ID and Client Secret are correct
   - Make sure you copied them from the right OAuth App

4. **"No email found" error**
   - GitHub users must have a verified email address
   - The user must grant email access permissions

### Debug Mode

Enable debug logging by setting:
```env
DEBUG=true
```

## Security Considerations

1. **Keep Client Secret Secure**
   - Never commit your Client Secret to version control
   - Use environment variables or secure secret management

2. **Use HTTPS in Production**
   - Always use HTTPS for production deployments
   - Update callback URLs accordingly

3. **Scope Permissions**
   - The app requests minimal permissions: `read:user` and `user:email`
   - Only reads basic profile information and email

## API Endpoints

The GitHub OAuth integration provides these endpoints:

- `GET /api/v1/auth/github/login` - Get GitHub authorization URL
- `GET /api/v1/auth/github/callback` - Handle OAuth callback

## User Flow

1. User clicks "Continue with GitHub"
2. User is redirected to GitHub for authorization
3. User authorizes the application
4. GitHub redirects back with an authorization code
5. Application exchanges code for access token
6. Application fetches user information from GitHub
7. User is created or logged in automatically
8. User is redirected to the dashboard

## Support

If you encounter issues:

1. Check the application logs for detailed error messages
2. Verify all environment variables are set correctly
3. Ensure your GitHub OAuth App settings match your deployment
4. Test with a fresh GitHub account to rule out permission issues

## Next Steps

After successful setup:

1. **Customize the UI** - Modify the login page styling
2. **Add User Management** - Implement user profile management
3. **Set up Email Notifications** - Configure email alerts for new users
4. **Monitor Usage** - Track OAuth usage and user registrations 