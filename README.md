# CyberSec Alert SaaS

A modern SaaS platform for enterprise security monitoring, asset management, and real-time vulnerability alerting.

---

## Features
- **User Authentication:** Email/password and GitHub OAuth login.
- **Dashboard:** View security alerts, assets, and statistics.
- **Asset Management:** Add, edit, and delete assets.
- **Alert Management:** View, acknowledge, and manage security alerts.
- **Automated CVE Scraping:** Fetches latest vulnerabilities from NVD and major vendors.
- **Email Notifications:** Sends alerts to registered users.
- **Token Verification:** Secure API access with JWT tokens.
- **Scheduler:** Automated background jobs for scraping and cleanup.
- **Modern SPA Frontend:** Responsive, minimal UI in a single HTML file.
- **Docker & Local Support:** Works with SQLite (local) and PostgreSQL (Docker).

---

## How It Works

### 1. **Architecture**
- **Backend:** FastAPI (Python), async SQLAlchemy, JWT, OAuth, background jobs.
- **Frontend:** Single-page app (`frontend/index.html`), fetches all data via REST API.
- **Database:**
  - **Local:** SQLite (`cybersec_alerts.db`)
  - **Docker:** PostgreSQL (containerized)
- **Scheduler:** APScheduler runs scraping and cleanup jobs.
- **Email:** Integrates with Mailgun (optional).

### 2. **Authentication**
- **Email/Password:** Standard registration and login.
- **GitHub OAuth:**
  - User clicks "Continue with GitHub"
  - Redirects to GitHub for authorization
  - On success, backend exchanges code for access token, fetches user info, logs in/creates user
- **JWT:** All API endpoints require a valid token (except login/register).

### 3. **Alert & Asset Management**
- **Assets:** Users can add, edit, and delete assets (servers, domains, etc.).
- **Alerts:**
  - CVE and vendor scrapers run on schedule
  - New vulnerabilities matching assets trigger alerts
  - Alerts are shown in dashboard and can be acknowledged

### 4. **Deployment**
- **Local:**
  - Uses SQLite
  - Run with `uvicorn` or `python scripts/setup_database.py`
- **Docker:**
  - Uses PostgreSQL
  - `docker compose up --build`
  - `.env` is loaded for all secrets and OAuth
- **Nginx (optional):**
  - Reverse proxy for production
  - Not required for local/dev

---

## Quick Start

### Local (SQLite)
```sh
pip install -r requirements.txt
python scripts/setup_database.py
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
Visit: http://localhost:8000

### Docker (PostgreSQL)
```sh
docker compose up --build
# In another terminal (first run only):
docker compose exec app python scripts/setup_database.py
```
Visit: http://localhost:8000

---

## Environment Variables (`.env`)
```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///cybersec_alerts.db  # or postgresql+psycopg2://postgres:postgres@db:5432/cybersaas
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:8000/api/v1/auth/github/callback
MAILGUN_API_KEY=your-mailgun-api-key (optional)
MAILGUN_DOMAIN=your-mailgun-domain (optional)
FROM_EMAIL=noreply@yourdomain.com (optional)
```

---

## GitHub OAuth Setup
1. Go to GitHub > Settings > Developer settings > OAuth Apps > New OAuth App
2. Set callback URL to: `http://localhost:8000/api/v1/auth/github/callback`
3. Copy Client ID and Secret to your `.env`
4. Restart backend/Docker after changes

---

## Project Structure
```
backend/         # FastAPI backend, routers, models, services
frontend/        # Single-page app (index.html)
scripts/         # Setup and utility scripts
tests/           # Pytest test suite
Dockerfile       # Docker build
nginx.conf       # (Optional) Nginx reverse proxy config
docker-compose.yml
.env             # Environment variables
```

---

## Testing
```sh
pytest
```

---

## Troubleshooting
- **Login fails:** Check `.env` and GitHub OAuth settings, restart backend.
- **DB errors in Docker:** Run `docker compose exec app python scripts/setup_database.py` after first startup.
- **OAuth callback mismatch:** Ensure callback URL in GitHub matches `.env` and how you access the app.
- **CORS issues:** Update `CORS_ORIGINS` in `.env` or backend config.

---

## License
MIT
