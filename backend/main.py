"""
FastAPI main application entry point.
Configures the API, middleware, routers, and startup/shutdown events.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os

from backend.config import settings
from backend.routers import auth, assets, alerts
from backend.scheduler.cron import scheduler


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    description="CVE and OEM vulnerability notification SaaS for SMBs",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(assets.router, prefix="/api/v1/assets", tags=["Assets"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version
    }


# Root endpoint to serve the frontend
@app.get("/")
async def root():
    """Serves the main frontend HTML file."""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        logger.error(f"index.html not found at {index_path}")
        raise HTTPException(status_code=404, detail="Frontend not found. Ensure index.html is in the frontend directory.")


# Serve static files (CSS, JS, images) from the frontend directory
# This should be placed *after* the root endpoint if the root also serves a file from this directory.
# However, if index.html is the only file served from root, and other assets are in subdirectories,
# it can be structured like this.
# For a more robust setup, especially with Single Page Applications (SPAs),
# you might have a catch-all route for the SPA and specific static mounts.

# Determine the absolute path to the frontend directory
# __file__ is backend/main.py
# os.path.dirname(__file__) is backend/
# os.path.dirname(os.path.dirname(__file__)) is the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(project_root, "frontend")

# Mount static files directory if it exists
if os.path.isdir(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
    logger.info(f"Serving static files from {frontend_dir} at /static")
else:
    logger.warning(f"Frontend directory not found at {frontend_dir}. Static files will not be served.")

# If your index.html references CSS/JS files directly like <link href="style.css">
# and they are in the same 'frontend' directory, you might need to serve the whole 'frontend' directory.
# Example: app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend_root")
# This would make index.html accessible at "/" and other files like "script.js" at "/script.js".
# The current setup serves index.html specifically at "/" and other files (if any) would need to be under /static
# or accessed via a different mount.

# For simplicity, if index.html is the primary entry and it references other files
# within the frontend folder (e.g. <script src="script.js">),
# we should adjust the static file serving.
# Let's assume for now that index.html is self-contained or uses CDN for JS/CSS,
# or that its assets are correctly referenced considering the /static mount if they exist.
# The current index.html uses CDN for axios, so that's fine.

# If you have local CSS/JS files in 'frontend' referenced by 'index.html'
# e.g. <link rel="stylesheet" href="style.css">
# You would need to adjust the StaticFiles mount.
# A common pattern is:
# app.mount("/static", StaticFiles(directory="frontend/static"), name="static_assets") # if you have a frontend/static subfolder
# and then serve index.html from the root.
# Or, if all assets are in 'frontend' alongside 'index.html':
# app.mount("/", StaticFiles(directory=frontend_dir, html = True), name="app")
# This makes any file in 'frontend' accessible from the root.
# e.g. http://localhost:8000/style.css if style.css is in frontend/
# And it will automatically serve index.html for '/'.

# Let's refine the static serving to make sure index.html and any other assets in frontend/ are served correctly.
# We will remove the specific @app.get("/") for index.html and use StaticFiles with html=True.

# Remove the previous @app.get("/")
# And replace the app.mount("/static", ...) with:

# (This is a conceptual change, the tool will apply it based on the final code block)
# The following code block will reflect the final intended change for serving static files.
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="app")