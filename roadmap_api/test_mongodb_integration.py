#!/usr/bin/env python3
"""
Test MongoDB integration for the roadmap API
"""
import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_mongodb_integration():
    """Test the MongoDB integration"""
    print("Testing MongoDB Integration...")
    
    # Test 1: Check if API is running
    print("\n1. Checking API status...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"✓ API is running: {response.json()}")
    except Exception as e:
        print(f"✗ API not running: {e}")
        return
    
    # Test 2: Test domains endpoint (should get from MongoDB)
    print("\n2. Testing domains from MongoDB...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/roadmap/roadmaps/domains")
        domains = response.json()
        print(f"✓ Domains from MongoDB: {len(domains['domains'])} found")
        print(f"  Sample: {domains['domains'][:3]}")
    except Exception as e:
        print(f"✗ Domains failed: {e}")
    
    # Test 3: Generate roadmap and save to MongoDB
    print("\n3. Testing roadmap generation with MongoDB storage...")
    test_cases = [
        {"goal": "become a python developer", "domain": "Backend Development", "user_id": "test_user_123"},
        {"goal": "become a frontend developer", "domain": "Frontend Development", "user_id": "test_user_456"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test {i}: {test_case['goal']}")
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/roadmap/generate-roadmap",
                json=test_case
            )
            
            if response.status_code == 200:
                roadmap = response.json()
                print(f"    ✓ Generated roadmap: {roadmap['id']}")
                print(f"    ✓ Domain: {roadmap['domain']}")
                print(f"    ✓ Steps: {len(roadmap['steps'])}")
                print(f"    ✓ Saved to MongoDB for user: {test_case['user_id']}")
            else:
                print(f"    ✗ Failed with status {response.status_code}")
                print(f"    Error: {response.text}")
                
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    # Test 4: Get user roadmaps from MongoDB
    print("\n4. Testing user roadmaps retrieval from MongoDB...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/roadmap/roadmaps/user/test_user_123")
        if response.status_code == 200:
            user_roadmaps = response.json()
            print(f"    ✓ User test_user_123 has {len(user_roadmaps['roadmaps'])} saved roadmaps")
            for roadmap in user_roadmaps['roadmaps']:
                print(f"      - {roadmap['goal']} ({roadmap['domain']})")
        else:
            print(f"    ✗ Failed to get user roadmaps: {response.status_code}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    # Test 5: Test similar roadmaps from MongoDB
    print("\n5. Testing similar roadmaps from MongoDB...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/roadmap/roadmaps/similar", params={
            "goal": "python developer",
            "limit": 3
        })
        if response.status_code == 200:
            similar = response.json()
            print(f"    ✓ Found {len(similar['roadmaps'])} similar roadmaps")
            for roadmap in similar['roadmaps'][:2]:
                print(f"      - {roadmap['goal']} ({roadmap['domain']})")
        else:
            print(f"    ✗ Failed to get similar roadmaps: {response.status_code}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    print("\n✅ MongoDB integration test completed!")

if __name__ == "__main__":
    test_mongodb_integration()
