#!/usr/bin/env python3
"""
Test script to verify chatbot storage is working
"""

import requests
import json
import time

def test_storage():
    """Test if the chatbot is storing data properly"""
    base_url = "http://localhost:8004"
    
    print("🧪 Testing Chatbot Storage...")
    print("=" * 50)
    
    # Test storage status
    print("1. Checking storage status...")
    try:
        response = requests.get(f"{base_url}/debug/storage")
        if response.status_code == 200:
            storage_info = response.json()
            print(f"✅ Storage type: {storage_info['storage_type']}")
            if storage_info['storage_type'] == 'in_memory':
                print(f"   In-memory chats: {storage_info['total_chats']}")
            else:
                print(f"   MongoDB chats: {storage_info['total_chats']}")
        else:
            print(f"❌ Storage check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Storage check failed: {e}")
        return
    
    # Test creating a chat
    print("\n2. Testing chat creation...")
    user_id = "test_user_123"
    
    try:
        response = requests.post(f"{base_url}/chats/new", json={
            "user_id": user_id,
            "title": "Test Chat"
        })
        
        if response.status_code == 200:
            chat_data = response.json()
            chat_id = chat_data["chat_id"]
            print(f"✅ Chat created: {chat_id}")
        else:
            print(f"❌ Chat creation failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Chat creation failed: {e}")
        return
    
    # Test sending a message
    print("\n3. Testing message sending...")
    try:
        response = requests.post(f"{base_url}/chat", json={
            "message": "Hello, this is a test message",
            "user_id": user_id,
            "chat_id": chat_id
        })
        
        if response.status_code == 200:
            message_data = response.json()
            print(f"✅ Message sent: {message_data['response'][:50]}...")
        else:
            print(f"❌ Message sending failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Message sending failed: {e}")
        return
    
    # Test retrieving chat history
    print("\n4. Testing chat history retrieval...")
    try:
        response = requests.get(f"{base_url}/chats/{user_id}")
        
        if response.status_code == 200:
            chats_data = response.json()
            print(f"✅ Found {len(chats_data['chats'])} chats for user")
            for chat in chats_data['chats']:
                print(f"   - {chat['title']} ({chat['message_count']} messages)")
        else:
            print(f"❌ Chat history retrieval failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Chat history retrieval failed: {e}")
        return
    
    # Test retrieving specific chat messages
    print("\n5. Testing specific chat retrieval...")
    try:
        response = requests.get(f"{base_url}/chats/{user_id}/{chat_id}")
        
        if response.status_code == 200:
            chat_data = response.json()
            print(f"✅ Retrieved chat: {chat_data['title']}")
            print(f"   Messages: {len(chat_data['messages'])}")
            for msg in chat_data['messages']:
                print(f"   - {msg['role']}: {msg['content'][:30]}...")
        else:
            print(f"❌ Specific chat retrieval failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Specific chat retrieval failed: {e}")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Storage test completed successfully!")
    print("✅ Chatbot is properly storing and retrieving data")

if __name__ == "__main__":
    test_storage()
