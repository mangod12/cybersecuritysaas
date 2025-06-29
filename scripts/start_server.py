"""
start_server.py - CyberSec Alert SaaS

This script starts the FastAPI application using Uvicorn.
- Verifies that configuration, database models, and FastAPI app can be imported.
- Starts the Uvicorn server to serve the application.

Usage:
    python scripts/start_server.py
"""

import sys
import os
import uvicorn

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    print("🚀 Starting CyberSec Alert SaaS...")
    
    try:
        # Test basic imports
        print("📦 Testing imports...")
        from backend.config import settings
        print(f"✅ Config loaded: {settings.app_name}")
        
        # Test database setup
        from backend.database.db import Base
        print("✅ Database models available")
        
        # Test FastAPI app creation
        from backend.main import app
        print("✅ FastAPI app created")
        
        print("\n🎉 Application setup successful!")
        
        # Start the Uvicorn server
        print("\n🚀 Launching Uvicorn server...")
        uvicorn.run(
            "backend.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
        return True
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
