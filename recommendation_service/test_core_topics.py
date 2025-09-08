"""
Test core topic filtering and recommendations
"""

import requests
import json

def test_core_topic_recommendations():
    print("🧪 Testing Core Topic Recommendations\n")
    
    # Test cases for different types of topics
    test_cases = [
        {
            "name": "Core Web Development Topics",
            "topics": ["JavaScript", "React", "Node.js", "Express"],
            "domain": "web-development",
            "should_trigger": True
        },
        {
            "name": "Basic Topics (should not trigger)",
            "topics": ["Introduction to Programming", "Basic Concepts", "Getting Started"],
            "domain": "web-development", 
            "should_trigger": False
        },
        {
            "name": "Advanced Topics (should trigger)",
            "topics": ["Advanced React Patterns", "Microservices Architecture", "Docker"],
            "domain": "web-development",
            "should_trigger": True
        },
        {
            "name": "Data Science Core Topics",
            "topics": ["Python", "Pandas", "Machine Learning", "TensorFlow"],
            "domain": "data-science",
            "should_trigger": True
        }
    ]
    
    for test_case in test_cases:
        print(f"Testing: {test_case['name']}")
        print(f"Topics: {', '.join(test_case['topics'])}")
        
        try:
            goal = f"I have completed: {', '.join(test_case['topics'])}. What should I build next?"
            
            response = requests.post("http://localhost:8002/api/recommend/projects", json={
                "goal": goal,
                "domain": test_case["domain"],
                "difficulty": "intermediate",
                "limit": 3
            })
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get('recommendations', [])
                
                if recommendations:
                    print(f"   ✅ Got {len(recommendations)} recommendations")
                    for i, rec in enumerate(recommendations[:2], 1):
                        print(f"      {i}. {rec['title']} ({rec['difficulty']})")
                        print(f"         Technologies: {', '.join(rec['technologies'][:3])}")
                else:
                    print(f"   ⚠️  No recommendations found")
                    
                # Check if this matches expected behavior
                if test_case['should_trigger'] and recommendations:
                    print(f"   ✅ Correctly triggered recommendations")
                elif not test_case['should_trigger'] and not recommendations:
                    print(f"   ✅ Correctly did not trigger recommendations")
                else:
                    print(f"   ⚠️  Unexpected behavior")
                    
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    test_core_topic_recommendations()

