#!/usr/bin/env python3
"""
Test script for PathWise Chatbot Service
"""

import requests
import json
import time

def test_chatbot_service():
    """Test the chatbot service endpoints"""
    base_url = "http://localhost:8004"
    
    print("🧪 Testing PathWise Chatbot Service...")
    print("=" * 50)
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test suggestions endpoint
    print("\n2. Testing suggestions endpoint...")
    try:
        response = requests.get(f"{base_url}/suggestions")
        if response.status_code == 200:
            print("✅ Suggestions endpoint working")
            suggestions = response.json()["suggestions"]
            print(f"   Found {len(suggestions)} suggestions")
            for i, suggestion in enumerate(suggestions[:3], 1):
                print(f"   {i}. {suggestion}")
        else:
            print(f"❌ Suggestions endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Suggestions endpoint failed: {e}")
    
    # Test chat endpoint
    print("\n3. Testing chat endpoint...")
    test_messages = [
        "Hello, I need career guidance",
        "How can I assess my programming skills?",
        "Suggest some project ideas for my portfolio",
        "What's the best way to learn Python?",
        "Help me with my resume"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n   Test {i}: '{message}'")
        try:
            response = requests.post(
                f"{base_url}/chat",
                json={"message": message, "user_id": "test_user"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Response: {data['response'][:100]}...")
                print(f"   📊 Confidence: {data['confidence']:.2f}")
                print(f"   💡 Suggestions: {len(data['suggestions'])} provided")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 50)
    print("🎉 Chatbot service testing completed!")

if __name__ == "__main__":
    test_chatbot_service()
