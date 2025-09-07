#!/usr/bin/env python3
"""
Test complete delete flow
"""
import requests
import time

def test_complete_delete_flow():
    print('=== Testing Complete Delete Flow ===')
    
    # Step 1: Generate a new roadmap
    print('\n1. Generating new roadmap...')
    try:
        response = requests.post('http://localhost:8000/api/roadmap/generate-roadmap', 
            json={'goal': 'test delete functionality', 'user_id': 'test_user_delete'})
        
        if response.status_code == 200:
            roadmap = response.json()
            print(f'✅ Generated roadmap: {roadmap["id"]}')
            roadmap_id = roadmap['id']
        else:
            print(f'❌ Failed to generate roadmap: {response.status_code}')
            return
    except Exception as e:
        print(f'❌ Error generating roadmap: {e}')
        return
    
    # Step 2: Get user roadmaps to verify it's there
    print('\n2. Getting user roadmaps...')
    try:
        response = requests.get('http://localhost:8000/api/roadmap/roadmaps/user/test_user_delete')
        if response.status_code == 200:
            roadmaps = response.json()
            print(f'✅ Found {len(roadmaps["roadmaps"])} roadmaps')
            for roadmap in roadmaps['roadmaps']:
                print(f'  - {roadmap["goal"]} (ID: {roadmap["id"]})')
        else:
            print(f'❌ Failed to get roadmaps: {response.status_code}')
    except Exception as e:
        print(f'❌ Error getting roadmaps: {e}')
    
    # Step 3: Delete the roadmap
    print(f'\n3. Deleting roadmap {roadmap_id}...')
    try:
        delete_response = requests.delete(f'http://localhost:8000/api/roadmap/roadmaps/{roadmap_id}', 
            params={'user_id': 'test_user_delete'})
        
        if delete_response.status_code == 200:
            print('✅ Delete successful!')
            print(f'Response: {delete_response.json()}')
        else:
            print(f'❌ Delete failed: {delete_response.status_code}')
            print(f'Response: {delete_response.text}')
    except Exception as e:
        print(f'❌ Error deleting roadmap: {e}')
    
    # Step 4: Verify it's deleted
    print('\n4. Verifying deletion...')
    try:
        response = requests.get('http://localhost:8000/api/roadmap/roadmaps/user/test_user_delete')
        if response.status_code == 200:
            roadmaps = response.json()
            print(f'✅ Remaining roadmaps: {len(roadmaps["roadmaps"])}')
            if len(roadmaps['roadmaps']) == 0:
                print('✅ Roadmap successfully deleted!')
            else:
                print('❌ Roadmap still exists!')
        else:
            print(f'❌ Failed to verify: {response.status_code}')
    except Exception as e:
        print(f'❌ Error verifying deletion: {e}')

if __name__ == "__main__":
    test_complete_delete_flow()
