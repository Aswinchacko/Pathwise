#!/usr/bin/env python3
"""
Test script for the Roadmap Generator API
"""
import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_api():
    """Test the API endpoints"""
    print("Testing Roadmap Generator API...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"✓ Root endpoint: {response.json()}")
    except Exception as e:
        print(f"✗ Root endpoint failed: {e}")
        return
    
    # Test domains endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/api/roadmap/roadmaps/domains")
        domains = response.json()
        print(f"✓ Domains endpoint: Found {len(domains['domains'])} domains")
        print(f"  Sample domains: {domains['domains'][:5]}")
    except Exception as e:
        print(f"✗ Domains endpoint failed: {e}")
    
    # Test roadmap generation
    try:
        test_goal = "Become a Full Stack Developer"
        test_domain = "Frontend Development"
        
        payload = {
            "goal": test_goal,
            "domain": test_domain,
            "user_id": "test_user_123"
        }
        
        response = requests.post(f"{API_BASE_URL}/api/roadmap/generate-roadmap", json=payload)
        roadmap = response.json()
        
        print(f"✓ Roadmap generation: Generated roadmap with {len(roadmap['steps'])} steps")
        print(f"  Goal: {roadmap['goal']}")
        print(f"  Domain: {roadmap['domain']}")
        print(f"  First step: {roadmap['steps'][0]['category']} - {len(roadmap['steps'][0]['skills'])} skills")
        
    except Exception as e:
        print(f"✗ Roadmap generation failed: {e}")
    
    # Test similar roadmaps
    try:
        response = requests.get(f"{API_BASE_URL}/api/roadmap/roadmaps/similar", params={
            "goal": "Frontend Developer",
            "limit": 3
        })
        similar = response.json()
        print(f"✓ Similar roadmaps: Found {len(similar['roadmaps'])} similar roadmaps")
        
    except Exception as e:
        print(f"✗ Similar roadmaps failed: {e}")
    
    print("\nAPI test completed!")

if __name__ == "__main__":
    test_api()
