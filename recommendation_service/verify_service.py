#!/usr/bin/env python3
"""
Verify that the recommendation service is working
"""

import requests
import json
import time

def main():
    print("🔍 Verifying Recommendation Service")
    print("=" * 40)
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8002/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check passed: {data['status']}")
            print(f"   📊 Total projects: {data.get('total_projects', 'Unknown')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to service: {e}")
        print("   💡 Make sure the service is running on port 8002")
        return False
    
    # Test recommendations endpoint
    print("\n2. Testing recommendations...")
    try:
        test_data = {
            "goal": "I want to become a full-stack developer",
            "domain": "web-development",
            "difficulty": "intermediate",
            "limit": 3
        }
        
        response = requests.post("http://localhost:8002/api/recommend/projects", 
                               json=test_data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('recommendations', [])
            print(f"   ✅ Got {len(recommendations)} recommendations")
            
            if recommendations:
                first_rec = recommendations[0]
                print(f"   📝 First recommendation: {first_rec['title']}")
                print(f"   🏷️  Technologies: {', '.join(first_rec['technologies'][:3])}")
        else:
            print(f"   ❌ Recommendations failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing recommendations: {e}")
        return False
    
    # Test search endpoint
    print("\n3. Testing search...")
    try:
        response = requests.get("http://localhost:8002/api/recommend/projects/search?query=React&limit=2", 
                              timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('search_results', [])
            print(f"   ✅ Search found {len(results)} results")
        else:
            print(f"   ❌ Search failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing search: {e}")
        return False
    
    print("\n🎉 All tests passed! Service is working correctly.")
    print("\n📖 API Documentation: http://localhost:8002/docs")
    print("🔧 Alternative Docs: http://localhost:8002/redoc")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Service verification failed.")
        print("💡 Try starting the service with: python main.py")
        exit(1)
