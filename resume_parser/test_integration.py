import requests
import json

# Test the resume parser API integration
BASE_URL = "http://localhost:8001"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("Health Check:", response.json())
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_simple_resume():
    """Test with a simple resume"""
    resume_text = """
John Doe
Software Engineer
john.doe@email.com
(555) 123-4567
San Francisco, CA

SUMMARY
Experienced software engineer with 5+ years of experience.

EXPERIENCE
Senior Software Engineer - Tech Corp
Jan 2020 - Present
• Led development of microservices
• Mentored junior developers

EDUCATION
Bachelor of Computer Science - University of California
2014 - 2018

SKILLS
Python, JavaScript, React, Node.js, Docker, AWS
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/parse-text",
            params={"text": resume_text}
        )
        
        print("Simple Resume Test:")
        print(json.dumps(response.json(), indent=2))
        return True
    except Exception as e:
        print(f"Simple resume test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Resume Parser Integration...")
    print("=" * 50)
    
    if test_health():
        test_simple_resume()
    else:
        print("Server is not running. Please start the server first.")
