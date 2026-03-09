# Cloud Run + PostgreSQL Setup Guide

This guide shows how to set up Cloud SQL PostgreSQL for the production deployment.

## Quick Setup (Cloud Console)

### 1. Create Cloud SQL PostgreSQL Instance

```bash
gcloud sql instances create cybersec-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=YOUR_ROOT_PASSWORD
```

Or via Console:
1. Go to **Cloud SQL** → **Create Instance** → **PostgreSQL**
2. Instance ID: `cybersec-db`
3. Password: Choose a secure password
4. Region: `us-central1` (same as Cloud Run)
5. Machine: `db-f1-micro` (for demo) or higher for production
6. Storage: 10GB minimum

### 2. Create Database and User

```bash
# Create database
gcloud sql databases create cybersec_alerts --instance=cybersec-db

# Create user
gcloud sql users create cybersec_user \
  --instance=cybersec-db \
  --password=YOUR_USER_PASSWORD
```

### 3. Connect Cloud Run to Cloud SQL

1. Go to **Cloud Run** → Select your service → **Edit & Deploy New Revision**
2. Under **Connections**, click **Add Connection**
3. Select your Cloud SQL instance: `cybersec-db`
4. Click **Deploy**

### 4. Set Environment Variables

In Cloud Run service settings, add:

```
DATABASE_URL=postgresql+psycopg2://cybersec_user:YOUR_USER_PASSWORD@/cybersec_alerts?host=/cloudsql/PROJECT_ID:us-central1:cybersec-db

SECRET_KEY=your-random-secret-key-here

# Optional but recommended:
MAILGUN_API_KEY=your-mailgun-key
MAILGUN_DOMAIN=your-mailgun-domain
FROM_EMAIL=alerts@yourdomain.com
```

**Important:** Replace:
- `YOUR_USER_PASSWORD` with the password you set
- `PROJECT_ID` with your actual GCP project ID
- `your-random-secret-key-here` with a secure random string

### 5. Deploy

The auto-deploy is already configured. Just push to `main`:

```bash
git push origin main
```

Or deploy manually:

```bash
gcloud run deploy cybersec-saas \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

## Verification

After deployment:

1. Check health: `https://YOUR-SERVICE-URL/health`
2. Login with demo credentials:
   - Email: `admin@example.com`
   - Password: `password123`

## Cost Optimization

**Development/Demo:**
- Use `db-f1-micro` instance (~$7/month)
- Stop instance when not in use

**Production:**
- Use `db-custom` with appropriate CPU/memory
- Enable automatic backups
- Set up High Availability if needed

## Troubleshooting

### "Can't connect to database"
- Verify Cloud SQL connection is added to Cloud Run
- Check DATABASE_URL format matches Cloud SQL Unix socket format
- Ensure database and user exist

### "Demo login doesn't work"
- Database is being auto-seeded on startup
- Check Cloud Run logs for seeding errors
- Verify DATABASE_URL is set correctly

### "Service won't start"
- Check Cloud Run logs for Python errors
- Verify all required dependencies in requirements.txt
- Ensure SECRET_KEY environment variable is set
