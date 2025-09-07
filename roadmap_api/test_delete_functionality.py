#!/usr/bin/env python3
"""
Test delete roadmap functionality
"""
import requests

def test_delete_functionality():
    print('Testing delete roadmap endpoint...')

    # First, let's get a user roadmap to delete
    try:
        response = requests.get('http://localhost:8000/api/roadmap/roadmaps/user/test_user_123')
        if response.status_code == 200:
            roadmaps = response.json()
            print(f'Found {len(roadmaps["roadmaps"])} roadmaps for test_user_123')
            
            if roadmaps['roadmaps']:
                roadmap_to_delete = roadmaps['roadmaps'][0]
                print(f'Testing delete for roadmap: {roadmap_to_delete["goal"]} (ID: {roadmap_to_delete["_id"]})')
                
                # Test delete
                delete_response = requests.delete(f'http://localhost:8000/api/roadmap/roadmaps/{roadmap_to_delete["_id"]}', 
                    params={'user_id': 'test_user_123'})
                
                print(f'Delete response status: {delete_response.status_code}')
                if delete_response.status_code == 200:
                    print('✅ Delete successful!')
                    print(f'Response: {delete_response.json()}')
                    
                    # Verify it's deleted
                    verify_response = requests.get('http://localhost:8000/api/roadmap/roadmaps/user/test_user_123')
                    if verify_response.status_code == 200:
                        remaining_roadmaps = verify_response.json()
                        print(f'Remaining roadmaps: {len(remaining_roadmaps["roadmaps"])}')
                else:
                    print(f'❌ Delete failed: {delete_response.text}')
            else:
                print('No roadmaps found to test delete')
        else:
            print(f'Error getting roadmaps: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    test_delete_functionality()
