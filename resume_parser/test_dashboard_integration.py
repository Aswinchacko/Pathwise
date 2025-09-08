import requests
import json

# Test the dashboard integration with resume parser
DASHBOARD_URL = "http://localhost:5173"
RESUME_PARSER_URL = "http://localhost:8001"

def test_resume_parser_service():
    """Test if resume parser service is running"""
    try:
        response = requests.get(f"{RESUME_PARSER_URL}/health")
        print("✅ Resume Parser Service:", response.json())
        return True
    except Exception as e:
        print(f"❌ Resume Parser Service failed: {e}")
        return False

def test_dashboard():
    """Test if dashboard is running"""
    try:
        response = requests.get(DASHBOARD_URL)
        if response.status_code == 200:
            print("✅ Dashboard is running")
            return True
        else:
            print(f"❌ Dashboard returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard failed: {e}")
        return False

def test_resume_parsing():
    """Test resume parsing with a sample file"""
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
        response = requests.post(
            f"{RESUME_PARSER_URL}/parse-text",
            params={"text": sample_resume}
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

if __name__ == "__main__":
    print("Testing Dashboard Integration with Resume Parser...")
    print("=" * 60)
    
    services_ok = test_resume_parser_service() and test_dashboard()
    
    if services_ok:
        print("\n" + "=" * 60)
        test_resume_parsing()
        print("\n" + "=" * 60)
        print("🎉 Integration test completed!")
        print("You can now:")
        print("1. Open http://localhost:5173 in your browser")
        print("2. Navigate to the Resume Parser page")
        print("3. Upload a resume file (PDF, DOCX, or TXT)")
        print("4. See the parsed data displayed")
    else:
        print("\n❌ Some services are not running. Please check the logs.")

