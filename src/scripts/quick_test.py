#!/usr/bin/env python3

import requests
import json
import time

def test_complete_system():
    """Test the complete system"""
    print("🧪 Testing Complete Product Review Sentiment Scraper System")
    print("=" * 60)
    
    # Test backend
    print("\n1. Testing Backend API...")
    try:
        # Health check
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check passed")
        else:
            print("❌ Backend health check failed")
            return False
        
        # API test
        payload = {"product_url": "https://www.daraz.pk/products/test"}
        response = requests.post("http://localhost:8000/scrape", json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API test passed - {data.get('total_reviews', 0)} reviews processed")
        else:
            print("❌ API test failed")
            return False
            
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False
    
    # Test frontend
    print("\n2. Testing Frontend...")
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
        else:
            print("❌ Frontend test failed")
            return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False
    
    print("\n🎉 All tests passed!")
    print("✅ System is working correctly!")
    return True

if __name__ == "__main__":
    if test_complete_system():
        print("\n🚀 You can now use the application at http://localhost:3000")
    else:
        print("\n❌ System test failed!")
        print("💡 Make sure both servers are running:")
        print("   Backend: python scripts/run_complete_setup.py")
