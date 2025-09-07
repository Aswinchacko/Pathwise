#!/usr/bin/env python3
"""
Test script for the Resume Parser API
"""

import requests
import json
import sys
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server. Make sure it's running on port 8000")
        return False

def test_upload_resume(file_path):
    """Test the resume upload endpoint"""
    print(f"Testing resume upload with file: {file_path}")
    
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_BASE_URL}/upload-resume", files=files)
        
        if response.status_code == 200:
            print("✓ Resume upload successful")
            data = response.json()
            print(f"  Status: {data['status']}")
            print(f"  Message: {data['message']}")
            print(f"  Extracted name: {data['data'].get('full_name', 'Not found')}")
            print(f"  Extracted email: {data['data'].get('email', 'Not found')}")
            print(f"  Skills count: {len(data['data'].get('skills', []))}")
            return True
        else:
            print(f"❌ Resume upload failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Upload test failed: {str(e)}")
        return False

def main():
    print("🧪 Resume Parser API Test")
    print("=" * 40)
    
    # Test health check
    if not test_health_check():
        sys.exit(1)
    
    print()
    
    # Test upload if file provided
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        test_upload_resume(test_file)
    else:
        print("ℹ️  To test file upload, provide a file path:")
        print("   python test_api.py path/to/resume.pdf")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()
