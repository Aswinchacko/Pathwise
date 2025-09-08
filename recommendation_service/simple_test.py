#!/usr/bin/env python3
"""
Simple test to verify the service works
"""

import requests
import time
import subprocess
import sys

def test_service():
    """Test if the service is working"""
    print("Testing recommendation service...")
    
    # Wait a bit for service to start
    time.sleep(2)
    
    try:
        response = requests.get("http://localhost:8002/health", timeout=5)
        print(f"✅ Service is running! Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Service is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error testing service: {e}")
        return False

def start_service():
    """Start the service in background"""
    print("Starting service...")
    try:
        # Start service in background
        process = subprocess.Popen([
            sys.executable, "-c", 
            "from main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8002)"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"Service started with PID: {process.pid}")
        return process
    except Exception as e:
        print(f"Error starting service: {e}")
        return None

if __name__ == "__main__":
    # Start service
    process = start_service()
    
    if process:
        # Test service
        if test_service():
            print("🎉 Service is working correctly!")
        else:
            print("❌ Service test failed")
        
        # Clean up
        try:
            process.terminate()
            print("Service stopped")
        except:
            pass
    else:
        print("❌ Failed to start service")
