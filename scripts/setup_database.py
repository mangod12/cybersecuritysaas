"""
Database initialization for local deployment.
Creates tables and seeds sample data.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent # Modified path
sys.path.insert(0, str(project_root))

async def create_database():
    """Create database tables and seed data."""
    try:
        print("Initializing database...")
        
        # Import after path is set
        from backend.database.db import get_async_engine, Base
        from backend.models import user, asset, alert
        
        # Get the async engine
        async_engine = get_async_engine()
        
        # Create all tables
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("Database tables created successfully")
        
        # Import and run seeding
        from backend.database.seed import seed_database
        await seed_database()
        
        print("Sample data seeded successfully")
        print("\nSample user created:")
        print("   Email: admin@example.com")
        print("   Password: password123")
        
        return True
        
    except Exception as e:
        print(f"Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main initialization function."""
    print("CVE Alert SaaS - Database Initialization")
    print("=" * 45)
    
    success = await create_database()
    
    if success:
        print("\nDatabase initialization complete!")
        print("\nYour CVE Alert SaaS is ready:")
        print("   • Dashboard: http://localhost:8000/")
        print("   • API Docs:  http://localhost:8000/docs")
        print("   • Health:    http://localhost:8000/health")
    else:
        print("\nDatabase initialization failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
