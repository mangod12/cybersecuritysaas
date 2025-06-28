"""Simple test script to debug import issues."""

import sys
import traceback

print("Testing imports...")

try:
    print("1. Testing dotenv...")
    from dotenv import load_dotenv
    print("   ✅ dotenv imported")
    
    print("2. Testing pydantic-settings...")
    from pydantic_settings import BaseSettings
    from pydantic import Field
    print("   ✅ pydantic-settings imported")
    
    print("3. Testing config...")
    sys.path.append('.')
    from backend.config import settings
    print(f"   ✅ Config loaded: {settings.app_name}")
    
    print("4. Testing database...")
    from backend.database.db import engine
    print("   ✅ Database imported")
    
    print("5. Testing models...")
    from backend.models.user import User
    from backend.models.asset import Asset
    print("   ✅ Models imported")
    
    print("6. Testing FastAPI app...")
    from backend.main import app
    print("   ✅ FastAPI app imported")
    
    print("\n🎉 All imports successful!")
    
except Exception as e:
    print(f"\n❌ Import failed: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
