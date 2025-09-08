#!/usr/bin/env python3
"""
Complete flow test for chatbot system
"""

import requests
import json
import time

def test_complete_flow():
    """Test the complete chatbot flow"""
    base_url = "http://localhost:8004"
    user_id = "test_user_complete_flow"
    
    print("🧪 Testing Complete Chatbot Flow...")
    print("=" * 60)
    
    # Step 1: Create a chat by sending a message
    print("1. Creating chat by sending first message...")
    try:
        response = requests.post(f"{base_url}/chat", json={
            "message": "Hello, I need help with my career",
            "user_id": user_id
        })
        
        if response.status_code == 200:
            data = response.json()
            chat_id = data["chat_id"]
            print(f"✅ Chat created: {chat_id}")
            print(f"   Response: {data['response'][:50]}...")
        else:
            print(f"❌ Failed to create chat: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error creating chat: {e}")
        return
    
    # Step 2: Check chat history
    print("\n2. Checking chat history...")
    try:
        response = requests.get(f"{base_url}/chats/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['chats'])} chats")
            for chat in data['chats']:
                print(f"   - {chat['title']} (ID: {chat['chat_id']})")
        else:
            print(f"❌ Failed to get chat history: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting chat history: {e}")
    
    # Step 3: Send another message to the same chat
    print("\n3. Sending another message to existing chat...")
    try:
        response = requests.post(f"{base_url}/chat", json={
            "message": "What skills should I learn for software development?",
            "user_id": user_id,
            "chat_id": chat_id
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Message sent to existing chat")
            print(f"   Response: {data['response'][:50]}...")
        else:
            print(f"❌ Failed to send message: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending message: {e}")
    
    # Step 4: Check chat history again
    print("\n4. Checking chat history after second message...")
    try:
        response = requests.get(f"{base_url}/chats/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['chats'])} chats")
            for chat in data['chats']:
                print(f"   - {chat['title']} (Messages: {chat['message_count']})")
        else:
            print(f"❌ Failed to get chat history: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting chat history: {e}")
    
    # Step 5: Create a new chat explicitly
    print("\n5. Creating a new chat explicitly...")
    try:
        response = requests.post(f"{base_url}/chats/new", json={
            "user_id": user_id,
            "title": "Explicit New Chat"
        })
        
        if response.status_code == 200:
            data = response.json()
            new_chat_id = data["chat_id"]
            print(f"✅ New chat created: {new_chat_id}")
        else:
            print(f"❌ Failed to create new chat: {response.status_code}")
    except Exception as e:
        print(f"❌ Error creating new chat: {e}")
    
    # Step 6: Final chat history check
    print("\n6. Final chat history check...")
    try:
        response = requests.get(f"{base_url}/chats/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Final result: {len(data['chats'])} chats found")
            for i, chat in enumerate(data['chats'], 1):
                print(f"   {i}. {chat['title']} (Messages: {chat['message_count']})")
        else:
            print(f"❌ Failed to get final chat history: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting final chat history: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Complete flow test finished!")
    print("💡 If you see chats above, the backend is working correctly.")
    print("💡 If the frontend still doesn't show chats, check browser console for errors.")

if __name__ == "__main__":
    test_complete_flow()
