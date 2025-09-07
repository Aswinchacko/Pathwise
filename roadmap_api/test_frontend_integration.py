#!/usr/bin/env python3
"""
Test the frontend integration by simulating the exact API calls the frontend makes
"""
import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_frontend_integration():
    """Test the exact API calls the frontend makes"""
    print("Testing Frontend Integration...")
    
    # Test 1: Get domains (like the frontend does)
    print("\n1. Testing domains endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/roadmap/roadmaps/domains")
        domains = response.json()
        print(f"✓ Domains: {len(domains['domains'])} found")
        print(f"  Sample: {domains['domains'][:3]}")
    except Exception as e:
        print(f"✗ Domains failed: {e}")
        return
    
    # Test 2: Generate roadmap (like the frontend does)
    print("\n2. Testing roadmap generation...")
    test_cases = [
        {"goal": "become a python developer", "domain": "Backend Development"},
        {"goal": "become a frontend developer", "domain": "Frontend Development"},
        {"goal": "become a data scientist", "domain": "Data Science"},
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
                print(f"    ✓ Generated roadmap with {len(roadmap['steps'])} steps")
                print(f"    ✓ Domain: {roadmap['domain']}")
                print(f"    ✓ Goal: {roadmap['goal']}")
                
                # Show first step details
                if roadmap['steps']:
                    first_step = roadmap['steps'][0]
                    print(f"    ✓ First step: {first_step['category']} - {len(first_step['skills'])} skills")
                    print(f"      Skills: {first_step['skills'][:3]}...")
            else:
                print(f"    ✗ Failed with status {response.status_code}")
                print(f"    Error: {response.text}")
                
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    # Test 3: Test user roadmaps (simulate saving)
    print("\n3. Testing user roadmaps...")
    try:
        # Generate a roadmap with user_id
        response = requests.post(
            f"{API_BASE_URL}/api/roadmap/generate-roadmap",
            json={
                "goal": "become a full stack developer",
                "domain": "Frontend Development",
                "user_id": "test_user_123"
            }
        )
        
        if response.status_code == 200:
            roadmap = response.json()
            print(f"    ✓ Generated roadmap for user: {roadmap['id']}")
            
            # Get user roadmaps
            user_response = requests.get(f"{API_BASE_URL}/api/roadmap/roadmaps/user/test_user_123")
            if user_response.status_code == 200:
                user_roadmaps = user_response.json()
                print(f"    ✓ User has {len(user_roadmaps['roadmaps'])} saved roadmaps")
            else:
                print(f"    ✗ Failed to get user roadmaps: {user_response.status_code}")
        else:
            print(f"    ✗ Failed to generate roadmap: {response.status_code}")
            
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    print("\n✅ Frontend integration test completed!")

if __name__ == "__main__":
    test_frontend_integration()
