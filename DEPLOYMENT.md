# CyberSec Alert SaaS - Deployment Guide

This guide covers multiple deployment options for the CyberSec Alert SaaS application.

## 🚀 Quick Start

Use the deployment script for easy deployment:

```bash
# Local production deployment
python scripts/deploy.py local
```

## 📋 Prerequisites

### For All Deployments
- Python 3.12+
- Git

## 🏠 Local Production Deployment

### Option 1: Using Deployment Script
```bash
python scripts/deploy.py local
```

### Option 2: Manual Local Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY=your-secret-key-here
export DATABASE_URL=sqlite:///cybersec_alerts.db
# For local development, use port 8000
export GITHUB_REDIRECT_URI=http://localhost:8000/api/v1/auth/github/callback

# Initialize database
python scripts/setup_database.py

# Start production server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🔧 Environment Configuration

### Required Environment Variables
```env
# Security
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///cybersec_alerts.db

# Email (optional)
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_DOMAIN=your-mailgun-domain
FROM_EMAIL=noreply@yourdomain.com

# NVD API (optional)
NVD_API_KEY=your-nvd-api-key

# GitHub OAuth (optional)
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here
# For local development (port 8000)
GITHUB_REDIRECT_URI=http://localhost:8000/api/v1/auth/github/callback
```

### Optional Environment Variables
```env
# Application
APP_NAME=CyberSec Alert SaaS
APP_VERSION=1.0.0
DEBUG=false

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000", "https://yourdomain.com"]

# Scraper settings
SCRAPER_INTERVAL_HOURS=6
```

## 📊 Database Setup

### SQLite (Default)
- Automatically created on first run
- Good for development and small deployments

### PostgreSQL (Production)
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb cybersec_alerts
sudo -u postgres createuser cybersec_user

# Set password
sudo -u postgres psql
ALTER USER cybersec_user PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE cybersec_alerts TO cybersec_user;
\q

# Update DATABASE_URL
export DATABASE_URL=postgresql://cybersec_user:your-password@localhost:5432/cybersec_alerts
```

## 🔒 Security Configuration

### Generate Secret Key
```python
import secrets
print(secrets.token_hex(32))
```

### SSL/TLS Setup (Production)
```bash
# Generate SSL certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Update nginx.conf with SSL configuration
# Uncomment HTTPS server block in nginx.conf
```

## 📈 Monitoring and Logging

### Health Checks
- **Application**: `GET /health`
- **Database**: Check connection status
- **Scheduler**: Verify job execution

### Logs
```bash
# Docker logs
docker-compose logs -f app

# Heroku logs
heroku logs --tail

# Local logs
tail -f logs/app.log
```

## 🔄 Updates and Maintenance

### Docker Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

### Heroku Updates
```bash
# Deploy updates
git add .
git commit -m "Update application"
git push heroku main
```

### Database Migrations
```bash
# Run migrations (if using Alembic)
alembic upgrade head

# Or recreate database
python scripts/setup_database.py
```

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
lsof -i :8000
# Kill process
kill -9 <PID>
```

#### Database Connection Issues
```bash
# Check database status
docker-compose ps db
# Restart database
docker-compose restart db
```

#### Permission Issues
```bash
# Fix file permissions
chmod +x scripts/deploy.py
chmod +x scripts/start_server.py
```

#### GitHub OAuth Issues
- Ensure the callback URL in your GitHub OAuth App matches your deployment
- For local development: `http://localhost:8000/api/v1/auth/github/callback`
- For Docker: `http://localhost:8001/api/v1/auth/github/callback`
- For production: `https://yourdomain.com/api/v1/auth/github/callback`

### Debug Mode
```bash
# Enable debug logging
export DEBUG=true
python scripts/start_server.py
```

## 📞 Support

For deployment issues:
1. Check the logs for error messages
2. Verify environment variables are set correctly
3. Ensure all prerequisites are installed
4. Check network connectivity and firewall settings

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)