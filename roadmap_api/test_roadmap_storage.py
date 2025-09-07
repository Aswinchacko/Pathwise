#!/usr/bin/env python3
"""
Test roadmap storage and update functionality
"""
import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_roadmap_storage():
    """Test roadmap storage and update functionality"""
    print("Testing Roadmap Storage and Updates...")
    
    # Test 1: Generate first roadmap
    print("\n1. Generating first roadmap...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/roadmap/generate-roadmap",
            json={
                "goal": "become a python developer",
                "domain": "Backend Development",
                "user_id": "test_user_123"
            }
        )
        
        if response.status_code == 200:
            roadmap1 = response.json()
            print(f"    ✓ Generated roadmap: {roadmap1['id']}")
            print(f"    ✓ Domain: {roadmap1['domain']}")
            print(f"    ✓ Steps: {len(roadmap1['steps'])}")
        else:
            print(f"    ✗ Failed: {response.status_code}")
            return
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return
    
    # Wait a moment
    time.sleep(2)
    
    # Test 2: Generate same roadmap again (should update)
    print("\n2. Generating same roadmap again (should update)...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/roadmap/generate-roadmap",
            json={
                "goal": "become a python developer",
                "domain": "Data Science",  # Different domain
                "user_id": "test_user_123"
            }
        )
        
        if response.status_code == 200:
            roadmap2 = response.json()
            print(f"    ✓ Updated roadmap: {roadmap2['id']}")
            print(f"    ✓ New domain: {roadmap2['domain']}")
            print(f"    ✓ Steps: {len(roadmap2['steps'])}")
            
            # Check if same ID (should be updated, not new)
            if roadmap1['id'] == roadmap2['id']:
                print(f"    ✓ Same roadmap ID - updated successfully")
            else:
                print(f"    ✗ Different roadmap ID - created new instead of updating")
        else:
            print(f"    ✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    # Test 3: Generate different roadmap (should create new)
    print("\n3. Generating different roadmap (should create new)...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/roadmap/generate-roadmap",
            json={
                "goal": "become a frontend developer",
                "domain": "Frontend Development",
                "user_id": "test_user_123"
            }
        )
        
        if response.status_code == 200:
            roadmap3 = response.json()
            print(f"    ✓ Generated new roadmap: {roadmap3['id']}")
            print(f"    ✓ Domain: {roadmap3['domain']}")
            print(f"    ✓ Steps: {len(roadmap3['steps'])}")
        else:
            print(f"    ✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    # Test 4: Get user roadmaps
    print("\n4. Getting user roadmaps...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/roadmap/roadmaps/user/test_user_123")
        if response.status_code == 200:
            user_roadmaps = response.json()
            print(f"    ✓ User has {len(user_roadmaps['roadmaps'])} roadmaps")
            for roadmap in user_roadmaps['roadmaps']:
                print(f"      - {roadmap['goal']} ({roadmap['domain']}) - Gen #{roadmap.get('generation_count', 1)}")
        else:
            print(f"    ✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    # Test 5: Get all generated roadmaps
    print("\n5. Getting all generated roadmaps...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/roadmap/roadmaps/all")
        if response.status_code == 200:
            all_roadmaps = response.json()
            print(f"    ✓ Total roadmaps in database: {all_roadmaps['total']}")
            print(f"    ✓ Showing {len(all_roadmaps['roadmaps'])} roadmaps")
            for roadmap in all_roadmaps['roadmaps'][:3]:  # Show first 3
                print(f"      - {roadmap['goal']} by user {roadmap.get('user_id', 'N/A')} - Gen #{roadmap.get('generation_count', 1)}")
        else:
            print(f"    ✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    print("\n✅ Roadmap storage test completed!")

if __name__ == "__main__":
    test_roadmap_storage()
