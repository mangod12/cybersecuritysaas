#!/usr/bin/env python3
"""
Deployment script for CyberSec Alert SaaS.
Handles environment setup, database initialization, and server startup.
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

def check_environment():
    """Check if all required environment variables are set."""
    print("🔍 Checking environment...")
    
    required_vars = [
        'GITHUB_CLIENT_ID',
        'GITHUB_CLIENT_SECRET', 
        'GITHUB_REDIRECT_URI'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with the required variables.")
        return False
    
    print("✅ Environment variables configured")
    return True

def check_dependencies():
    """Check if all required Python packages are installed."""
    print("📦 Checking dependencies...")
    
    required_packages = [
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('sqlalchemy', 'sqlalchemy'),
        ('python-jose', 'jose'),
        ('passlib', 'passlib'),
        ('requests', 'requests'),
        ('python-dotenv', 'dotenv')
    ]
    
    missing_packages = []
    for pkg_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(pkg_name)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed")
    return True

def initialize_database():
    """Initialize the database."""
    print("🗄️ Initializing database...")
    
    try:
        result = subprocess.run([sys.executable, 'init_db.py'], 
                              capture_output=True, text=True, check=True)
        print("✅ Database initialized successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Database initialization failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def start_server(host="0.0.0.0", port=8001, reload=True):
    """Start the FastAPI server."""
    print(f"🚀 Starting server on {host}:{port}...")
    
    cmd = [
        sys.executable, '-m', 'uvicorn',
        'backend.main:app',
        '--host', host,
        '--port', str(port)
    ]
    
    if reload:
        cmd.append('--reload')
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return False
    
    return True

def main():
    """Main deployment function."""
    print("🚀 CyberSec Alert SaaS - Deployment")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    print("\n🎉 Deployment successful!")
    print(f"🌐 Application will be available at: http://localhost:8001")
    print(f"📖 API Documentation: http://localhost:8001/docs")
    print(f"❤️ Health Check: http://localhost:8001/health")
    print("\n👤 Default login credentials:")
    print("   Email: admin@example.com")
    print("   Password: password123")
    print("\nPress Ctrl+C to stop the server")
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 