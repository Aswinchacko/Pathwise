#!/usr/bin/env python3
"""
Test the final API with MongoDB data
"""
import requests
import json

def test_api():
    print('=== TESTING API WITH MONGODB DATA ===')

    # Test 1: Generate roadmap
    print('\n1. Testing roadmap generation...')
    try:
        response = requests.post('http://localhost:8000/api/roadmap/generate-roadmap', 
            json={'goal': 'become a react developer', 'user_id': 'test_user_789'})
        
        if response.status_code == 200:
            roadmap = response.json()
            print('✅ Generated roadmap successfully:')
            print(f'   ID: {roadmap["id"]}')
            print(f'   Title: {roadmap["title"]}')
            print(f'   Domain: {roadmap["domain"]}')
            print(f'   Steps: {len(roadmap["steps"])} categories')
        else:
            print(f'❌ Error: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'❌ Exception: {e}')

    # Test 2: Get domains
    print('\n2. Testing domains endpoint...')
    try:
        response = requests.get('http://localhost:8000/api/roadmap/roadmaps/domains')
        if response.status_code == 200:
            domains = response.json()
            print(f'✅ Found {len(domains["domains"])} domains')
            print(f'   Sample domains: {domains["domains"][:5]}')
        else:
            print(f'❌ Error: {response.status_code}')
    except Exception as e:
        print(f'❌ Exception: {e}')

    # Test 3: Get user roadmaps
    print('\n3. Testing user roadmaps...')
    try:
        response = requests.get('http://localhost:8000/api/roadmap/roadmaps/user/test_user_789')
        if response.status_code == 200:
            user_roadmaps = response.json()
            print(f'✅ Found {len(user_roadmaps["roadmaps"])} user roadmaps')
            for roadmap in user_roadmaps['roadmaps']:
                print(f'   - {roadmap["title"]} ({roadmap["domain"]})')
        else:
            print(f'❌ Error: {response.status_code}')
    except Exception as e:
        print(f'❌ Exception: {e}')

    # Test 4: Get all roadmaps
    print('\n4. Testing all roadmaps...')
    try:
        response = requests.get('http://localhost:8000/api/roadmap/roadmaps/all?limit=3')
        if response.status_code == 200:
            all_roadmaps = response.json()
            print(f'✅ Found {all_roadmaps["total"]} total roadmaps')
            print(f'   Showing {len(all_roadmaps["roadmaps"])} roadmaps:')
            for roadmap in all_roadmaps['roadmaps']:
                print(f'   - {roadmap["title"]} by user {roadmap.get("user_id", "N/A")}')
        else:
            print(f'❌ Error: {response.status_code}')
    except Exception as e:
        print(f'❌ Exception: {e}')

if __name__ == "__main__":
    test_api()
