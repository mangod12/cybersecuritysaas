from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.routers.auth import get_current_user
from backend.dependencies.user_dependencies import require_role
from backend.models.alert import get_alerts
from backend.services.scrapers.loader import run_all_scrapers
from backend.database.db import get_db
from backend.logging_config import logger

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user=Depends(get_current_user)):
    alerts = get_alerts()
    return templates.TemplateResponse("dashboard.html", {"request": request, "alerts": alerts, "user": user})

@router.get("/oems", response_class=HTMLResponse)
async def oem_sources(request: Request, user=Depends(require_role("admin"))):
    # For demo: list available scrapers
    from backend.services.scrapers.loader import run_all_scrapers
    return templates.TemplateResponse("oems.html", {"request": request, "user": user, "oems": ["Google Security Blog"]})

@router.get("/users", response_class=HTMLResponse)
async def users(request: Request, user=Depends(require_role("admin"))):
    # For demo: list users
    from backend.models.user import list_users
    return templates.TemplateResponse("users.html", {"request": request, "user": user, "users": list_users()})