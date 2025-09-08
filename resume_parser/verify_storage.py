import requests
import json
import time

def test_resume_storage():
    """Test if resumes are being stored by checking the API responses"""
    
    # Wait for service to start
    print("Waiting for service to start...")
    time.sleep(5)
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:8001/health", timeout=10)
        if response.status_code == 200:
            print("✅ Service is running")
            print(f"Health: {response.json()}")
        else:
            print(f"❌ Service health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to service: {e}")
        return False
    
    # Test file upload
    print("\nTesting file upload...")
    test_content = """
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
        files = {"file": ("test.txt", test_content, "text/plain")}
        data = {"user_id": "test_user_123"}
        
        response = requests.post(
            "http://localhost:8001/parse",
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"Upload response status: {response.status_code}")
        print(f"Upload response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Resume uploaded and parsed successfully!")
                print(f"Name: {result['data']['name']}")
                return True
            else:
                print(f"❌ Resume parsing failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Upload failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def test_resume_retrieval():
    """Test retrieving stored resumes"""
    print("\nTesting resume retrieval...")
    
    try:
        response = requests.get("http://localhost:8001/resumes", timeout=10)
        print(f"Retrieval response status: {response.status_code}")
        print(f"Retrieval response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Retrieved {len(result['resumes'])} resumes")
                for i, resume in enumerate(result['resumes']):
                    print(f"  Resume {i+1}: {resume['parsed_data']['name']} - {resume['file_name']}")
                return True
            else:
                print(f"❌ Retrieval failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Retrieval failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Retrieval error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Resume Storage...")
    print("=" * 50)
    
    # Start the service in background
    import subprocess
    import sys
    
    print("Starting resume parser service...")
    process = subprocess.Popen([sys.executable, "main.py"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    
    try:
        # Test storage
        storage_ok = test_resume_storage()
        
        # Test retrieval
        retrieval_ok = test_resume_retrieval()
        
        print("\n" + "=" * 50)
        if storage_ok and retrieval_ok:
            print("🎉 Resume storage is working!")
        else:
            print("❌ Resume storage has issues")
            
    finally:
        # Clean up
        process.terminate()
        process.wait()
        print("Service stopped")
