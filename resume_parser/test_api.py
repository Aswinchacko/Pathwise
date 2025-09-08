import requests
import json

# Test the resume parser API
BASE_URL = "http://localhost:8001"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())
    print()

def test_parse_text():
    """Test parsing resume text directly"""
    resume_text = """
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
Python, JavaScript, TypeScript, React, Node.js, FastAPI, Docker, AWS
"""
    
    response = requests.post(
        f"{BASE_URL}/parse-text",
        json=resume_text
    )
    
    print("Parse Text Response:")
    print(json.dumps(response.json(), indent=2))
    print()

def test_parse_file():
    """Test parsing resume file"""
    with open("test_resume.txt", "r") as f:
        files = {"file": ("test_resume.txt", f.read(), "text/plain")}
    
    response = requests.post(
        f"{BASE_URL}/parse",
        files=files
    )
    
    print("Parse File Response:")
    print(json.dumps(response.json(), indent=2))
    print()

if __name__ == "__main__":
    print("Testing Resume Parser API...")
    print("=" * 50)
    
    try:
        test_health()
        test_parse_text()
        test_parse_file()
        print("All tests completed!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running on port 8001.")
    except Exception as e:
        print(f"Error: {e}")

