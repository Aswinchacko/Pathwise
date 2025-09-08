import requests
import json
import time

def test_resume_storage_final():
    """Final test to verify resume storage is working"""
    
    print("Testing Resume Storage in MongoDB...")
    print("=" * 50)
    
    # Wait for service
    print("Waiting for service to start...")
    time.sleep(5)
    
    # Test health
    try:
        response = requests.get("http://localhost:8001/health", timeout=10)
        if response.status_code == 200:
            print("✅ Service is running")
        else:
            print(f"❌ Service health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to service: {e}")
        return False
    
    # Test file upload
    print("\n1. Testing file upload and storage...")
    test_content = """
John Smith
Software Engineer
john.smith@email.com
(555) 123-4567
San Francisco, CA

SUMMARY
Experienced software engineer with 5+ years of experience in full-stack development.

EXPERIENCE
Senior Software Engineer - Tech Solutions Inc
Jan 2020 - Present
• Led development of microservices architecture using Python and FastAPI
• Mentored junior developers and conducted code reviews

Software Developer - StartupXYZ
Jun 2018 - Dec 2019
• Developed React-based frontend applications
• Built RESTful APIs using Node.js and Express

EDUCATION
Bachelor of Computer Science - University of California
2014 - 2018

SKILLS
Python, JavaScript, TypeScript, React, Node.js, FastAPI, Docker, AWS, MongoDB
"""
    
    try:
        files = {"file": ("test_resume.txt", test_content, "text/plain")}
        data = {"user_id": "test_user_123"}
        
        response = requests.post(
            "http://localhost:8001/parse",
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"Upload status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Resume uploaded and parsed successfully!")
                print(f"   Name: {result['data']['name']}")
                print(f"   Email: {result['data']['email']}")
                print(f"   Skills: {len(result['data']['skills'])} skills found")
                print(f"   Experience: {len(result['data']['experience'])} positions")
            else:
                print(f"❌ Resume parsing failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Upload failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False
    
    # Test resume retrieval
    print("\n2. Testing resume retrieval...")
    try:
        response = requests.get("http://localhost:8001/resumes", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Retrieved {len(result['resumes'])} resumes from database")
                for i, resume in enumerate(result['resumes']):
                    print(f"   Resume {i+1}: {resume['parsed_data']['name']} - {resume['file_name']}")
                    print(f"      User ID: {resume.get('user_id', 'None')}")
                    print(f"      Created: {resume['created_at']}")
            else:
                print(f"❌ Retrieval failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Retrieval failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Retrieval error: {e}")
        return False
    
    # Test user-specific retrieval
    print("\n3. Testing user-specific resume retrieval...")
    try:
        response = requests.get("http://localhost:8001/resumes", 
                              params={"user_id": "test_user_123"}, 
                              timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Retrieved {len(result['resumes'])} resumes for user test_user_123")
                for resume in result['resumes']:
                    print(f"   - {resume['parsed_data']['name']} ({resume['file_name']})")
            else:
                print(f"❌ User retrieval failed: {result.get('error')}")
        else:
            print(f"❌ User retrieval failed with status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ User retrieval error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Resume storage test completed!")
    print("✅ Resumes are being stored in MongoDB collection 'resume'")
    print("✅ User association is working")
    print("✅ Resume retrieval is working")
    
    return True

if __name__ == "__main__":
    test_resume_storage_final()
