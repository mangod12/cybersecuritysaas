"""
verify_deployment.py - CyberSec Alert SaaS

This script verifies that the local deployment is working:
- Checks server health
- Checks API documentation
- Tests user registration, login, and asset endpoints

Intended for local deployment verification and CI/CD pipelines.

Usage:
    python scripts/verify_deployment.py
"""

import requests
import json
import sys
import time

def test_deployment():
    """Test the local deployment."""
    print("🚀 CVE Alert SaaS - Local Deployment Verification")
    print("=" * 55)
    
    # Test server health
    print("🏥 Testing server health...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Server is healthy: {health_data}")
        else:
            print(f"❌ Health check failed: Status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure the server is running with:")
        print("   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload")
        return False
    
    # Test API documentation
    print("\n📖 Testing API documentation...")
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API documentation is accessible")
        else:
            print(f"❌ API docs failed: Status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  API docs test failed: {e}")
    
    # Test registration endpoint
    print("\n👤 Testing user registration...")
    user_data = {
        "email": f"test_{int(time.time())}@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "company": "Test Company"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/v1/auth/register", json=user_data, timeout=5)
        if response.status_code == 201:
            print("✅ User registration working")
            
            # Test login
            print("\n🔐 Testing user login...")
            login_data = {
                "username": user_data["email"],
                "password": user_data["password"]
            }
            
            response = requests.post("http://localhost:8000/api/v1/auth/login", data=login_data, timeout=5)
            if response.status_code == 200:
                token_data = response.json()
                print("✅ User login working")
                
                # Test authenticated endpoint
                headers = {"Authorization": f"Bearer {token_data['access_token']}"}
                response = requests.get("http://localhost:8000/api/v1/assets/", headers=headers, timeout=5)
                if response.status_code == 200:
                    print("✅ Authentication working")
                else:
                    print(f"⚠️  Authentication test failed: Status {response.status_code}")
            else:
                print(f"⚠️  Login test failed: Status {response.status_code}")
        else:
            print(f"⚠️  Registration test failed: Status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Authentication tests failed: {e}")
    
    print("\n🎉 Deployment verification completed!")
    print("\n🌐 Your CVE Alert SaaS is now deployed locally:")
    print("   • 🏠 Dashboard:        http://localhost:8000/")
    print("   • 📖 API Documentation: http://localhost:8000/docs")
    print("   • ❤️  Health Check:     http://localhost:8000/health")
    print("   • 🔄 Alternative Docs:  http://localhost:8000/redoc")
    
    print("\n📋 Next Steps:")
    print("   1. Open the dashboard: http://localhost:8000/")
    print("   2. Create an account or login")
    print("   3. Add your IT assets for monitoring")
    print("   4. Configure email alerts in the .env file")
    print("   5. The system will automatically scan for vulnerabilities")
    
    print("\n⚠️  Note: To stop the server, press Ctrl+C in the terminal running uvicorn")
    
    return True

if __name__ == "__main__":
    success = test_deployment()
    sys.exit(0 if success else 1)
