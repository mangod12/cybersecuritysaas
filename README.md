# CyberSec Alert SaaS

A comprehensive vulnerability monitoring and alerting platform for Small and Medium Businesses (SMBs). Track your IT assets and receive real-time alerts when new CVEs or vendor security advisories affect your infrastructure.

## 🚀 Features

- **Asset Management**: Track hardware, software, firmware, and operating systems
- **CVE Monitoring**: Automatic scanning of NIST NVD database for new vulnerabilities
- **Vendor Advisories**: Monitor security advisories from major vendors (Cisco, Fortinet, Microsoft)
- **Smart Matching**: Intelligent matching of vulnerabilities to your specific assets
- **Email Alerts**: Instant notifications via Mailgun when vulnerabilities affect your assets
- **Dashboard**: Web-based dashboard for managing assets and viewing alerts
- **RESTful API**: Complete API for integration with other tools
- **Scheduled Scanning**: Automated vulnerability checks every 6-12 hours

## 🏗️ Architecture

### Backend Stack
- **FastAPI**: High-performance web framework with automatic API documentation
- **SQLAlchemy**: Database ORM with support for SQLite (dev) and PostgreSQL (production)
- **APScheduler**: Background task scheduling for vulnerability scanning
- **JWT Authentication**: Secure token-based authentication
- **Pydantic**: Data validation and serialization
- **Mailgun**: Email delivery service for alerts

### Frontend
- **Vanilla JavaScript**: Lightweight frontend with modern ES6+ features
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Dynamic content loading via REST API

## 📋 Prerequisites

- Python 3.11+ (Python 3.12 recommended)
- Rust Toolchain (for compiling some dependencies)
- Microsoft Visual C++ 14.0 or greater (Build Tools for Visual Studio)
- SQLite (included) or PostgreSQL
- Mailgun account (for email alerts)
- Optional: NVD API key for higher rate limits

## 🛠️ Local Deployment (Windows/PowerShell)

### 1. Install Dependencies
Ensure you are in a PowerShell terminal with the Developer Command Prompt for Visual Studio environment loaded, or that the necessary build tools are in your PATH.
```powershell
# Create and activate a virtual environment (recommended)
python -m venv venv
.\\venv\\Scripts\\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` (if an example is provided) or create `.env` and fill in your settings.
Key settings to update:
- `DATABASE_URL` (defaults to SQLite)
- `SECRET_KEY` (generate a strong random key)
- `MAILGUN_API_KEY`, `MAILGUN_DOMAIN`, `FROM_EMAIL` (if using email alerts)
- `NVD_API_KEY` (optional, for NVD integration)

### 3. Initialize the Database
```powershell
python .\\scripts\\init_db.py
```

### 4. Start the Server
```powershell
python .\\scripts\\start_server.py
```
Alternatively, for development with auto-reload:
```powershell
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Access the Application
- Dashboard: [http://localhost:8000/](http://localhost:8000/)
  - **Note**: The basic frontend is a single `frontend/index.html` file.
  - To serve this through FastAPI, you would typically configure static file serving. For example, by adding `app.mount("/static_frontend", StaticFiles(directory="frontend"), name="frontend")` to `backend/main.py` and then accessing it via `/static_frontend/index.html`, or by creating a specific route to serve `index.html` at the root.
  - Alternatively, you can open `frontend/index.html` directly in your browser (though API calls might be affected by CORS if not configured for `file://` origins, which is generally not recommended for production).
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 6. (Optional) Run Demo/Test Scripts
Run the project demo to simulate asset creation and alert checking:
```powershell
python .\\scripts\\run_project_demo.py
```
Run the API demo for specific endpoint tests:
```powershell
python .\\scripts\\run_api_demo.py
```
Check server status:
```powershell
python .\\scripts\\status_check.py
```
Verify deployment:
```powershell
python .\\scripts\\verify_deployment.py
```

## ✅ Testing
Run automated tests using pytest:
```powershell
pytest
```
This will discover and run tests in the `tests/` directory.

## 📦 Production Deployment
- Use PostgreSQL and production settings in `.env`
- Set `DEBUG=False` in `.env`
- Use a process manager (e.g., gunicorn with uvicorn workers) for production
- Set up HTTPS and a reverse proxy (nginx, etc.)

## 🧩 How It Works: System Overview

CyberSec Alert SaaS is designed as a modular, production-ready platform for vulnerability monitoring and alerting. Here’s how the main components interact:

### 1. Configuration
- All environment variables are loaded from `.env` using Pydantic Settings (`backend/config.py`).
- Database, JWT, email, and scheduler settings are centralized for easy management.

### 2. Database Layer
- SQLAlchemy ORM models (`backend/models/`) define Users, Assets, and Alerts.
- Database connection/session management is handled in `backend/database/db.py` (sync and async support).
- The database is initialized and seeded with sample data using `scripts/init_db.py` and `backend/database/seed.py`.

### 3. API Layer (FastAPI)
- The main FastAPI app is in `backend/main.py`.
- Routers for authentication, asset management, and alerting are in `backend/routers/`.
- All endpoints are versioned under `/api/v1/`.
- JWT authentication is enforced for protected endpoints.

### 4. Vulnerability & Advisory Processing
- Background scheduler (`backend/scheduler/cron.py`) runs periodic tasks to fetch new CVEs and vendor advisories.
- Scrapers in `backend/services/` fetch and parse vulnerability data.
- The alert checker (`backend/services/alert_checker.py`) matches new vulnerabilities to user assets and creates alerts.
- Email notifications are sent via Mailgun using `backend/services/email_alert.py`.

### 5. Frontend
- The frontend is a simple HTML/JS dashboard in `frontend/index.html`.
- It interacts with the backend API for asset management and alert viewing.

### 6. Testing & Scripts
- All automated tests are in the `tests/` directory and can be run with `pytest`.
- Utility/demo scripts are in `scripts/` for setup, health checks, and demos.

## 📚 Code Documentation
- All Python modules and classes are now documented with clear docstrings and comments.
- See each file for details on its purpose and usage.

## 🏁 Typical Workflow
1. Clone the repo and install dependencies.
2. Configure `.env` for your environment.
3. Run `python scripts/init_db.py` to set up the database.
4. Start the server with `python scripts/start_server.py` or the uvicorn command.
5. Access the dashboard and API docs in your browser.
6. Add assets, configure email, and let the system monitor for vulnerabilities!

---

**Built with ❤️ for the cybersecurity community**