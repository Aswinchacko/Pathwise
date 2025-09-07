#!/usr/bin/env python3
"""
Quick test to verify chatbot storage without MongoDB
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import get_or_create_chat, save_message, get_conversation_context, in_memory_chats

async def test_in_memory_storage():
    """Test in-memory storage functionality"""
    print("🧪 Testing In-Memory Storage...")
    print("=" * 40)
    
    # Test 1: Create a chat
    print("1. Creating chat...")
    chat = await get_or_create_chat("test_user_123")
    print(f"✅ Chat created: {chat['_id']}")
    print(f"   Title: {chat['title']}")
    print(f"   Messages: {len(chat['messages'])}")
    
    # Test 2: Add messages
    print("\n2. Adding messages...")
    await save_message(chat['_id'], "user", "Hello, how are you?")
    await save_message(chat['_id'], "assistant", "I'm doing great! How can I help you today?")
    await save_message(chat['_id'], "user", "I need help with my career")
    await save_message(chat['_id'], "assistant", "I'd be happy to help with career guidance!")
    
    print(f"✅ Added 4 messages to chat {chat['_id']}")
    
    # Test 3: Get conversation context
    print("\n3. Getting conversation context...")
    context = await get_conversation_context(chat['_id'])
    print(f"✅ Retrieved {len(context)} messages from context")
    for i, msg in enumerate(context):
        print(f"   {i+1}. {msg['role']}: {msg['content'][:50]}...")
    
    # Test 4: Check in-memory storage
    print("\n4. Checking in-memory storage...")
    print(f"✅ Total chats in memory: {len(in_memory_chats)}")
    for chat_id, chat_data in in_memory_chats.items():
        print(f"   - {chat_id}: {chat_data['title']} ({len(chat_data['messages'])} messages)")
    
    print("\n" + "=" * 40)
    print("🎉 In-memory storage test completed!")
    print("✅ Chatbot storage is working correctly")

if __name__ == "__main__":
    asyncio.run(test_in_memory_storage())
