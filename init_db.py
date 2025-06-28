#!/usr/bin/env python3
"""
Database initialization script for CyberSec Alert SaaS.

This script creates all database tables and seeds the database with initial data.
It is intended to be run once during setup or whenever you need to reset the database
for development or testing.

- Uses the async SQLAlchemy engine for table creation.
- Calls the seed_database() function to add a sample admin user and assets.
- Prints status messages to the console for user feedback.

Usage:
    python init_db.py

Requirements:
    - The .env file must be configured with the correct DATABASE_URL.
    - All dependencies in requirements.txt must be installed.
"""

import asyncio
import sys
import os
import traceback

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pydantic import BaseModel, Field  # noqa: E402

# Refactor imports to ensure compatibility
async def main():
    """Initialize the database."""
    try:
        print("Initializing database...")
        # Import after path setup
        from backend.database.db import async_engine, Base # Use async_engine
        from backend.models.user import User
        from backend.models.asset import Asset
        from backend.models.alert import Alert
        from backend.database.seed import seed_database

        async with async_engine.begin() as conn: # Corrected to use async_engine
            await conn.run_sync(Base.metadata.create_all)

        print("Database tables created")
        await seed_database()
        print("Database seeded with initial data")

        print("\nDatabase initialization complete!")
        print("You can now access:")
        print("   - Web Dashboard: http://localhost:8000/")
        print("   - API Documentation: http://localhost:8000/docs")
        print("   - Health Check: http://localhost:8000/health")
        print("\nDefault login credentials:")
        print("   Email: admin@example.com")
        print("   Password: password123")

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
