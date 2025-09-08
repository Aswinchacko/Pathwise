"""
Test the integration between roadmap and recommendation system
"""

import requests
import json

def test_recommendation_integration():
    print("🧪 Testing Recommendation System Integration\n")
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    try:
        response = requests.get("http://localhost:8002/health")
        if response.status_code == 200:
            print("   ✅ Recommendation service is running")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to recommendation service: {e}")
        return False
    
    # Test 2: Get recommendations for completed topics
    print("\n2. Testing Project Recommendations...")
    test_cases = [
        {
            "name": "Web Development Topics",
            "topics": ["HTML", "CSS", "JavaScript", "React"],
            "domain": "web-development",
            "difficulty": "intermediate"
        },
        {
            "name": "Data Science Topics", 
            "topics": ["Python", "Pandas", "Machine Learning"],
            "domain": "data-science",
            "difficulty": "beginner"
        },
        {
            "name": "Mobile Development Topics",
            "topics": ["React Native", "Mobile UI Design"],
            "domain": "mobile-development",
            "difficulty": "intermediate"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n   Testing: {test_case['name']}")
        try:
            goal = f"I have completed: {', '.join(test_case['topics'])}. What should I build next?"
            
            response = requests.post("http://localhost:8002/api/recommend/projects", json={
                "goal": goal,
                "domain": test_case["domain"],
                "difficulty": test_case["difficulty"],
                "limit": 3
            })
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get('recommendations', [])
                print(f"   ✅ Got {len(recommendations)} recommendations")
                
                if recommendations:
                    first_rec = recommendations[0]
                    print(f"      First: {first_rec['title']} ({first_rec['difficulty']})")
                    print(f"      Technologies: {', '.join(first_rec['technologies'][:3])}")
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test 3: Search by technology
    print("\n3. Testing Technology Search...")
    technologies = ["React", "Python", "Docker", "Machine Learning"]
    
    for tech in technologies:
        try:
            response = requests.get(f"http://localhost:8002/api/recommend/projects/search?query={tech}&limit=2")
            if response.status_code == 200:
                data = response.json()
                results = data.get('search_results', [])
                print(f"   ✅ {tech}: {len(results)} projects found")
            else:
                print(f"   ❌ {tech}: Search failed")
        except Exception as e:
            print(f"   ❌ {tech}: Error - {e}")
    
    # Test 4: Feedback submission
    print("\n4. Testing Feedback Submission...")
    try:
        response = requests.post("http://localhost:8002/api/recommend/feedback", json={
            "user_id": "test_user_123",
            "project_id": "web_001",
            "rating": 5,
            "feedback": "Great project for learning React!"
        })
        
        if response.status_code == 200:
            print("   ✅ Feedback submitted successfully")
        else:
            print(f"   ❌ Feedback failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Feedback error: {e}")
    
    print("\n🎉 Integration Test Complete!")
    print("\n📖 Next Steps:")
    print("1. Start your dashboard frontend")
    print("2. Generate a roadmap")
    print("3. Complete some topics by clicking the checkboxes")
    print("4. Watch the project recommendation popup appear!")
    print("5. Or click the 'Project Ideas' button to see recommendations")

if __name__ == "__main__":
    test_recommendation_integration()

