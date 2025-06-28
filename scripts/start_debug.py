#!/usr/bin/env python3
"""
Debug startup script for the CVE Alert SaaS.
This script helps identify and fix startup issues.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent # Modified path
sys.path.insert(0, str(project_root))

async def test_database_connection():
    """Test database connection and create tables if needed."""
    try:
        from backend.database.db import engine, Base
        from backend.models import user, asset, alert  # Import all models
        
        print("🔌 Testing database connection...")
        
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

async def test_imports():
    """Test all critical imports."""
    try:
        print("📦 Testing imports...")
        
        # Test config
        from backend.config import settings
        print(f"   Config loaded: {settings.APP_NAME}")
        
        # Test models
        from backend.models.user import User
        from backend.models.asset import Asset
        from backend.models.alert import Alert
        print("   Models imported successfully")
        
        # Test services
        from backend.services.auth_service import get_password_hash
        from backend.services.cve_scraper import CVEScraper
        print("   Services imported successfully")
        
        # Test routers
        from backend.routers.auth import router as auth_router
        from backend.routers.assets import router as assets_router
        from backend.routers.alerts import router as alerts_router
        print("   Routers imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def seed_database():
    """Seed the database with initial data."""
    try:
        print("🌱 Seeding database...")
        from backend.database.seed import init_db
        await init_db()
        print("✅ Database seeded successfully")
        return True
    except Exception as e:
        print(f"❌ Database seeding failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def start_server():
    """Start the FastAPI server."""
    try:
        print("🚀 Starting server...")
        import uvicorn
        from backend.main import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Server start failed: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main debug function."""
    print("🔍 CVE Alert SaaS - Debug Startup")
    print("=" * 40)
    
    # Test imports first
    if not await test_imports():
        print("❌ Cannot proceed due to import errors")
        return
    
    # Test database
    if not await test_database_connection():
        print("❌ Cannot proceed due to database errors")
        return
    
    # Seed database
    if not await seed_database():
        print("⚠️  Database seeding failed, but continuing...")
    
    print("\n✅ All checks passed! Starting server...")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📊 Dashboard will be available at: http://localhost:8000/")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("\nPress CTRL+C to stop the server")
    
    # Start the server
    start_server()

if __name__ == "__main__":
    asyncio.run(main())
