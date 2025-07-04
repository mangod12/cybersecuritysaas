"""
FastAPI main application entry point.
Configures the API, middleware, routers, and startup/shutdown events.
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import pyotp
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.routers import auth, alerts, assets, dashboard
from backend.scheduler.cron import scheduler
from backend.models.audit_log import AuditLog
from backend.database.db import get_async_db


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting CyberSec Alert SaaS...")
    
    # Start scheduler
    scheduler.start()
    logger.info("Scheduler started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    scheduler.shutdown()
    logger.info("Scheduler stopped")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A SaaS for monitoring cybersecurity alerts.",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, lambda r, e: JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"}))

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "null" # Allow file:// origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    """Application startup events."""
    # No database init_db call here; handled by migration or setup script
    logger.info("Startup complete.")


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status_code": 500}
    )


# API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(assets.router, prefix="/api/v1/assets", tags=["assets"])
app.include_router(dashboard.router)


# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version
    }


# Serve static files from frontend directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(project_root, "frontend")

if os.path.isdir(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
    logger.info(f"Serving frontend from {frontend_dir}")
else:
    logger.warning(f"Frontend directory not found at {frontend_dir}")
    # Fallback root endpoint if frontend is missing
    @app.get("/")
    async def root():
        return {"message": "Frontend not found", "docs": "/docs", "health": "/health"}

# --- MFA and Audit Logging for login ---
@app.post("/api/v1/auth/login")
@limiter.limit("5/minute")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), request: Request = None, db: AsyncSession = Depends(get_async_db)):
    # ...existing login logic...
    # MFA check (if enabled for user)
    # if user.mfa_enabled:
    #     # Prompt for TOTP code and verify with pyotp
    #     ...
    # Audit log
    # audit = AuditLog(user_id=user.id, action="login", detail=f"IP: {request.client.host if request else 'unknown'}")
    # db.add(audit)
    # await db.commit()
    pass  # Placeholder for future audit logging