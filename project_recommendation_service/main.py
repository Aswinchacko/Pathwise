"""
Project Recommendation Service
Recommends projects based on completed roadmap topics
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Project Recommendation Service", version="1.0.0")

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
ROADMAP_API_URL = os.getenv("ROADMAP_API_URL", "http://localhost:8001")
RECOMMENDATION_SERVICE_URL = os.getenv("RECOMMENDATION_SERVICE_URL", "http://localhost:8002")

class ProjectRecommendationRequest(BaseModel):
    user_id: str
    roadmap_id: str
    completed_topics: List[str]
    domain: str
    completion_percentage: float

class ProjectRecommendation(BaseModel):
    project_id: str
    title: str
    description: str
    difficulty: str  # beginner, intermediate, advanced
    estimated_duration: str  # e.g., "2-4 weeks"
    skills_required: List[str]
    skills_learned: List[str]
    project_type: str  # web_app, mobile_app, data_analysis, etc.
    github_template: Optional[str] = None
    tutorial_links: List[str] = []
    tags: List[str] = []

class ProjectRecommendationResponse(BaseModel):
    recommendations: List[ProjectRecommendation]
    message: str
    completion_percentage: float
    next_milestone: str

# Sample project database (in production, this would be in MongoDB)
PROJECT_DATABASE = {
    "Data Science": [
        {
            "project_id": "ds_001",
            "title": "Stock Price Prediction Model",
            "description": "Build a machine learning model to predict stock prices using historical data and technical indicators.",
            "difficulty": "intermediate",
            "estimated_duration": "3-4 weeks",
            "skills_required": ["Python", "Pandas", "NumPy", "Scikit-learn", "Matplotlib"],
            "skills_learned": ["Time Series Analysis", "Feature Engineering", "Model Evaluation", "Financial Data"],
            "project_type": "data_analysis",
            "github_template": "https://github.com/example/stock-prediction-template",
            "tutorial_links": [
                "https://www.kaggle.com/learn/intro-to-programming",
                "https://pandas.pydata.org/docs/getting_started/index.html"
            ],
            "tags": ["finance", "machine-learning", "time-series", "pandas"]
        },
        {
            "project_id": "ds_002",
            "title": "Customer Segmentation Analysis",
            "description": "Analyze customer data to identify distinct segments and create targeted marketing strategies.",
            "difficulty": "beginner",
            "estimated_duration": "2-3 weeks",
            "skills_required": ["Python", "Pandas", "Matplotlib", "Seaborn", "K-means"],
            "skills_learned": ["Clustering", "Data Visualization", "Customer Analytics", "Statistical Analysis"],
            "project_type": "data_analysis",
            "github_template": "https://github.com/example/customer-segmentation",
            "tutorial_links": [
                "https://scikit-learn.org/stable/modules/clustering.html",
                "https://seaborn.pydata.org/tutorial.html"
            ],
            "tags": ["clustering", "visualization", "marketing", "analytics"]
        }
    ],
    "Frontend Development": [
        {
            "project_id": "fe_001",
            "title": "E-commerce Dashboard",
            "description": "Create a responsive e-commerce admin dashboard with product management, order tracking, and analytics.",
            "difficulty": "intermediate",
            "estimated_duration": "4-5 weeks",
            "skills_required": ["React", "JavaScript", "CSS", "Chart.js", "API Integration"],
            "skills_learned": ["State Management", "Component Design", "Data Visualization", "Responsive Design"],
            "project_type": "web_app",
            "github_template": "https://github.com/example/ecommerce-dashboard",
            "tutorial_links": [
                "https://reactjs.org/tutorial/tutorial.html",
                "https://www.chartjs.org/docs/latest/"
            ],
            "tags": ["react", "dashboard", "ecommerce", "responsive"]
        },
        {
            "project_id": "fe_002",
            "title": "Real-time Chat Application",
            "description": "Build a real-time chat application with user authentication, message history, and file sharing.",
            "difficulty": "advanced",
            "estimated_duration": "5-6 weeks",
            "skills_required": ["React", "Node.js", "Socket.io", "MongoDB", "JWT"],
            "skills_learned": ["WebSockets", "Real-time Communication", "Authentication", "Database Design"],
            "project_type": "web_app",
            "github_template": "https://github.com/example/realtime-chat",
            "tutorial_links": [
                "https://socket.io/get-started/chat",
                "https://jwt.io/introduction"
            ],
            "tags": ["realtime", "chat", "websockets", "authentication"]
        }
    ],
    "Backend Development": [
        {
            "project_id": "be_001",
            "title": "RESTful API with Authentication",
            "description": "Build a secure REST API with user authentication, authorization, and CRUD operations.",
            "difficulty": "intermediate",
            "estimated_duration": "3-4 weeks",
            "skills_required": ["Node.js", "Express", "MongoDB", "JWT", "bcrypt"],
            "skills_learned": ["API Design", "Security", "Database Operations", "Middleware"],
            "project_type": "api",
            "github_template": "https://github.com/example/restful-api",
            "tutorial_links": [
                "https://expressjs.com/en/guide/routing.html",
                "https://jwt.io/introduction"
            ],
            "tags": ["api", "authentication", "security", "crud"]
        }
    ],
    "Mobile Development": [
        {
            "project_id": "mob_001",
            "title": "Task Management App",
            "description": "Create a cross-platform mobile app for task management with offline support and sync.",
            "difficulty": "intermediate",
            "estimated_duration": "4-5 weeks",
            "skills_required": ["React Native", "JavaScript", "AsyncStorage", "Redux"],
            "skills_learned": ["Mobile Development", "State Management", "Offline Storage", "Cross-platform"],
            "project_type": "mobile_app",
            "github_template": "https://github.com/example/task-manager-app",
            "tutorial_links": [
                "https://reactnative.dev/docs/getting-started",
                "https://redux.js.org/introduction/getting-started"
            ],
            "tags": ["mobile", "react-native", "tasks", "offline"]
        }
    ]
}

def get_roadmap_details(roadmap_id: str, user_id: str) -> Dict[str, Any]:
    """Fetch roadmap details from roadmap API"""
    try:
        response = requests.get(f"{ROADMAP_API_URL}/api/roadmap/roadmaps/user/{user_id}")
        if response.status_code == 200:
            roadmaps = response.json().get("roadmaps", [])
            for roadmap in roadmaps:
                if roadmap.get("roadmap_id") == roadmap_id:
                    return roadmap
        return None
    except Exception as e:
        print(f"Error fetching roadmap: {e}")
        return None

def calculate_skill_match(completed_topics: List[str], project_skills: List[str]) -> float:
    """Calculate how well completed topics match project requirements"""
    if not project_skills:
        return 0.0
    
    completed_lower = [topic.lower() for topic in completed_topics]
    project_lower = [skill.lower() for skill in project_skills]
    
    matches = sum(1 for skill in project_lower if any(topic in skill or skill in topic for topic in completed_lower))
    return matches / len(project_skills)

def get_recommendations(domain: str, completed_topics: List[str], completion_percentage: float) -> List[ProjectRecommendation]:
    """Get project recommendations based on domain and completed topics"""
    domain_projects = PROJECT_DATABASE.get(domain, [])
    recommendations = []
    
    for project in domain_projects:
        # Calculate skill match percentage
        skill_match = calculate_skill_match(completed_topics, project["skills_required"])
        
        # Filter based on completion percentage and skill match
        if completion_percentage >= 20 and skill_match >= 0.3:  # At least 30% skill match
            # Adjust difficulty based on completion percentage
            if completion_percentage < 40 and project["difficulty"] == "advanced":
                continue  # Skip advanced projects for low completion
            elif completion_percentage >= 60 and project["difficulty"] == "beginner":
                continue  # Skip beginner projects for high completion
            
            recommendations.append(ProjectRecommendation(**project))
    
    # Sort by skill match and difficulty
    recommendations.sort(key=lambda x: (
        calculate_skill_match(completed_topics, x.skills_required),
        {"beginner": 1, "intermediate": 2, "advanced": 3}[x.difficulty]
    ), reverse=True)
    
    return recommendations[:5]  # Return top 5 recommendations

def get_next_milestone(completion_percentage: float) -> str:
    """Get the next milestone message based on completion percentage"""
    if completion_percentage < 20:
        return "Complete a few more topics to unlock project recommendations!"
    elif completion_percentage < 40:
        return "Great progress! Try some beginner projects to apply your skills."
    elif completion_percentage < 60:
        return "You're halfway there! Intermediate projects are now available."
    elif completion_percentage < 80:
        return "Excellent work! Advanced projects and mentor recommendations are unlocked."
    else:
        return "Outstanding! You're ready for job opportunities and advanced projects."

@app.get("/")
async def root():
    return {"message": "Project Recommendation Service is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/projects/recommend", response_model=ProjectRecommendationResponse)
async def recommend_projects(request: ProjectRecommendationRequest):
    """Get project recommendations based on completed topics"""
    try:
        # Validate completion percentage
        if request.completion_percentage < 0 or request.completion_percentage > 100:
            raise HTTPException(status_code=400, detail="Completion percentage must be between 0 and 100")
        
        # Get recommendations
        recommendations = get_recommendations(
            request.domain, 
            request.completed_topics, 
            request.completion_percentage
        )
        
        # Get next milestone message
        next_milestone = get_next_milestone(request.completion_percentage)
        
        if not recommendations:
            return ProjectRecommendationResponse(
                recommendations=[],
                message="Complete more topics to unlock project recommendations!",
                completion_percentage=request.completion_percentage,
                next_milestone=next_milestone
            )
        
        return ProjectRecommendationResponse(
            recommendations=recommendations,
            message=f"Found {len(recommendations)} project recommendations based on your progress!",
            completion_percentage=request.completion_percentage,
            next_milestone=next_milestone
        )
        
    except Exception as e:
        print(f"Error in project recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.get("/api/projects/domains")
async def get_available_domains():
    """Get list of domains with available projects"""
    return {
        "domains": list(PROJECT_DATABASE.keys()),
        "total_projects": sum(len(projects) for projects in PROJECT_DATABASE.values())
    }

@app.get("/api/projects/domain/{domain}")
async def get_projects_by_domain(domain: str):
    """Get all projects for a specific domain"""
    if domain not in PROJECT_DATABASE:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    projects = [ProjectRecommendation(**project) for project in PROJECT_DATABASE[domain]]
    return {
        "domain": domain,
        "projects": projects,
        "count": len(projects)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)

