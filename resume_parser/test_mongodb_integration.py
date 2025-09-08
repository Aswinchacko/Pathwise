import requests
import json
from datetime import datetime

# Test the resume parser API with MongoDB integration
BASE_URL = "http://localhost:8001"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("✅ Health Check:", response.json())
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_parse_and_store_resume():
    """Test parsing and storing a resume in MongoDB"""
    sample_resume = """
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
        # Test parsing text directly
        response = requests.post(
            f"{BASE_URL}/parse-text",
            json=sample_resume
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Resume Parsing Test:")
            print(f"   Name: {data['data']['name']}")
            print(f"   Email: {data['data']['email']}")
            print(f"   Phone: {data['data']['phone']}")
            print(f"   Location: {data['data']['location']}")
            print(f"   Skills: {len(data['data']['skills'])} skills found")
            print(f"   Experience: {len(data['data']['experience'])} positions")
            print(f"   Education: {len(data['data']['education'])} entries")
            return True
        else:
            print(f"❌ Resume parsing failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Resume parsing test failed: {e}")
        return False

def test_file_upload():
    """Test file upload and MongoDB storage"""
    try:
        # Create a test resume file
        test_resume_content = """
Jane Doe
Data Scientist
jane.doe@email.com
(555) 987-6543
New York, NY

SUMMARY
Data scientist with expertise in machine learning and statistical analysis.

EXPERIENCE
Senior Data Scientist - DataCorp
Jan 2021 - Present
• Built ML models for predictive analytics
• Led data science team of 5 engineers

Data Analyst - Analytics Inc
Jun 2019 - Dec 2020
• Performed statistical analysis on large datasets
• Created data visualizations and reports

EDUCATION
Master of Science in Data Science - Stanford University
2017 - 2019

SKILLS
Python, R, SQL, Machine Learning, TensorFlow, PyTorch, Pandas, NumPy
"""
        
        # Test file upload
        files = {"file": ("test_resume.txt", test_resume_content, "text/plain")}
        data = {"user_id": "test_user_123"}
        
        response = requests.post(
            f"{BASE_URL}/parse",
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ File Upload Test:")
            print(f"   Success: {result['success']}")
            if result['success']:
                print(f"   Name: {result['data']['name']}")
                print(f"   Email: {result['data']['email']}")
                print(f"   Skills: {len(result['data']['skills'])} skills found")
                return True
            else:
                print(f"   Error: {result['error']}")
                return False
        else:
            print(f"❌ File upload failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ File upload test failed: {e}")
        return False

def test_get_resumes():
    """Test retrieving resumes from MongoDB"""
    try:
        # Get all resumes
        response = requests.get(f"{BASE_URL}/resumes")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Get Resumes Test:")
            print(f"   Success: {data['success']}")
            print(f"   Number of resumes: {len(data['resumes'])}")
            
            if data['resumes']:
                for i, resume in enumerate(data['resumes'][:3]):  # Show first 3
                    print(f"   Resume {i+1}: {resume['parsed_data']['name']} - {resume['file_name']}")
            
            return True
        else:
            print(f"❌ Get resumes failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get resumes test failed: {e}")
        return False

def test_get_user_resumes():
    """Test retrieving resumes for a specific user"""
    try:
        # Get resumes for test user
        response = requests.get(f"{BASE_URL}/resumes", params={"user_id": "test_user_123"})
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Get User Resumes Test:")
            print(f"   Success: {data['success']}")
            print(f"   Number of resumes for user: {len(data['resumes'])}")
            return True
        else:
            print(f"❌ Get user resumes failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get user resumes test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Resume Parser MongoDB Integration...")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health),
        ("Parse Resume Text", test_parse_and_store_resume),
        ("File Upload & Storage", test_file_upload),
        ("Get All Resumes", test_get_resumes),
        ("Get User Resumes", test_get_user_resumes)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! MongoDB integration is working correctly.")
    else:
        print("❌ Some tests failed. Please check the logs above.")
