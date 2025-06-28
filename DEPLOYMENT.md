# 🚀 CyberSec Alert SaaS - Deployment Guide

This guide covers all deployment options for the CyberSec Alert SaaS application.

## 📋 Prerequisites

- Python 3.11+ (3.12 recommended)
- Git
- Docker & Docker Compose (for containerized deployment)
- GitHub OAuth App configured

## 🎯 Deployment Options

### Option 1: Local Development Deployment

**Quick Start:**
```bash
# 1. Clone and setup
git clone <your-repo>
cd cybersecuritysaas-main

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your GitHub OAuth credentials

# 4. Deploy
python deploy.py
```

**Manual Steps:**
```bash
# Initialize database
python init_db.py

# Start server
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

**Access:**
- Application: http://localhost:8001
- API Docs: http://localhost:8001/docs
- Health Check: http://localhost:8001/health

### Option 2: Docker Deployment

**Single Container:**
```bash
# Build and run
docker build -t cybersec-alert-saas .
docker run -p 8001:8001 --env-file .env cybersec-alert-saas
```

**Multi-Container (Recommended):**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Option 3: Production Deployment

#### A. Cloud Platform Deployment

**Heroku:**
```bash
# Create Procfile
echo "web: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create your-app-name
heroku config:set GITHUB_CLIENT_ID=your_client_id
heroku config:set GITHUB_CLIENT_SECRET=your_client_secret
heroku config:set GITHUB_REDIRECT_URI=https://your-app-name.herokuapp.com/api/v1/auth/github/callback
git push heroku main
```

**Railway:**
```bash
# Connect repository to Railway
# Set environment variables in Railway dashboard
# Deploy automatically on push
```

**Render:**
```bash
# Connect repository to Render
# Set environment variables
# Configure build command: pip install -r requirements.txt
# Configure start command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

#### B. VPS Deployment

**Ubuntu/Debian:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip python3-venv nginx postgresql

# Clone application
git clone <your-repo>
cd cybersecuritysaas-main

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup database
sudo -u postgres createdb cybersec_alerts
sudo -u postgres createuser cybersec_user

# Configure environment
cp .env.example .env
# Edit .env with production values

# Setup systemd service
sudo cp deployment/cybersec-alert.service /etc/systemd/system/
sudo systemctl enable cybersec-alert
sudo systemctl start cybersec-alert

# Setup nginx
sudo cp nginx.conf /etc/nginx/sites-available/cybersec-alert
sudo ln -s /etc/nginx/sites-available/cybersec-alert /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔧 Environment Configuration

### Required Environment Variables

```env
# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=https://yourdomain.com/api/v1/auth/github/callback

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://user:password@localhost/cybersec_alerts

# Email (Optional)
MAILGUN_API_KEY=your_mailgun_key
MAILGUN_DOMAIN=your_domain.com
FROM_EMAIL=noreply@yourdomain.com

# NVD API (Optional)
NVD_API_KEY=your_nvd_api_key
```

### Production Security Checklist

- [ ] Use HTTPS in production
- [ ] Set strong SECRET_KEY
- [ ] Configure CORS origins properly
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up proper logging
- [ ] Configure rate limiting
- [ ] Set up monitoring and alerts
- [ ] Regular backups
- [ ] SSL certificates
- [ ] Firewall configuration

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# Check application health
curl http://localhost:8001/health

# Check database connection
python -c "from backend.database.db import engine; print('DB OK')"

# Check GitHub OAuth
curl http://localhost:8001/api/v1/auth/github/login
```

### Logs
```bash
# Application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f app

# System logs
sudo journalctl -u cybersec-alert -f
```

### Backup
```bash
# Database backup
pg_dump cybersec_alerts > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz . --exclude=venv --exclude=__pycache__
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.KEY }}
          script: |
            cd /path/to/app
            git pull origin main
            source venv/bin/activate
            pip install -r requirements.txt
            python init_db.py
            sudo systemctl restart cybersec-alert
```

## 🚨 Troubleshooting

### Common Issues

**1. "GitHub OAuth not configured"**
- Check .env file exists and has correct values
- Restart application after changing .env
- Verify GitHub OAuth App settings

**2. Database connection errors**
- Check DATABASE_URL format
- Ensure database server is running
- Verify user permissions

**3. Port already in use**
- Change port in uvicorn command
- Check for other running services
- Use `netstat -tulpn | grep :8001`

**4. Permission denied**
- Check file permissions
- Run as appropriate user
- Verify Docker user permissions

### Performance Optimization

**For High Traffic:**
- Use Gunicorn with multiple workers
- Implement Redis for caching
- Use CDN for static files
- Database connection pooling
- Load balancing

**Gunicorn Configuration:**
```bash
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
```

## 📞 Support

For deployment issues:
1. Check logs for error messages
2. Verify environment configuration
3. Test individual components
4. Review security checklist
5. Contact support with error details

---

**🎉 Your CyberSec Alert SaaS is now deployed and ready to monitor vulnerabilities!** 