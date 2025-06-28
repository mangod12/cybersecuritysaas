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
        print("🗄️  Initializing database...")
        
        # Import after path is set
        from backend.database.db import engine, Base
        from backend.models import user, asset, alert
        
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ Database tables created successfully")
        
        # Import and run seeding
        from backend.database.seed import init_db
        await init_db()
        
        print("✅ Sample data seeded successfully")
        print("\n👤 Sample user created:")
        print("   Email: admin@example.com")
        print("   Password: password123")
        
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main initialization function."""
    print("🚀 CVE Alert SaaS - Database Initialization")
    print("=" * 45)
    
    success = await create_database()
    
    if success:
        print("\n🎉 Database initialization complete!")
        print("\n🌐 Your CVE Alert SaaS is ready:")
        print("   • Dashboard: http://localhost:8000/")
        print("   • API Docs:  http://localhost:8000/docs")
        print("   • Health:    http://localhost:8000/health")
    else:
        print("\n❌ Database initialization failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
