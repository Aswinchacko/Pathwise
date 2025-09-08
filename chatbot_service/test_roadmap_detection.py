#!/usr/bin/env python3
"""
Test script for roadmap detection functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import detect_roadmap_request, extract_goal_from_message

def test_roadmap_detection():
    """Test roadmap detection and goal extraction"""
    print("🧪 Testing Roadmap Detection...")
    print("=" * 50)
    
    test_messages = [
        "Create a roadmap for becoming a full-stack developer",
        "Generate a learning path for data science",
        "Make a roadmap for mobile app development",
        "I want to learn machine learning, create a roadmap",
        "Help me plan my career in DevOps",
        "What skills should I learn for web development?",
        "How can I become a Python developer?",
        "Create a plan for learning React",
        "Generate a roadmap for becoming a data scientist",
        "I need help with my career path in technology"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Testing: '{message}'")
        
        # Test roadmap detection
        detection = detect_roadmap_request(message)
        print(f"   Roadmap Request: {detection['is_roadmap_request']}")
        print(f"   Confidence: {detection['confidence']:.2f}")
        print(f"   Extracted Goal: '{detection['extracted_goal']}'")
        
        # Test goal extraction
        goal = extract_goal_from_message(message)
        print(f"   Direct Goal: '{goal}'")
        
        if detection['is_roadmap_request']:
            print("   ✅ Roadmap request detected!")
        else:
            print("   ❌ Roadmap request not detected")
    
    print("\n" + "=" * 50)
    print("🎉 Roadmap detection testing completed!")

if __name__ == "__main__":
    test_roadmap_detection()

