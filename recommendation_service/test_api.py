"""
Test script for the Recommendation API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8002"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_recommendations():
    """Test project recommendations"""
    print("\nTesting project recommendations...")
    
    test_cases = [
        {
            "goal": "I want to become a full-stack developer",
            "domain": "web-development",
            "difficulty": "intermediate",
            "limit": 5
        },
        {
            "goal": "Learn machine learning and data science",
            "domain": "data-science",
            "difficulty": "beginner",
            "limit": 3
        },
        {
            "goal": "Build mobile apps",
            "domain": "mobile-development",
            "limit": 4
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i+1}: {test_case['goal']}")
        try:
            response = requests.post(f"{BASE_URL}/api/recommend/projects", json=test_case)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Got {len(data['recommendations'])} recommendations")
                for j, rec in enumerate(data['recommendations'][:2]):  # Show first 2
                    print(f"  {j+1}. {rec['title']} ({rec['difficulty']}) - Score: {rec.get('final_score', 'N/A')}")
            else:
                print(f"✗ Failed with status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"✗ Error: {e}")

def test_categories():
    """Test categories endpoint"""
    print("\nTesting categories endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/recommend/categories")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Found {len(data['domains'])} domains")
            print(f"  Domains: {', '.join(data['domains'][:5])}...")
            print(f"  Difficulties: {', '.join(data['difficulties'])}")
        else:
            print(f"✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

def test_trending():
    """Test trending projects"""
    print("\nTesting trending projects...")
    try:
        response = requests.get(f"{BASE_URL}/api/recommend/trending?limit=3")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Found {len(data['trending_projects'])} trending projects")
            for i, project in enumerate(data['trending_projects'][:2]):
                print(f"  {i+1}. {project['title']} (Popularity: {project['popularity_score']})")
        else:
            print(f"✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

def test_search():
    """Test project search"""
    print("\nTesting project search...")
    search_queries = ["React", "Python", "Machine Learning", "Mobile App"]
    
    for query in search_queries:
        print(f"\nSearching for: '{query}'")
        try:
            response = requests.get(f"{BASE_URL}/api/recommend/projects/search?query={query}&limit=2")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Found {len(data['search_results'])} results")
                for i, project in enumerate(data['search_results'][:1]):
                    print(f"  {i+1}. {project['title']} (Similarity: {project.get('similarity_score', 'N/A')})")
            else:
                print(f"✗ Failed with status {response.status_code}")
        except Exception as e:
            print(f"✗ Error: {e}")

def test_feedback():
    """Test feedback submission"""
    print("\nTesting feedback submission...")
    try:
        feedback_data = {
            "user_id": "test_user_123",
            "project_id": "web_001",
            "rating": 5,
            "feedback": "Great project for beginners!"
        }
        
        response = requests.post(f"{BASE_URL}/api/recommend/feedback", json=feedback_data)
        if response.status_code == 200:
            print("✓ Feedback submitted successfully")
        else:
            print(f"✗ Failed with status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")

def test_statistics():
    """Test statistics endpoint"""
    print("\nTesting statistics endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/recommend/statistics")
        if response.status_code == 200:
            data = response.json()
            print("✓ Statistics retrieved successfully")
            print(f"  Total domains: {len(data['domains'])}")
            print(f"  Difficulty distribution: {data['difficulties']}")
        else:
            print(f"✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

def main():
    """Run all tests"""
    print("=" * 50)
    print("RECOMMENDATION API TEST SUITE")
    print("=" * 50)
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    # Run tests
    tests = [
        test_health,
        test_categories,
        test_recommendations,
        test_trending,
        test_search,
        test_feedback,
        test_statistics
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
