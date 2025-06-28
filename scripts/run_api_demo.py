"""
run_api_demo.py - CyberSec Alert SaaS

This script demonstrates the core API functionality:
- Health check
- User registration
- User login
- Asset management (create/list)

Intended for local development and demo purposes.

Usage:
    python scripts/run_api_demo.py
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"✅ Health check passed: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_registration():
    """Test user registration."""
    print("\n👤 Testing user registration...")
    user_data = {
        "email": "demo@example.com",
        "password": "demopassword123",
        "full_name": "Demo User",
        "company": "Demo Company"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code == 200:
            print(f"✅ Registration successful: {response.json()}")
            return response.json()
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_login():
    """Test user login."""
    print("\n🔐 Testing user login...")
    login_data = {
        "username": "demo@example.com",
        "password": "demopassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Login successful: Token received")
            return token_data["access_token"]
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_asset_management(token):
    """Test asset management endpoints."""
    print("\n💻 Testing asset management...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create an asset
    asset_data = {
        "name": "Demo Server",
        "asset_type": "server",
        "vendor": "Microsoft",
        "product": "Windows Server",
        "version": "2019",
        "cpe": "cpe:2.3:o:microsoft:windows_server_2019:*:*:*:*:*:*:*:*"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/assets/", json=asset_data, headers=headers)
        if response.status_code == 200:
            asset = response.json()
            print(f"✅ Asset created: {asset['name']}")
            
            # List assets
            response = requests.get(f"{BASE_URL}/assets/", headers=headers)
            if response.status_code == 200:
                assets = response.json()
                print(f"✅ Assets listed: {len(assets)} assets found")
                return asset["id"]
            else:
                print(f"❌ Asset listing failed: {response.status_code}")
        else:
            print(f"❌ Asset creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Asset management error: {e}")
        return None

def test_alerts(token):
    """Test alerts endpoint."""
    print("\n🚨 Testing alerts...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/alerts/", headers=headers)
        if response.status_code == 200:
            alerts = response.json()
            print(f"✅ Alerts retrieved: {len(alerts)} alerts found")
            return True
        else:
            print(f"❌ Alerts retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Alerts error: {e}")
        return False

def test_api_docs():
    """Test API documentation endpoint."""
    print("\n📖 Testing API documentation...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API documentation accessible")
            return True
        else:
            print(f"❌ API docs failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API docs error: {e}")
        return False

def main():
    """Run the API demo."""
    print("🚀 CVE Alert SaaS - API Demo")
    print("=" * 40)
    
    # Test health
    if not test_health():
        print("❌ Server is not responding. Please start the server first.")
        return
    
    # Test API docs
    test_api_docs()
    
    # Test registration
    registration_result = test_registration()
    if not registration_result:
        print("⚠️  Registration failed, trying to login with existing account...")
    
    # Test login
    token = test_login()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    # Test asset management
    asset_id = test_asset_management(token)
    
    # Test alerts
    test_alerts(token)
    
    print("\n🎉 API Demo completed!")
    print("\n🌐 You can explore more at:")
    print(f"   • Dashboard: {BASE_URL}/")
    print(f"   • API Docs: {BASE_URL}/docs")
    print(f"   • Interactive API: {BASE_URL}/redoc")

if __name__ == "__main__":
    main()
