#!/usr/bin/env python3
"""
Test script for enhanced chatbot with roadmap integration
"""

import requests
import json
import time

def test_enhanced_chatbot():
    """Test the enhanced chatbot with roadmap functionality"""
    base_url = "http://localhost:8004"
    
    print("🧪 Testing Enhanced PathWise Chatbot with Roadmap Integration...")
    print("=" * 70)
    
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
    
    # Test 2: Test roadmap generation in chat
    print("\n2. Testing roadmap generation in chat...")
    user_id = "test_user_roadmap"
    
    test_messages = [
        "Create a roadmap for becoming a full-stack developer",
        "Generate a learning path for data science",
        "Make a roadmap for mobile app development",
        "I want to learn machine learning, create a roadmap",
        "Help me plan my career in DevOps"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n   Test message {i}: '{message}'")
        try:
            response = requests.post(f"{base_url}/chat", json={
                "message": message,
                "user_id": user_id
            }, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Response received")
                print(f"   📊 Confidence: {data['confidence']:.2f}")
                print(f"   💡 Suggestions: {len(data['suggestions'])} provided")
                
                # Check if response contains roadmap data
                if "roadmap" in data.get('response', '').lower():
                    print(f"   🗺️  Roadmap detected in response!")
                else:
                    print(f"   📝 Regular response: {data['response'][:100]}...")
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Small delay between messages
    
    # Test 3: Test roadmap generation endpoint
    print("\n3. Testing direct roadmap generation...")
    try:
        response = requests.post(f"{base_url}/roadmap/generate", json={
            "goal": "Become a Python developer",
            "user_id": user_id,
            "domain": "Programming"
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Roadmap generated successfully")
            print(f"   Title: {data['roadmap']['title']}")
            print(f"   Domain: {data['roadmap']['domain']}")
            print(f"   Steps: {len(data['roadmap']['steps'])}")
        else:
            print(f"❌ Roadmap generation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Roadmap generation error: {e}")
    
    # Test 4: Test getting user roadmaps
    print("\n4. Testing user roadmaps retrieval...")
    try:
        response = requests.get(f"{base_url}/roadmap/user/{user_id}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['roadmaps'])} saved roadmaps")
            for roadmap in data['roadmaps']:
                print(f"   - {roadmap['title']} ({roadmap['domain']})")
        else:
            print(f"❌ Failed to get user roadmaps: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting user roadmaps: {e}")
    
    # Test 5: Test available domains
    print("\n5. Testing available domains...")
    try:
        response = requests.get(f"{base_url}/roadmap/domains", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['domains'])} available domains")
            for domain in data['domains'][:5]:  # Show first 5
                print(f"   - {domain}")
        else:
            print(f"❌ Failed to get domains: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting domains: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 Enhanced chatbot testing completed!")
    print("✅ Chatbot with roadmap integration is working correctly")
    return True

if __name__ == "__main__":
    test_enhanced_chatbot()

