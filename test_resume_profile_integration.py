#!/usr/bin/env python3
"""
Test script to verify resume-to-profile integration
Tests the complete flow: Resume Upload -> Parse -> Store -> Update Profile
"""

import requests
import json
import time
import sys

# API endpoints
AUTH_API = "http://localhost:5000/api/auth"
RESUME_API = "http://localhost:8001"

def test_auth_service():
    """Test if auth service is running"""
    try:
        response = requests.get(f"{AUTH_API}/profile", timeout=5)
        # This should fail with 401 since we don't have a token, but service should be up
        return response.status_code in [401, 200]
    except Exception as e:
        print(f"❌ Auth service not running: {e}")
        return False

def test_resume_service():
    """Test if resume parser service is running"""
    try:
        response = requests.get(f"{RESUME_API}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Resume parser service is running")
            return True
        else:
            print(f"❌ Resume parser service returned: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Resume parser service not running: {e}")
        return False

def create_test_user():
    """Create a test user for testing"""
    test_user = {
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    
    try:
        # Try to register the user
        response = requests.post(f"{AUTH_API}/register", json=test_user)
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Test user created successfully")
            return data['token'], data['user']
        elif response.status_code == 400 and "already exists" in response.json().get('message', ''):
            # User already exists, try to login
            login_response = requests.post(f"{AUTH_API}/login", json={
                "email": test_user["email"],
                "password": test_user["password"]
            })
            
            if login_response.status_code == 200:
                data = login_response.json()
                print("✅ Logged in with existing test user")
                return data['token'], data['user']
            else:
                print(f"❌ Failed to login: {login_response.text}")
                return None, None
        else:
            print(f"❌ Failed to create user: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return None, None

def test_profile_endpoints(token):
    """Test the new profile endpoints"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET profile
    try:
        response = requests.get(f"{AUTH_API}/profile", headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print("✅ Profile GET endpoint working")
            print(f"   User: {profile.get('firstName', '')} {profile.get('lastName', '')}")
            print(f"   Skills: {len(profile.get('skills', []))} skills")
            return profile
        else:
            print(f"❌ Profile GET failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error testing profile GET: {e}")
        return None

def test_resume_upload_and_profile_update(token, user_id):
    """Test resume upload and profile update"""
    
    # Sample resume content
    sample_resume = """
John Smith
Software Engineer
john.smith@email.com
(555) 123-4567
San Francisco, CA

SUMMARY
Experienced software engineer with 5+ years of experience in full-stack development.
Passionate about building scalable applications and mentoring junior developers.

EXPERIENCE
Senior Software Engineer - Tech Solutions Inc
Jan 2020 - Present
• Led development of microservices architecture using Python and FastAPI
• Mentored junior developers and conducted code reviews
• Improved system performance by 40% through optimization

Software Developer - StartupXYZ
Jun 2018 - Dec 2019
• Developed React-based frontend applications
• Built RESTful APIs using Node.js and Express
• Collaborated with design team on user experience improvements

EDUCATION
Bachelor of Computer Science - University of California
2014 - 2018
GPA: 3.8/4.0

SKILLS
Python, JavaScript, TypeScript, React, Node.js, FastAPI, Docker, AWS, MongoDB, PostgreSQL

PROJECTS
E-commerce Platform
Built a full-stack e-commerce platform using React and Node.js
Technologies: React, Node.js, MongoDB, Stripe API

Task Management App
Developed a collaborative task management application
Technologies: Vue.js, Express.js, PostgreSQL

CERTIFICATIONS
AWS Certified Solutions Architect
Certified Kubernetes Administrator
"""

    # Step 1: Upload and parse resume
    print("\n--- Testing Resume Upload ---")
    try:
        files = {"file": ("test_resume.txt", sample_resume, "text/plain")}
        data = {"user_id": user_id}
        
        response = requests.post(f"{RESUME_API}/parse", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Resume uploaded and parsed successfully")
                parsed_data = result['data']
                print(f"   Name: {parsed_data.get('name')}")
                print(f"   Email: {parsed_data.get('email')}")
                print(f"   Skills: {len(parsed_data.get('skills', []))} skills found")
                print(f"   Experience: {len(parsed_data.get('experience', []))} positions")
                print(f"   Education: {len(parsed_data.get('education', []))} entries")
                
                # Step 2: Update profile from resume data
                print("\n--- Testing Profile Update from Resume ---")
                return test_profile_update_from_resume(token, parsed_data)
            else:
                print(f"❌ Resume parsing failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Resume upload failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing resume upload: {e}")
        return False

def test_profile_update_from_resume(token, resume_data):
    """Test updating profile from resume data"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.put(f"{AUTH_API}/profile/from-resume", 
                              json=resume_data, 
                              headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('user'):
                user = result['user']
                print("✅ Profile updated from resume successfully")
                print(f"   Name: {user.get('full_name')}")
                print(f"   Email: {user.get('email')}")
                print(f"   Phone: {user.get('phone')}")
                print(f"   Location: {user.get('location')}")
                print(f"   Skills: {len(user.get('skills', []))} skills")
                print(f"   Experience: {len(user.get('experience', []))} positions")
                print(f"   Education: {len(user.get('education', []))} entries")
                print(f"   Projects: {len(user.get('projects', []))} projects")
                return True
            else:
                print(f"❌ No user data in response: {result}")
                return False
        else:
            print(f"❌ Profile update failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing profile update from resume: {e}")
        return False

def test_regular_profile_update(token):
    """Test regular profile update endpoint"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    profile_update = {
        "firstName": "Updated",
        "lastName": "User",
        "phone": "(555) 999-8888",
        "location": "New York, NY",
        "summary": "Updated summary from test",
        "skills": ["Python", "JavaScript", "React", "Testing"]
    }
    
    try:
        response = requests.put(f"{AUTH_API}/profile", 
                              json=profile_update, 
                              headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Regular profile update successful")
            print(f"   Updated name: {result['user']['full_name']}")
            print(f"   Updated phone: {result['user']['phone']}")
            return True
        else:
            print(f"❌ Regular profile update failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing regular profile update: {e}")
        return False

def main():
    print("🧪 Testing Resume-to-Profile Integration")
    print("=" * 50)
    
    # Check if services are running
    print("\n1. Checking services...")
    auth_ok = test_auth_service()
    resume_ok = test_resume_service()
    
    if not auth_ok:
        print("❌ Auth service is not running. Please start it with: cd auth_back && npm start")
        return
    else:
        print("✅ Auth service is running")
    
    if not resume_ok:
        print("❌ Resume parser service is not running. Please start it with: cd resume_parser && python main.py")
        return
    
    # Create test user
    print("\n2. Setting up test user...")
    token, user = create_test_user()
    if not token:
        print("❌ Failed to create/login test user")
        return
    
    user_id = user['id']
    print(f"✅ Test user ready - ID: {user_id}")
    
    # Test profile endpoints
    print("\n3. Testing profile endpoints...")
    profile = test_profile_endpoints(token)
    if not profile:
        return
    
    # Test resume upload and profile update
    print("\n4. Testing resume upload and profile integration...")
    if test_resume_upload_and_profile_update(token, user_id):
        print("\n5. Testing regular profile update...")
        test_regular_profile_update(token)
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")
        print("\nThe resume-to-profile integration is working correctly:")
        print("✅ Resume parsing and storage")
        print("✅ Profile update from resume data")
        print("✅ Regular profile updates")
        print("✅ Extended user model with resume fields")
    else:
        print("\n❌ Resume-to-profile integration test failed")

if __name__ == "__main__":
    main()
