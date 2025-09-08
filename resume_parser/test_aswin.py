import requests
import json

# Test the resume parser API with Aswin's resume
BASE_URL = "http://localhost:8001"

def test_parse_aswin_resume():
    """Test parsing Aswin's resume file"""
    try:
        with open("test_aswin_resume.txt", "r", encoding="utf-8") as f:
            files = {"file": ("test_aswin_resume.txt", f.read(), "text/plain")}
        
        response = requests.post(
            f"{BASE_URL}/parse",
            files=files
        )
        
        print("Parse Aswin Resume Response:")
        print(json.dumps(response.json(), indent=2))
        print()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing Aswin's Resume...")
    print("=" * 50)
    test_parse_aswin_resume()

