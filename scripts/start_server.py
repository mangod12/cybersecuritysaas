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
import asyncio
import uvicorn # Added import

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Modified path

async def main():
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
        
        print("\\n🎉 Application setup successful!")
        
        # Start the Uvicorn server
        print("\\n🚀 Launching Uvicorn server...")
        config = uvicorn.Config("backend.main:app", host="0.0.0.0", port=8000, reload=True)
        server = uvicorn.Server(config)
        await server.serve()
        
        print("\\nApplication is running at:")
        print("- Dashboard: http://localhost:8000")
        print("- API Docs: http://localhost:8000/docs")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # It's better to run uvicorn directly in non-async context for simplicity if the main goal is just to start the server.
    # However, to keep the async main structure for potential future async setup tasks, we'll use this.
    # For a production script, you might run uvicorn as a separate process or use a process manager.
    
    # Check if already in an asyncio event loop (e.g., if run from Jupyter or another async environment)
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        print("Asyncio loop is already running. Creating a new task for main().")
        task = loop.create_task(main())
        # If in a Jupyter-like environment, this might not block as expected.
        # For a script, we'd want it to block, so asyncio.run(main()) is generally preferred.
    else:
        success = asyncio.run(main())
        if not success:
            sys.exit(1)
