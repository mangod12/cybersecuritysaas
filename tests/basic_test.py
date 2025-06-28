import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

print("Testing basic Python setup...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path[:3]}")

try:
    import pydantic
    print(f"Pydantic version: {pydantic.__version__}")
except ImportError as e:
    print(f"Pydantic import error: {e}")

try:
    import fastapi
    print(f"FastAPI version: {fastapi.__version__}")
except ImportError as e:
    print(f"FastAPI import error: {e}")

try:
    import uvicorn
    print(f"Uvicorn available")
except ImportError as e:
    print(f"Uvicorn import error: {e}")

print("\nTesting config import...")
try:
    from backend.config import Settings
    settings = Settings()
    print(f"✅ Config loaded successfully: {settings.app_name}")
except Exception as e:
    print(f"❌ Config import failed: {e}")
    import traceback
    traceback.print_exc()
