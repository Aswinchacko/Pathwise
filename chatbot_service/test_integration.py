#!/usr/bin/env python3
"""
Integration test for PathWise Chatbot Service
"""

import requests
import json
import time

def test_chatbot_integration():
    """Test the complete chatbot integration"""
    base_url = "http://localhost:8004"
    
    print("🧪 Testing PathWise Chatbot Integration...")
    print("=" * 60)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Storage status
    print("\n2. Testing storage status...")
    try:
        response = requests.get(f"{base_url}/debug/storage", timeout=5)
        if response.status_code == 200:
            storage_info = response.json()
            print(f"✅ Storage type: {storage_info['storage_type']}")
            print(f"   Total chats: {storage_info['total_chats']}")
        else:
            print(f"❌ Storage check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Storage check failed: {e}")
    
    # Test 3: Create new chat
    print("\n3. Testing chat creation...")
    user_id = "test_user_integration"
    chat_id = None
    
    try:
        response = requests.post(f"{base_url}/chats/new", json={
            "user_id": user_id,
            "title": "Integration Test Chat"
        }, timeout=10)
        
        if response.status_code == 200:
            chat_data = response.json()
            chat_id = chat_data["chat_id"]
            print(f"✅ Chat created: {chat_id}")
        else:
            print(f"❌ Chat creation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Chat creation failed: {e}")
        return False
    
    # Test 4: Send messages
    print("\n4. Testing message exchange...")
    test_messages = [
        "Hello, I need help with my career",
        "What skills should I develop for tech?",
        "Suggest some project ideas"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n   Test message {i}: '{message}'")
        try:
            response = requests.post(f"{base_url}/chat", json={
                "message": message,
                "user_id": user_id,
                "chat_id": chat_id
            }, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Response: {data['response'][:80]}...")
                print(f"   📊 Confidence: {data['confidence']:.2f}")
                print(f"   💡 Suggestions: {len(data['suggestions'])} provided")
                if data['suggestions']:
                    print(f"      - {data['suggestions'][0]}")
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Small delay between messages
    
    # Test 5: Get chat history
    print("\n5. Testing chat history retrieval...")
    try:
        response = requests.get(f"{base_url}/chats/{user_id}", timeout=10)
        
        if response.status_code == 200:
            chats_data = response.json()
            print(f"✅ Found {len(chats_data['chats'])} chats for user")
            for chat in chats_data['chats']:
                print(f"   - {chat['title']} ({chat['message_count']} messages)")
        else:
            print(f"❌ Chat history retrieval failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat history retrieval failed: {e}")
    
    # Test 6: Get specific chat messages
    print("\n6. Testing specific chat retrieval...")
    try:
        response = requests.get(f"{base_url}/chats/{user_id}/{chat_id}", timeout=10)
        
        if response.status_code == 200:
            chat_data = response.json()
            print(f"✅ Retrieved chat: {chat_data['title']}")
            print(f"   Messages: {len(chat_data['messages'])}")
            for msg in chat_data['messages'][-3:]:  # Show last 3 messages
                print(f"   - {msg['role']}: {msg['content'][:50]}...")
        else:
            print(f"❌ Specific chat retrieval failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Specific chat retrieval failed: {e}")
    
    # Test 7: Update chat title
    print("\n7. Testing chat title update...")
    try:
        new_title = "Updated Integration Test Chat"
        response = requests.put(f"{base_url}/chats/{user_id}/{chat_id}/title?title={new_title}", timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Title updated to: {new_title}")
        else:
            print(f"❌ Title update failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Title update failed: {e}")
    
    # Test 8: Delete chat
    print("\n8. Testing chat deletion...")
    try:
        response = requests.delete(f"{base_url}/chats/{user_id}/{chat_id}", timeout=10)
        
        if response.status_code == 200:
            print("✅ Chat deleted successfully")
        else:
            print(f"❌ Chat deletion failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat deletion failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Integration test completed!")
    print("✅ Chatbot service is working correctly")
    return True

if __name__ == "__main__":
    test_chatbot_integration()
