"""
Quick test script to verify the application setup.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.getcwd())

try:
    print("🔍 Testing application setup...")
    
    # Test configuration
    from backend.config import settings
    print(f"✅ Configuration loaded: {settings.app_name}")
    
    # Test database setup
    from backend.database.db import Base
    print("✅ Database models imported")
    
    # Test models
    from backend.models.user import User
    from backend.models.asset import Asset
    from backend.models.alert import Alert
    print("✅ All models imported successfully")
    
    # Test services
    from backend.services.cve_scraper import cve_scraper
    from backend.services.vendor_scraper import vendor_scraper
    from backend.services.alert_checker import alert_checker
    print("✅ All services imported successfully")
    
    # Test main app
    from backend.main import app
    print("✅ FastAPI application created successfully")
    
    print("\n🎉 All components loaded successfully!")
    print("The application is ready to run.")
    
except Exception as e:
    print(f"❌ Error during setup test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
