from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import random
import re
from datetime import datetime
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os

app = FastAPI(title="Roadmap Generator API", version="1.0.0")

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Test MongoDB connection
        db.admin.command('ping')
        return {"status": "healthy", "service": "roadmap-api", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "service": "roadmap-api", "database": "disconnected", "error": str(e)}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "pathwise")

# Initialize MongoDB client
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]
roadmap_collection = db["roadmap"]

# Load CSV data
try:
    df = pd.read_csv("cross_domain_roadmaps_520.csv")
    print(f"Loaded {len(df)} roadmaps from CSV")
    
    # Store CSV data in MongoDB if collection is empty
    if roadmap_collection.count_documents({}) == 0:
        print("Storing CSV data in MongoDB...")
        roadmaps_to_insert = []
        for _, row in df.iterrows():
            roadmap_doc = {
                "csv_id": int(row['id']),
                "title": row['goal'],  # Add explicit title field
                "goal": row['goal'],
                "domain": row['domain'],
                "roadmap_text": row['roadmap'],
                "steps": parse_roadmap_steps(row['roadmap']),
                "created_at": datetime.now(),
                "source": "csv_import"
            }
            roadmaps_to_insert.append(roadmap_doc)
        
        roadmap_collection.insert_many(roadmaps_to_insert)
        print(f"Stored {len(roadmaps_to_insert)} roadmaps in MongoDB")
    else:
        print(f"MongoDB already contains {roadmap_collection.count_documents({})} roadmaps")
        
except FileNotFoundError:
    print("CSV file not found. Please ensure cross_domain_roadmaps_520.csv is in the same directory.")
    df = pd.DataFrame()

# Pydantic models
class RoadmapRequest(BaseModel):
    goal: str
    domain: Optional[str] = None
    user_id: Optional[str] = None

class RoadmapResponse(BaseModel):
    id: str
    title: str
    goal: str
    domain: str
    steps: List[dict]
    created_at: str

class DomainResponse(BaseModel):
    domains: List[str]

class UserRoadmapsResponse(BaseModel):
    roadmaps: List[dict]

# MongoDB is used for storage instead of in-memory

def parse_roadmap_steps(roadmap_text: str) -> List[dict]:
    """Parse roadmap text into structured steps"""
    steps = []
    
    # Split by | to get main categories
    categories = roadmap_text.split(' | ')
    
    for category in categories:
        if ':' in category:
            category_name, skills_text = category.split(':', 1)
            category_name = category_name.strip()
            # Split skills by semicolon and clean them up
            skills = [skill.strip() for skill in skills_text.split(';') if skill.strip()]
            
            steps.append({
                "category": category_name,
                "skills": skills
            })
    
    return steps

def find_best_roadmap(goal: str, domain: Optional[str] = None) -> dict:
    """Find the best matching roadmap based on goal and domain from MongoDB"""
    try:
        # Build MongoDB query
        query = {}
        if domain:
            query["domain"] = {"$regex": domain, "$options": "i"}
        
        # Get all roadmaps from MongoDB
        roadmaps = list(roadmap_collection.find(query))
        
        if not roadmaps:
            # Fallback to all roadmaps if domain filter returns nothing
            roadmaps = list(roadmap_collection.find({}))
        
        if not roadmaps:
            raise HTTPException(status_code=500, detail="No roadmaps available in database")
        
        # Enhanced matching based on goal keywords
        goal_lower = goal.lower()
        best_match = None
        best_score = 0
        
        # Define keyword mappings for better matching
        keyword_mappings = {
            'frontend': ['frontend', 'front-end', 'ui', 'ux', 'react', 'vue', 'angular', 'javascript', 'css', 'html'],
            'backend': ['backend', 'back-end', 'server', 'api', 'node', 'python', 'java', 'php', 'ruby', 'go'],
            'fullstack': ['fullstack', 'full-stack', 'full stack', 'fullstack', 'mern', 'mean'],
            'data': ['data', 'analytics', 'science', 'scientist', 'analysis', 'machine learning', 'ai', 'ml'],
            'devops': ['devops', 'dev ops', 'deployment', 'ci/cd', 'docker', 'kubernetes', 'aws', 'cloud'],
            'mobile': ['mobile', 'ios', 'android', 'react native', 'flutter', 'swift', 'kotlin'],
            'python': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy', 'data science'],
            'javascript': ['javascript', 'js', 'node', 'react', 'vue', 'angular', 'typescript'],
            'java': ['java', 'spring', 'hibernate', 'maven', 'gradle'],
            'web': ['web', 'website', 'web development', 'html', 'css', 'javascript']
        }
        
        for roadmap in roadmaps:
            score = 0
            roadmap_goal = roadmap['goal'].lower()
            roadmap_domain = roadmap['domain'].lower()
            
            # Check for exact matches in goal
            if goal_lower in roadmap_goal:
                score += 20
            
            # Check for keyword matches in goal
            goal_words = goal_lower.split()
            for word in goal_words:
                if word in roadmap_goal:
                    score += 3
                
                # Check keyword mappings
                for category, keywords in keyword_mappings.items():
                    if word in keywords:
                        if category in roadmap_goal or category in roadmap_domain:
                            score += 5
            
            # Bonus for domain match
            if domain and domain.lower() in roadmap_domain:
                score += 10
            
            # Check for common tech terms
            tech_terms = ['developer', 'engineer', 'programmer', 'coder', 'architect']
            for term in tech_terms:
                if term in goal_lower and term in roadmap_goal:
                    score += 2
            
            if score > best_score:
                best_score = score
                best_match = roadmap
        
        # If no good match found, return a random one
        if best_match is None:
            best_match = roadmaps[0]  # Take first one as fallback
        
        return best_match
        
    except Exception as e:
        print(f"Error finding roadmap in MongoDB: {e}")
        raise HTTPException(status_code=500, detail=f"Error finding roadmap: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Roadmap Generator API is running"}

@app.post("/api/roadmap/generate-roadmap", response_model=RoadmapResponse)
async def generate_roadmap(request: RoadmapRequest):
    """Generate a roadmap based on goal and domain and store/update in MongoDB"""
    try:
        # Find best matching roadmap from MongoDB
        best_match = find_best_roadmap(request.goal, request.domain)
        
        # Use pre-parsed steps from MongoDB
        steps = best_match.get('steps', [])
        
        # Debug logging
        print(f"Generated roadmap for goal: '{request.goal}'")
        print(f"Matched domain: {best_match['domain']}")
        print(f"Number of steps: {len(steps)}")
        for i, step in enumerate(steps):
            print(f"Step {i+1}: {step['category']} - {len(step['skills'])} skills")
        
        # Create response
        roadmap_id = f"roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
        
        response = RoadmapResponse(
            id=roadmap_id,
            title=request.goal,
            goal=request.goal,
            domain=best_match['domain'],
            steps=steps,
            created_at=datetime.now().isoformat()
        )
        
        # Store/Update roadmap in MongoDB
        roadmap_doc = {
            "roadmap_id": roadmap_id,
            "title": request.goal,  # Add explicit title field
            "goal": request.goal,
            "domain": best_match['domain'],
            "steps": steps,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "source": "user_generated",
            "user_id": request.user_id,
            "base_roadmap_id": best_match.get('_id'),  # Reference to original roadmap
            "generation_count": 1
        }
        
        # Check if user already has a roadmap for this goal
        if request.user_id:
            existing_roadmap = roadmap_collection.find_one({
                "user_id": request.user_id,
                "goal": request.goal,
                "source": "user_generated"
            })
            
            if existing_roadmap:
                # Update existing roadmap
                roadmap_doc["generation_count"] = existing_roadmap.get("generation_count", 1) + 1
                roadmap_doc["roadmap_id"] = existing_roadmap["roadmap_id"]  # Keep same ID
                roadmap_doc["created_at"] = existing_roadmap["created_at"]  # Keep original creation date
                
                result = roadmap_collection.update_one(
                    {
                        "user_id": request.user_id,
                        "goal": request.goal,
                        "source": "user_generated"
                    },
                    {
                        "$set": {
                            "title": request.goal,  # Update title field
                            "domain": best_match['domain'],
                            "steps": steps,
                            "updated_at": datetime.now(),
                            "generation_count": roadmap_doc["generation_count"],
                            "base_roadmap_id": best_match.get('_id')
                        }
                    }
                )
                
                if result.modified_count > 0:
                    print(f"Updated existing roadmap for user {request.user_id} (generation #{roadmap_doc['generation_count']})")
                else:
                    print(f"No changes made to roadmap for user {request.user_id}")
                
                # Update response with existing roadmap ID
                response.id = existing_roadmap["roadmap_id"]
            else:
                # Insert new roadmap
                roadmap_collection.insert_one(roadmap_doc)
                print(f"Created new roadmap for user {request.user_id}")
        else:
            # Insert new roadmap without user_id
            roadmap_collection.insert_one(roadmap_doc)
            print(f"Created new roadmap (no user)")
        
        return response
        
    except Exception as e:
        print(f"Error generating roadmap: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating roadmap: {str(e)}")

@app.get("/api/roadmap/roadmaps/domains", response_model=DomainResponse)
async def get_available_domains():
    """Get list of available domains from MongoDB"""
    try:
        # Get unique domains from MongoDB
        domains = roadmap_collection.distinct("domain")
        return DomainResponse(domains=domains)
    except Exception as e:
        print(f"Error getting domains: {e}")
        return DomainResponse(domains=[])

@app.get("/api/roadmap/roadmaps/similar")
async def get_similar_roadmaps(goal: str, domain: Optional[str] = None, limit: int = 5):
    """Get similar roadmaps based on goal from MongoDB"""
    try:
        # Build MongoDB query
        query = {}
        if domain:
            query["domain"] = {"$regex": domain, "$options": "i"}
        
        # Get roadmaps from MongoDB
        roadmaps = list(roadmap_collection.find(query).limit(limit * 2))  # Get more to filter
        
        if not roadmaps:
            return {"roadmaps": []}
        
        # Simple similarity scoring
        goal_lower = goal.lower()
        scored_roadmaps = []
        
        for roadmap in roadmaps:
            score = 0
            roadmap_goal = roadmap['goal'].lower()
            
            # Check for keyword matches
            goal_words = goal_lower.split()
            for word in goal_words:
                if word in roadmap_goal:
                    score += 1
            
            if score > 0:
                # Convert MongoDB document to dict and remove _id
                roadmap_dict = {k: v for k, v in roadmap.items() if k != '_id'}
                scored_roadmaps.append((score, roadmap_dict))
        
        # Sort by score and return top results
        scored_roadmaps.sort(key=lambda x: x[0], reverse=True)
        similar_roadmaps = [roadmap for _, roadmap in scored_roadmaps[:limit]]
        
        return {"roadmaps": similar_roadmaps}
        
    except Exception as e:
        print(f"Error finding similar roadmaps: {e}")
        raise HTTPException(status_code=500, detail=f"Error finding similar roadmaps: {str(e)}")

@app.get("/api/roadmap/roadmaps/user/{user_id}", response_model=UserRoadmapsResponse)
async def get_user_roadmaps(user_id: str):
    """Get saved roadmaps for a user from MongoDB"""
    try:
        # Get user roadmaps from MongoDB
        user_roadmaps = list(roadmap_collection.find(
            {"user_id": user_id, "source": "user_generated"}
        ).sort("updated_at", -1))  # Sort by updated_at to show most recently modified first
        
        # Convert MongoDB documents to dict format
        roadmaps = []
        for roadmap in user_roadmaps:
            roadmap_dict = {
                "_id": str(roadmap["_id"]),
                "id": roadmap["roadmap_id"],
                "title": roadmap.get("title", roadmap["goal"]),  # Use title field, fallback to goal
                "goal": roadmap["goal"],
                "domain": roadmap["domain"],
                "steps": roadmap["steps"],
                "created_at": roadmap["created_at"].isoformat(),
                "updated_at": roadmap.get("updated_at", roadmap["created_at"]).isoformat(),
                "generation_count": roadmap.get("generation_count", 1)
            }
            roadmaps.append(roadmap_dict)
        
        return UserRoadmapsResponse(roadmaps=roadmaps)
        
    except Exception as e:
        print(f"Error getting user roadmaps: {e}")
        return UserRoadmapsResponse(roadmaps=[])

@app.get("/api/roadmap/roadmaps/all")
async def get_all_generated_roadmaps(limit: int = 50, skip: int = 0):
    """Get all generated roadmaps from MongoDB"""
    try:
        # Get all user-generated roadmaps
        roadmaps = list(roadmap_collection.find(
            {"source": "user_generated"}
        ).sort("updated_at", -1).skip(skip).limit(limit))
        
        # Convert MongoDB documents to dict format
        roadmap_list = []
        for roadmap in roadmaps:
            roadmap_dict = {
                "_id": str(roadmap["_id"]),
                "id": roadmap["roadmap_id"],
                "title": roadmap.get("title", roadmap["goal"]),  # Use title field, fallback to goal
                "goal": roadmap["goal"],
                "domain": roadmap["domain"],
                "steps": roadmap["steps"],
                "created_at": roadmap["created_at"].isoformat(),
                "updated_at": roadmap.get("updated_at", roadmap["created_at"]).isoformat(),
                "generation_count": roadmap.get("generation_count", 1),
                "user_id": roadmap.get("user_id")
            }
            roadmap_list.append(roadmap_dict)
        
        # Get total count
        total_count = roadmap_collection.count_documents({"source": "user_generated"})
        
        return {
            "roadmaps": roadmap_list,
            "total": total_count,
            "limit": limit,
            "skip": skip
        }
        
    except Exception as e:
        print(f"Error getting all roadmaps: {e}")
        return {"roadmaps": [], "total": 0, "limit": limit, "skip": skip}

@app.delete("/api/roadmap/roadmaps/{roadmap_id}")
async def delete_roadmap(roadmap_id: str, user_id: str):
    """Delete a saved roadmap from MongoDB"""
    try:
        # Delete roadmap from MongoDB
        result = roadmap_collection.delete_one({
            "roadmap_id": roadmap_id,
            "user_id": user_id,
            "source": "user_generated"
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Roadmap not found")
        
        return {"message": "Roadmap deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting roadmap: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting roadmap: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
