import requests
import json

# Test if resumes are being stored in MongoDB
BASE_URL = "http://localhost:8001"

def test_simple_resume_storage():
    """Test storing a simple resume"""
    sample_resume = """
John Smith
Software Engineer
john.smith@email.com
(555) 123-4567
San Francisco, CA

SUMMARY
Experienced software engineer with 5+ years of experience.

EXPERIENCE
Senior Software Engineer - Tech Corp
Jan 2020 - Present
• Led development of microservices

EDUCATION
Bachelor of Computer Science - University of California
2014 - 2018

SKILLS
Python, JavaScript, React, Node.js
"""
    
    try:
        # Test parsing text
        print("Testing text parsing...")
        response = requests.post(
            f"{BASE_URL}/parse-text",
            json={"text": sample_resume}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Text parsing successful!")
            print(f"Name: {data['data']['name']}")
            print(f"Email: {data['data']['email']}")
            return True
        else:
            print(f"❌ Text parsing failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_file_upload_storage():
    """Test file upload and storage"""
    try:
        # Create test file content
        test_content = """
Jane Doe
Data Scientist
jane.doe@email.com
(555) 987-6543
New York, NY

SUMMARY
Data scientist with ML expertise.

SKILLS
Python, R, Machine Learning, TensorFlow
"""
        
        print("\nTesting file upload...")
        files = {"file": ("test.txt", test_content, "text/plain")}
        data = {"user_id": "test_user_123"}
        
        response = requests.post(
            f"{BASE_URL}/parse",
            files=files,
            data=data
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ File upload and storage successful!")
                print(f"Name: {result['data']['name']}")
                return True
            else:
                print(f"❌ File upload failed: {result['error']}")
                return False
        else:
            print(f"❌ File upload failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_stored_resumes():
    """Test retrieving stored resumes"""
    try:
        print("\nTesting resume retrieval...")
        response = requests.get(f"{BASE_URL}/resumes")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Resume retrieval successful!")
            print(f"Number of resumes: {len(data['resumes'])}")
            
            for i, resume in enumerate(data['resumes']):
                print(f"Resume {i+1}: {resume['parsed_data']['name']} - {resume['file_name']}")
            
            return True
        else:
            print(f"❌ Resume retrieval failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Resume Storage in MongoDB...")
    print("=" * 50)
    
    # Test health first
    try:
        health_response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {health_response.json()}")
    except Exception as e:
        print(f"❌ Cannot connect to service: {e}")
        exit(1)
    
    # Run tests
    tests = [
        test_simple_resume_storage,
        test_file_upload_storage,
        test_get_stored_resumes
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! Resumes are being stored in MongoDB.")
    else:
        print("❌ Some tests failed. Check the logs above.")
