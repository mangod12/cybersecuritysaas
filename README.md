# CyberSec Alert SaaS

A modern SaaS platform for enterprise security monitoring, asset management, and real-time vulnerability alerting.

---

## 🎯 Problem Statement

Organizations today face critical challenges in managing their cybersecurity posture:

- **Overwhelming Alert Fatigue:** Security teams are bombarded with thousands of vulnerability alerts daily from multiple sources (NVD, vendor advisories, CVE feeds), making it nearly impossible to prioritize and respond effectively.

- **Delayed Response Times:** Manual monitoring of security feeds and vendor advisories leads to delayed awareness of critical vulnerabilities, leaving systems exposed to exploitation during the gap between disclosure and patching.

- **Poor Asset Visibility:** Without centralized asset management, organizations struggle to understand which systems are affected by new vulnerabilities, leading to inefficient triage and remediation workflows.

- **Missed Critical Updates:** Important security advisories from vendors like Microsoft, Cisco, Red Hat, and others are scattered across different platforms, increasing the risk of missing critical patches and updates.

- **Lack of Automation:** Manual processes for vulnerability tracking, alert distribution, and asset correlation consume valuable security team resources that could be better spent on strategic initiatives.

### How This Platform Solves These Problems

CyberSec Alert SaaS provides a **unified, automated vulnerability intelligence platform** that:
- ✅ Aggregates vulnerabilities from multiple authoritative sources into a single dashboard
- ✅ Automatically correlates new threats with your asset inventory
- ✅ Sends real-time notifications only for relevant vulnerabilities
- ✅ Reduces alert fatigue through intelligent filtering and asset matching
- ✅ Enables rapid response with centralized alert management and acknowledgment workflows

---

## 🚀 What This System Does

CyberSec Alert SaaS is a **comprehensive vulnerability intelligence and alerting platform** that automates the entire security monitoring lifecycle.

### Core Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA COLLECTION LAYER                         │
│  NVD CVE Feed  │  Microsoft MSRC  │  Cisco PSIRT  │  Red Hat   │
│  Vendor RSS    │  Security APIs   │  Advisories   │  And More  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  AUTOMATED SCRAPING ENGINE                       │
│  • Scheduled jobs (APScheduler)                                 │
│  • CVE enrichment with CVSS scores                              │
│  • Multi-source vulnerability aggregation                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CORRELATION ENGINE                             │
│  • Matches vulnerabilities to user assets                       │
│  • Creates targeted alerts                                      │
│  • Deduplication and prioritization                             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  NOTIFICATION SYSTEM                             │
│  Email Alerts  │  Dashboard Updates  │  Future: Slack/Discord  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                                │
│  • Real-time dashboard with statistics                          │
│  • Asset management portal                                      │
│  • Alert acknowledgment and tracking                            │
└─────────────────────────────────────────────────────────────────┘
```

### 5 Key Capabilities

1. **🔍 Multi-Source Vulnerability Aggregation**
   - Automatically collects CVEs from NVD (National Vulnerability Database)
   - Fetches vendor-specific advisories (Microsoft MSRC, Cisco PSIRT, Red Hat Security)
   - Parses RSS feeds from major security vendors
   - Enriches vulnerability data with CVSS scores and metadata

2. **🏢 Intelligent Asset Management**
   - Centralized inventory of your IT assets (servers, domains, applications)
   - Easy add/edit/delete operations through web interface
   - Asset metadata tracking for better vulnerability correlation
   - Future: CPE (Common Platform Enumeration) matching for precise asset-vulnerability mapping

3. **⚡ Real-Time Alert Generation**
   - Automatic correlation between new vulnerabilities and your assets
   - Instant alert creation when threats affect your infrastructure
   - Priority-based alerting (critical, high, medium, low)
   - Alert deduplication to reduce noise

4. **📧 Multi-Channel Notifications**
   - Email notifications via Mailgun integration
   - Dashboard alerts with visual indicators
   - Acknowledge/dismiss workflow for alert management
   - Future: Slack, Discord, Microsoft Teams, and SMS notifications

5. **🔐 Enterprise-Grade Authentication**
   - Email/password authentication with secure password hashing
   - GitHub OAuth integration for seamless SSO
   - JWT-based API security
   - Token verification for all protected endpoints

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, high-performance Python web framework with automatic API documentation
- **SQLAlchemy 2.0** - Async ORM for database operations
- **Alembic** - Database migration management
- **APScheduler** - Background job scheduling for automated scraping
- **Uvicorn/Gunicorn** - ASGI server for production deployment
- **Python-JOSE** - JWT token generation and validation
- **Passlib** - Secure password hashing with bcrypt

### Frontend
- **Single-Page Application** - Vanilla JavaScript SPA (`frontend/index.html`)
- **REST API Integration** - All data fetched via asynchronous API calls
- **Responsive Design** - Mobile-friendly interface
- **Real-time Updates** - Dynamic dashboard with live statistics

### Infrastructure
- **Docker & Docker Compose** - Containerized deployment
- **PostgreSQL** - Production database (Docker)
- **SQLite** - Development database (local)
- **Nginx** - Optional reverse proxy for production
- **Heroku-ready** - Procfile and runtime.txt included

### Security & Data Sources
- **NVD CVE Feed** - NIST National Vulnerability Database
- **Microsoft MSRC API** - Microsoft Security Response Center advisories
- **Cisco PSIRT API** - Cisco Product Security Incident Response Team
- **Red Hat Security API** - Red Hat CVE database
- **Mailgun API** - Email notification service
- **GitHub OAuth** - Social authentication provider
- **HTTPX/AIOHTTP** - Async HTTP clients for API integrations
- **BeautifulSoup4** - HTML parsing for vendor advisories

### Development & Testing
- **pytest** - Unit and integration testing
- **pytest-asyncio** - Async test support
- **black** - Code formatting
- **flake8** - Linting
- **isort** - Import sorting
- **python-dotenv** - Environment variable management

## ✨ Key Features

### 🔐 Authentication & Authorization
- [x] **Email/Password Authentication** - Secure registration and login with bcrypt password hashing
- [x] **GitHub OAuth Integration** - Seamless single sign-on with GitHub accounts
- [x] **JWT Token-Based Security** - Stateless authentication for all API endpoints
- [x] **Token Verification** - Automatic validation of user sessions
- [ ] **Two-Factor Authentication (2FA)** - Future enhancement for additional security
- [ ] **Role-Based Access Control (RBAC)** - Multi-tenancy support with admin/user roles

### 📊 Real-Time Dashboard
- [x] **Live Statistics** - Real-time counts of alerts, assets, and vulnerabilities
- [x] **Alert Summary** - Overview of critical, high, medium, and low-priority alerts
- [x] **Asset Overview** - At-a-glance view of all monitored assets
- [x] **Recent Activity Feed** - Latest alerts and system events
- [x] **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices

### 🏢 Asset Management
- [x] **Add/Edit/Delete Assets** - Full CRUD operations for asset inventory
- [x] **Asset Metadata** - Store asset names, types, descriptions, and custom fields
- [x] **Asset Search & Filtering** - Quickly find specific assets
- [x] **Asset-Alert Correlation** - Automatic matching of vulnerabilities to assets
- [ ] **CPE Matching** - Future: Precise vulnerability-to-asset matching using Common Platform Enumeration
- [ ] **Asset Import/Export** - Bulk operations via CSV/JSON

### 🚨 Automated Alert System
- [x] **Automatic Alert Generation** - Creates alerts when vulnerabilities match your assets
- [x] **Multi-Level Severity** - Critical, High, Medium, Low priority classification
- [x] **Alert Acknowledgment** - Mark alerts as reviewed or dismissed
- [x] **Alert History** - Complete audit trail of all alerts
- [x] **Deduplication** - Prevents duplicate alerts for the same vulnerability
- [ ] **Custom Alert Rules** - Future: User-defined filtering and routing logic
- [ ] **Alert Suppression** - Temporary muting of specific alert types

### 🔍 Automated Vulnerability Scraping
- [x] **NVD CVE Feed** - Daily scraping of National Vulnerability Database
- [x] **Microsoft MSRC API** - Microsoft Security Response Center advisories
- [x] **Cisco PSIRT API** - Cisco Product Security Incident Response Team updates
- [x] **Red Hat Security API** - Red Hat CVE database integration
- [x] **Vendor RSS Feeds** - Multiple vendor advisory feeds
- [x] **CVE Enrichment** - Automatic CVSS score fetching and metadata enhancement
- [x] **Scheduled Jobs** - APScheduler for automated, periodic scraping
- [ ] **Custom Scraper Configuration** - User-defined scraping frequencies and sources

### 👨‍💻 Developer-Friendly
- [x] **RESTful API** - Clean, well-documented API endpoints
- [x] **Automatic API Documentation** - FastAPI auto-generated docs at `/docs` (Swagger UI)
- [x] **Async/Await** - High-performance async operations throughout
- [x] **Database Migrations** - Alembic for version-controlled schema changes
- [x] **Environment Configuration** - `.env` file for easy setup
- [x] **Docker Support** - One-command containerized deployment
- [x] **Local Development** - SQLite for quick local testing without Docker

### 📧 Email Notifications
- [x] **Mailgun Integration** - Professional email delivery service
- [x] **Alert Emails** - Automatic notifications for new critical alerts
- [x] **HTML Email Templates** - Professional, branded email design
- [x] **Configurable Recipients** - Email sent to all registered users
- [ ] **Email Preferences** - Future: Per-user notification settings
- [ ] **Digest Emails** - Scheduled summary emails (daily/weekly)

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

## 🔮 Future Improvements

### High Priority
1. **🔗 Advanced Asset Correlation with CPE Matching**
   - Implement Common Platform Enumeration (CPE) database
   - Automatic matching of CVEs to assets using CPE strings
   - Significantly reduce false positives and improve alert accuracy
   - Support for software version tracking and affected version ranges

2. **🏢 Multi-Tenancy Support**
   - Organization/team workspace isolation
   - Role-Based Access Control (RBAC) with admin, manager, and viewer roles
   - Per-organization asset and alert management
   - Team collaboration features

3. **📢 Enhanced Notification System**
   - Slack integration with webhook support
   - Discord notifications for security teams
   - Microsoft Teams channel alerts
   - SMS notifications via Twilio for critical alerts
   - Per-user notification preferences (channel, frequency, severity filters)
   - Notification templates and customization

4. **🧠 Vulnerability Intelligence Enhancements**
   - CVSS score-based automatic prioritization
   - EPSS (Exploit Prediction Scoring System) integration
   - Known exploited vulnerabilities (KEV) catalog integration
   - Threat intelligence feeds (e.g., CISA, AlienVault OTX)
   - Vulnerability trending and statistics

### Medium Priority
5. **📈 Dashboard Enhancements**
   - Interactive charts and graphs (Chart.js/D3.js)
   - Vulnerability trend analysis over time
   - Asset risk scoring and heat maps
   - Customizable dashboard widgets
   - Export reports to PDF/Excel
   - Executive summary views

6. **🤖 Automation & Integrations**
   - Jira ticket auto-creation for critical vulnerabilities
   - ServiceNow integration for enterprise workflows
   - PagerDuty integration for on-call alerting
   - REST API webhooks for custom integrations
   - GitHub Security Advisory integration
   - Automated remediation workflow suggestions

7. **📋 Compliance & Reporting**
   - Compliance framework mapping (PCI-DSS, HIPAA, SOC 2, ISO 27001)
   - Automated compliance reports
   - Audit logging for all user actions
   - Vulnerability SLA tracking
   - Executive summary reports

8. **🎯 AI-Powered Features**
   - Machine learning for alert prioritization
   - Natural language processing for vulnerability summaries
   - Predictive analytics for vulnerability trends
   - Automated asset tagging and categorization
   - Intelligent alert grouping and correlation

### Technical Improvements
9. **⚡ Performance Optimization**
   - Redis caching layer for API responses
   - Database query optimization and indexing
   - Elasticsearch for full-text search
   - Real-time WebSocket updates instead of polling
   - CDN integration for static assets

10. **🔒 Security Enhancements**
    - Two-Factor Authentication (2FA/MFA)
    - API rate limiting and throttling
    - IP whitelist/blacklist support
    - Security audit logging
    - Encrypted data at rest
    - Regular security scanning with SAST/DAST tools

11. **🚀 DevOps & Infrastructure**
    - Kubernetes deployment manifests
    - Helm charts for easy deployment
    - CI/CD pipeline automation (GitHub Actions)
    - Automated testing (unit, integration, E2E)
    - Infrastructure as Code (Terraform)
    - Monitoring and observability (Prometheus, Grafana)
    - Log aggregation (ELK stack)

12. **💡 User Experience**
    - Modern frontend framework (React/Vue/Svelte)
    - Dark mode support
    - Advanced search and filtering
    - Saved searches and custom views
    - Mobile native apps (iOS/Android)
    - In-app guided tours and help system
    - Keyboard shortcuts for power users

---

## Troubleshooting
- **Login fails:** Check `.env` and GitHub OAuth settings, restart backend.
- **DB errors in Docker:** Run `docker compose exec app python scripts/setup_database.py` after first startup.
- **OAuth callback mismatch:** Ensure callback URL in GitHub matches `.env` and how you access the app.
- **CORS issues:** Update `CORS_ORIGINS` in `.env` or backend config.

---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### How to Contribute
1. **Fork the repository** and create your feature branch (`git checkout -b feature/AmazingFeature`)
2. **Make your changes** and ensure they follow the project's coding standards
3. **Test your changes** thoroughly (`pytest`)
4. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
5. **Push to the branch** (`git push origin feature/AmazingFeature`)
6. **Open a Pull Request** with a clear description of your changes

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Use `black` for code formatting
- Add tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

### Areas We Need Help
- [ ] Frontend modernization (React/Vue migration)
- [ ] Additional vulnerability source integrations
- [ ] Test coverage improvements
- [ ] Documentation enhancements
- [ ] Performance optimizations
- [ ] Security auditing

---

## 📧 Contact

- **Project Maintainer:** [GitHub Profile](https://github.com/mangod12)
- **Repository:** [https://github.com/mangod12/cybersecuritysaas](https://github.com/mangod12/cybersecuritysaas)
- **Issues:** [Report a Bug](https://github.com/mangod12/cybersecuritysaas/issues)
- **Feature Requests:** [Request a Feature](https://github.com/mangod12/cybersecuritysaas/issues/new)

---

## 📊 Project Statistics

![GitHub last commit](https://img.shields.io/github/last-commit/mangod12/cybersecuritysaas)
![GitHub issues](https://img.shields.io/github/issues/mangod12/cybersecuritysaas)
![GitHub pull requests](https://img.shields.io/github/issues-pr/mangod12/cybersecuritysaas)
![GitHub](https://img.shields.io/github/license/mangod12/cybersecuritysaas)

**Language Composition:**
- Python (Backend, APIs, Scrapers, Services)
- JavaScript (Frontend SPA)
- HTML/CSS (User Interface)
- SQL (Database Schemas)
- Shell (Deployment Scripts)

**Lines of Code:** ~4,000+ lines

---

## License
MIT
