#!/usr/bin/env python3
"""
Test script to verify frontend-backend connection
"""

import requests
import json

def test_connection():
    """Test the complete flow"""
    print("🧪 Testing Frontend-Backend Connection...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get('http://localhost:8002/health')
        if response.status_code == 200:
            print("✅ Backend is healthy")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure the chatbot service is running: cd chatbot_service && python start_server.py")
        return
    
    # Test 2: CORS test
    print("\n2. Testing CORS...")
    try:
        headers = {
            'Origin': 'http://localhost:5173',
            'Content-Type': 'application/json'
        }
        response = requests.options('http://localhost:8002/chat', headers=headers)
        print(f"✅ CORS preflight: {response.status_code}")
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
    
    # Test 3: Chat endpoint
    print("\n3. Testing chat endpoint...")
    try:
        response = requests.post('http://localhost:8002/chat', 
                               json={'message': 'Hello from test', 'user_id': 'test_user'},
                               headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat endpoint working")
            print(f"   Response: {data['response'][:50]}...")
            print(f"   Chat ID: {data['chat_id']}")
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
    
    # Test 4: Chat history
    print("\n4. Testing chat history...")
    try:
        response = requests.get('http://localhost:8002/chats/test_user')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat history working: {len(data['chats'])} chats found")
        else:
            print(f"❌ Chat history failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat history error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Connection test completed!")
    print("\n💡 If all tests pass, try refreshing your browser")
    print("💡 Make sure both services are running:")
    print("   - Backend: cd chatbot_service && python start_server.py")
    print("   - Frontend: cd dashboard && npm run dev")

if __name__ == "__main__":
    test_connection()
