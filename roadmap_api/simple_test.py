#!/usr/bin/env python3
"""
Simple test to verify the server can start
"""
import subprocess
import time
import requests
import sys

def test_server():
    print("Testing server startup...")
    
    # Start server in subprocess
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("Server started, waiting 5 seconds...")
        time.sleep(5)
        
        # Test if server is responding
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            print(f"✓ Server is responding: {response.json()}")
            
            # Test roadmap generation
            roadmap_response = requests.post("http://localhost:8000/api/roadmap/generate-roadmap", 
                json={"goal": "Become a Frontend Developer", "domain": "Frontend Development"})
            print(f"✓ Roadmap generation works: {roadmap_response.status_code}")
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Server not responding: {e}")
        
        # Kill the process
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"✗ Error starting server: {e}")

if __name__ == "__main__":
    test_server()
