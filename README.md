

# CyberSec Alert SaaS

[![CI](https://github.com/mangod12/cybersecuritysaas/actions/workflows/ci.yml/badge.svg)](https://github.com/mangod12/cybersecuritysaas/actions/workflows/ci.yml)

Production-deployed vulnerability intelligence platform that aggregates CVEs from multiple authoritative sources and automatically correlates them with enterprise assets to generate real-time prioritized alerts.

🚀 **Live Demo:**
[https://cybersec-saas-zjfau6dqcq-uc.a.run.app/](https://cybersec-saas-zjfau6dqcq-uc.a.run.app/)

🧪 **Demo Login:**
- Email: `admin@example.com` / Password: `password123`
- Or use **GitHub OAuth** login

**Tech:** FastAPI + PostgreSQL + Cloud Run with auto-deploy on push to `main`

---

## Overview

CyberSec Alert SaaS solves a real operational security problem:

Security teams receive thousands of vulnerability disclosures daily. Most are irrelevant. Manual triage is inefficient and error-prone.

This system:

* Aggregates CVEs from NVD, Microsoft MSRC, Cisco PSIRT, Red Hat, and RSS feeds
* Enriches vulnerabilities with CVSS scoring
* Correlates vulnerabilities against user-managed asset inventory
* Automatically generates targeted alerts
* Reduces alert fatigue through asset-based filtering
* Provides centralized dashboard + notification workflows

---

## System Architecture

```
External Sources
(NVD, MSRC, Cisco, Red Hat, RSS)
        │
        ▼
Async Scraping Engine (APScheduler)
        │
        ▼
Vulnerability Enrichment Layer
        │
        ▼
Asset Correlation Engine
        │
        ▼
Alert Generation + Deduplication
        │
        ▼
Dashboard + Email Notifications
```

Deployed as a containerized FastAPI application on Google Cloud Run.

---

## Key Capabilities

### Multi-Source Aggregation

* NVD CVE feed
* Microsoft MSRC advisories
* Cisco PSIRT API
* Red Hat Security data
* Vendor RSS feeds
* CVSS enrichment

### Asset Management

* Full CRUD asset inventory
* Vendor / product / version tracking
* Asset-to-vulnerability matching
* Metadata tracking

### Alert System

* Automatic alert generation
* Severity classification (Critical → Low)
* Deduplication
* Alert acknowledgment workflow
* Dashboard visibility

### Authentication & Security

* Secure password hashing (bcrypt)
* JWT-based authentication
* GitHub OAuth login
* Token validation middleware

### Notifications

* Email integration (Mailgun)
* Dashboard alert visibility
* Slack webhook field ready for extension

---

## Tech Stack

Backend:

* FastAPI (async)
* SQLAlchemy 2.0
* PostgreSQL (production)
* SQLite (local dev)
* APScheduler
* Python-JOSE (JWT)
* Passlib (bcrypt)

Frontend:

* Vanilla JavaScript SPA
* REST API integration

Infrastructure:

* Docker
* Google Cloud Run (production)
* Nginx (optional reverse proxy)
* Gunicorn/Uvicorn ASGI server

Testing:

* pytest
* pytest-asyncio

---

## Production Deployment

Hosted on: **Google Cloud Run**

* Containerized via Docker
* Managed PostgreSQL database
* Async API architecture
* Environment-based configuration
* Secure secret management

---

## Screenshots

Login Interface
![Login](./Screenshot%202026-02-23%20152721.png)

Dashboard & Asset Management
![Dashboard](./Screenshot%202026-02-23%20152748.png)

---

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Setup database (creates tables and seeds demo user)
python scripts/setup_database.py

# Run development server
uvicorn backend.main:app --reload
```

Visit: http://localhost:8000/app/

### Production Deployment (Google Cloud Run)

**Automatic deployment is configured!** Just push to `main`:

```bash
git push origin main
```

The Cloud Build trigger automatically builds and deploys to Cloud Run.

**First-time setup:**
1. Follow [CLOUD_SQL_SETUP.md](CLOUD_SQL_SETUP.md) to create PostgreSQL database
2. Or run the automated script in Cloud Shell:
   ```bash
   bash scripts/setup_cloud_sql.sh YOUR_PROJECT_ID
   ```

---

## Configuration

Copy `.env.example` to `.env` and configure:

**Required:**
- `SECRET_KEY` - Random secret for JWT signing
- `DATABASE_URL` - PostgreSQL connection string

**Optional:**
- `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` - For GitHub OAuth
- `MAILGUN_API_KEY` / `MAILGUN_DOMAIN` - For email alerts
- `NVD_API_KEY` - For CVE data (higher rate limits)

See [.env.example](.env.example) for full configuration options.

---

## Roadmap (Focused)

* CPE-based asset matching
* EPSS integration
* Slack & Teams notifications
* Role-based access control (RBAC)
* Multi-tenant architecture
* CI/CD pipeline automation

---

## Repository Structure

```
backend/              FastAPI app, routers, models, services
  ├── routers/        API endpoints
  ├── services/       Business logic & external API integrations
  ├── models/         SQLAlchemy ORM models
  └── database/       DB connection & seeding
frontend/             Vanilla JS SPA
scripts/              Deployment & setup utilities
tests/                pytest test suite
.github/workflows/    CI/CD pipelines
  ├── ci.yml          Tests on PR
  └── deploy.yml      Auto-deploy on push
cloudbuild.yaml       Cloud Build configuration
Dockerfile            Container image
```

---

## Why This Project Matters

This project demonstrates:

* Async backend architecture
* External API integration
* Scheduled background jobs
* Secure authentication systems
* Asset correlation logic
* Production deployment experience
* Containerization & cloud deployment

---

## License

MIT

