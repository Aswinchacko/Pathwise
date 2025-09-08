#!/usr/bin/env python3

import requests
import json
import time

def test_chatbot_service():
    base_url = "http://localhost:8004"
    
    print("Testing Chatbot Service...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return False
    
    # Test chat endpoint
    try:
        chat_data = {
            "message": "Hello, I need help with my career",
            "user_id": "test_user_123"
        }
        response = requests.post(f"{base_url}/chat", json=chat_data, timeout=10)
        print(f"Chat test: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result['response']}")
            print(f"Chat ID: {result['chat_id']}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Chat test failed: {e}")
        return False

if __name__ == "__main__":
    test_chatbot_service()

