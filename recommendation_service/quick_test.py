"""
Quick test script for the Recommendation API
Run this to verify all endpoints are working
"""

import requests
import json

BASE_URL = "http://localhost:8002"

def test_endpoints():
    print("🧪 Testing Recommendation API Endpoints\n")
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   ✅ Health: {response.status_code} - {response.json()['status']}")
    except Exception as e:
        print(f"   ❌ Health failed: {e}")
    
    # Test 2: Get Categories
    print("\n2. Testing Categories...")
    try:
        response = requests.get(f"{BASE_URL}/api/recommend/categories")
        data = response.json()
        print(f"   ✅ Categories: {len(data['domains'])} domains, {len(data['difficulties'])} difficulties")
    except Exception as e:
        print(f"   ❌ Categories failed: {e}")
    
    # Test 3: Get Recommendations
    print("\n3. Testing Recommendations...")
    test_cases = [
        {
            "goal": "I want to become a full-stack developer",
            "domain": "web-development",
            "difficulty": "intermediate",
            "limit": 3
        },
        {
            "goal": "Learn machine learning",
            "domain": "data-science",
            "difficulty": "beginner",
            "limit": 2
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        try:
            response = requests.post(f"{BASE_URL}/api/recommend/projects", json=test_case)
            data = response.json()
            print(f"   ✅ Test {i+1}: Got {len(data['recommendations'])} recommendations")
            if data['recommendations']:
                print(f"      First: {data['recommendations'][0]['title']}")
        except Exception as e:
            print(f"   ❌ Test {i+1} failed: {e}")
    
    # Test 4: Search
    print("\n4. Testing Search...")
    try:
        response = requests.get(f"{BASE_URL}/api/recommend/projects/search?query=React&limit=2")
        data = response.json()
        print(f"   ✅ Search: Found {len(data['search_results'])} results")
    except Exception as e:
        print(f"   ❌ Search failed: {e}")
    
    # Test 5: Trending
    print("\n5. Testing Trending...")
    try:
        response = requests.get(f"{BASE_URL}/api/recommend/trending?limit=3")
        data = response.json()
        print(f"   ✅ Trending: {len(data['trending_projects'])} projects")
    except Exception as e:
        print(f"   ❌ Trending failed: {e}")
    
    # Test 6: Statistics
    print("\n6. Testing Statistics...")
    try:
        response = requests.get(f"{BASE_URL}/api/recommend/statistics")
        data = response.json()
        print(f"   ✅ Statistics: {len(data['domains'])} domains, {len(data['technologies'])} technologies")
    except Exception as e:
        print(f"   ❌ Statistics failed: {e}")
    
    # Test 7: Feedback
    print("\n7. Testing Feedback...")
    try:
        feedback_data = {
            "user_id": "test_user",
            "project_id": "web_001",
            "rating": 5,
            "feedback": "Great project!"
        }
        response = requests.post(f"{BASE_URL}/api/recommend/feedback", json=feedback_data)
        print(f"   ✅ Feedback: {response.status_code} - {response.json()['message']}")
    except Exception as e:
        print(f"   ❌ Feedback failed: {e}")
    
    print("\n🎉 Testing Complete!")
    print(f"\n📖 API Documentation: {BASE_URL}/docs")
    print(f"🔧 Alternative Docs: {BASE_URL}/redoc")

if __name__ == "__main__":
    test_endpoints()

