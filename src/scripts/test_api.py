#!/usr/bin/env python3

import requests
import json
import time
import sys

def wait_for_server(url, timeout=30):
    """Wait for server to be available"""
    print(f"⏳ Waiting for server at {url}...")
    
    for i in range(timeout):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"✅ Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        if i % 5 == 0:  # Print progress every 5 seconds
            print(f"   Still waiting... ({i+1}/{timeout}s)")
    
    print(f"❌ Server not available after {timeout} seconds")
    return False

def test_api():
    """Test the FastAPI backend"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Product Review Sentiment Scraper API...")
    print("=" * 50)
    
    # Wait for server to be available
    if not wait_for_server(f"{base_url}/health"):
        print("❌ Backend server is not running!")
        print("💡 Please start the backend server first:")
        print("   python scripts/start_backend.py")
        return False
    
    # Test health endpoint
    try:
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Service: {data.get('service', 'unknown')}")
            print(f"   Version: {data.get('version', 'unknown')}")
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test root endpoint
    try:
        print("\n2. Testing root endpoint...")
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint passed")
            print(f"   Message: {data.get('message', 'No message')}")
            print(f"   Version: {data.get('version', 'unknown')}")
        else:
            print(f"❌ Root endpoint failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False
    
    # Test scrape endpoint
    try:
        print("\n3. Testing scrape endpoint...")
        payload = {"product_url": "https://www.daraz.pk/products/test-product"}
        response = requests.post(f"{base_url}/scrape", json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Scrape endpoint passed")
            print(f"   Success: {data.get('success', False)}")
            print(f"   Total reviews: {data.get('total_reviews', 0)}")
            print(f"   Message: {data.get('message', 'No message')}")
            
            # Check data structure
            reviews = data.get('data', [])
            if reviews and len(reviews) > 0:
                sample_review = reviews[0]
                print("   Sample review structure:")
                for key, value in sample_review.items():
                    print(f"     {key}: {type(value).__name__} = {str(value)[:50]}{'...' if len(str(value)) > 50 else ''}")
                
                # Check sentiment distribution
                sentiments = {}
                for review in reviews:
                    sentiment = review.get('sentiment_label', 'Unknown')
                    sentiments[sentiment] = sentiments.get(sentiment, 0) + 1
                
                print("   Sentiment distribution:")
                for sentiment, count in sentiments.items():
                    print(f"     {sentiment}: {count}")
                
                print("✅ Data structure is valid")
            else:
                print("❌ No review data returned")
                return False
        else:
            print(f"❌ Scrape endpoint failed: HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Scrape endpoint error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All API tests passed!")
    print("✅ Backend is working correctly!")
    print("\n💡 Next steps:")
    print("   1. Open http://localhost:3000 in your browser")
    print("   2. Enter a product URL and click 'Scrape Reviews'")
    print("   3. View the sentiment analysis results")
    return True

if __name__ == "__main__":
    if test_api():
        print("\n🚀 You can now use the application!")
        sys.exit(0)
    else:
        print("\n❌ API tests failed!")
        print("💡 Troubleshooting:")
        print("   1. Make sure Python backend is running: python scripts/start_backend.py")
        print("   2. Check if port 8000 is available: lsof -i :8000")
        print("   3. Check backend logs for errors")
        sys.exit(1)
