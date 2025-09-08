#!/usr/bin/env python3

import requests
import json
import time
import subprocess
import sys
import os

def start_service():
    """Start the resume parser service"""
    print("Starting resume parser service...")
    process = subprocess.Popen([sys.executable, "main.py"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
    return process

def test_service():
    """Test the resume storage functionality"""
    
    # Start service
    process = start_service()
    
    try:
        # Wait for service to start
        print("Waiting for service to start...")
        time.sleep(8)
        
        # Test health
        print("Testing health endpoint...")
        try:
            response = requests.get("http://localhost:8001/health", timeout=10)
            if response.status_code == 200:
                print("✅ Service is running")
                print(f"Health: {response.json()}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to service: {e}")
            return False
        
        # Test file upload
        print("\nTesting file upload...")
        test_resume = """
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
        
        files = {"file": ("test.txt", test_resume, "text/plain")}
        data = {"user_id": "test_user_123"}
        
        try:
            response = requests.post(
                "http://localhost:8001/parse",
                files=files,
                data=data,
                timeout=30
            )
            
            print(f"Upload status: {response.status_code}")
            print(f"Upload response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("✅ Resume uploaded and parsed successfully!")
                    print(f"Name: {result['data']['name']}")
                    print(f"Email: {result['data']['email']}")
                    print(f"Skills: {result['data']['skills']}")
                else:
                    print(f"❌ Parsing failed: {result.get('error')}")
                    return False
            else:
                print(f"❌ Upload failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False
        
        # Test retrieval
        print("\nTesting resume retrieval...")
        try:
            response = requests.get("http://localhost:8001/resumes", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"✅ Retrieved {len(result['resumes'])} resumes")
                    for i, resume in enumerate(result['resumes']):
                        print(f"  Resume {i+1}: {resume['parsed_data']['name']}")
                        print(f"    File: {resume['file_name']}")
                        print(f"    User: {resume.get('user_id', 'None')}")
                else:
                    print(f"❌ Retrieval failed: {result.get('error')}")
                    return False
            else:
                print(f"❌ Retrieval failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Retrieval error: {e}")
            return False
        
        print("\n🎉 All tests passed! Resumes are being stored in MongoDB.")
        return True
        
    finally:
        # Clean up
        process.terminate()
        process.wait()
        print("Service stopped")

if __name__ == "__main__":
    print("Resume Storage Test")
    print("=" * 40)
    test_service()
