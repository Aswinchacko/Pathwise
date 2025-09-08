"""
Recommendation System Microservice
FastAPI-based service for recommending project ideas based on user goals
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import os
from datetime import datetime
import json

from ml_models import ProjectRecommendationEngine

# Initialize FastAPI app
app = FastAPI(
    title="Project Recommendation API",
    description="AI-powered project recommendation system for developers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommendation engine
try:
    recommendation_engine = ProjectRecommendationEngine()
    print("Recommendation engine initialized successfully")
except Exception as e:
    print(f"Error initializing recommendation engine: {e}")
    recommendation_engine = None

# Pydantic models
class RecommendationRequest(BaseModel):
    goal: str = Field(..., description="User's career goal or learning objective")
    domain: Optional[str] = Field(None, description="Preferred domain (web-development, data-science, etc.)")
    difficulty: Optional[str] = Field(None, description="Preferred difficulty level (beginner, intermediate, advanced)")
    user_id: Optional[str] = Field(None, description="User ID for personalized recommendations")
    limit: Optional[int] = Field(10, description="Number of recommendations to return", ge=1, le=50)

class FeedbackRequest(BaseModel):
    user_id: str = Field(..., description="User ID")
    project_id: str = Field(..., description="Project ID")
    rating: int = Field(..., description="Rating from 1-5", ge=1, le=5)
    feedback: Optional[str] = Field(None, description="Optional text feedback")

class ProjectResponse(BaseModel):
    project_id: str
    title: str
    description: str
    difficulty: str
    estimated_time: str
    technologies: List[str]
    categories: List[str]
    learning_objectives: List[str]
    prerequisites: List[str]
    project_type: str
    domain: str
    complexity_score: int
    popularity_score: float
    tags: List[str]
    similarity_score: Optional[float] = None
    final_score: Optional[float] = None
    content_score: Optional[float] = None
    collaborative_score: Optional[float] = None

class RecommendationResponse(BaseModel):
    recommendations: List[ProjectResponse]
    total_count: int
    user_goal: str
    domain: Optional[str] = None
    difficulty: Optional[str] = None
    algorithm_used: str

class DomainStatsResponse(BaseModel):
    domains: Dict[str, int]
    difficulties: Dict[str, int]
    technologies: Dict[str, int]
    avg_complexity_by_domain: Dict[str, float]

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        if recommendation_engine is None:
            return {
                "status": "unhealthy", 
                "service": "recommendation-api",
                "error": "Recommendation engine not initialized"
            }
        
        # Test basic functionality
        test_recs = recommendation_engine.content_based_recommendations("test", limit=1)
        
        return {
            "status": "healthy",
            "service": "recommendation-api",
            "engine_status": "operational",
            "total_projects": len(recommendation_engine.projects_df) if recommendation_engine else 0
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "recommendation-api",
            "error": str(e)
        }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Project Recommendation API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/api/recommend/projects", response_model=RecommendationResponse)
async def get_project_recommendations(request: RecommendationRequest):
    """Get personalized project recommendations based on user goals"""
    
    if recommendation_engine is None:
        raise HTTPException(status_code=500, detail="Recommendation engine not available")
    
    try:
        # Get hybrid recommendations
        recommendations = recommendation_engine.hybrid_recommendations(
            user_goal=request.goal,
            user_id=request.user_id,
            user_domain=request.domain,
            difficulty_preference=request.difficulty,
            limit=request.limit
        )
        
        # Convert to response format
        project_responses = []
        for rec in recommendations:
            project_responses.append(ProjectResponse(
                project_id=rec['project_id'],
                title=rec['title'],
                description=rec['description'],
                difficulty=rec['difficulty'],
                estimated_time=rec['estimated_time'],
                technologies=rec['technologies'],
                categories=rec['categories'],
                learning_objectives=rec['learning_objectives'],
                prerequisites=rec['prerequisites'],
                project_type=rec['project_type'],
                domain=rec['domain'],
                complexity_score=rec['complexity_score'],
                popularity_score=rec['popularity_score'],
                tags=rec['tags'],
                similarity_score=rec.get('similarity_score'),
                final_score=rec.get('final_score'),
                content_score=rec.get('content_score'),
                collaborative_score=rec.get('collaborative_score')
            ))
        
        return RecommendationResponse(
            recommendations=project_responses,
            total_count=len(project_responses),
            user_goal=request.goal,
            domain=request.domain,
            difficulty=request.difficulty,
            algorithm_used="hybrid"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.get("/api/recommend/categories")
async def get_project_categories():
    """Get available project categories and domains"""
    
    if recommendation_engine is None:
        raise HTTPException(status_code=500, detail="Recommendation engine not available")
    
    try:
        # Get unique domains
        domains = recommendation_engine.projects_df['domain'].unique().tolist()
        
        # Get unique difficulties
        difficulties = recommendation_engine.projects_df['difficulty'].unique().tolist()
        
        # Get all unique categories
        all_categories = set()
        for categories in recommendation_engine.projects_df['categories']:
            all_categories.update(categories)
        
        # Get all unique technologies
        all_technologies = set()
        for techs in recommendation_engine.projects_df['technologies']:
            all_technologies.update(techs)
        
        return {
            "domains": domains,
            "difficulties": difficulties,
            "categories": sorted(list(all_categories)),
            "technologies": sorted(list(all_technologies))[:50]  # Top 50 technologies
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting categories: {str(e)}")

@app.post("/api/recommend/feedback")
async def submit_feedback(request: FeedbackRequest):
    """Submit user feedback for a project recommendation"""
    
    if recommendation_engine is None:
        raise HTTPException(status_code=500, detail="Recommendation engine not available")
    
    try:
        # Add user feedback
        recommendation_engine.add_user_feedback(
            user_id=request.user_id,
            project_id=request.project_id,
            rating=request.rating,
            feedback=request.feedback
        )
        
        return {
            "message": "Feedback submitted successfully",
            "user_id": request.user_id,
            "project_id": request.project_id,
            "rating": request.rating
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")

@app.get("/api/recommend/trending")
async def get_trending_projects(
    domain: Optional[str] = Query(None, description="Filter by domain"),
    limit: int = Query(10, description="Number of projects to return", ge=1, le=50)
):
    """Get trending projects based on popularity scores"""
    
    if recommendation_engine is None:
        raise HTTPException(status_code=500, detail="Recommendation engine not available")
    
    try:
        trending = recommendation_engine.get_trending_projects(domain=domain, limit=limit)
        
        # Convert to response format
        project_responses = []
        for project in trending:
            project_responses.append(ProjectResponse(
                project_id=project['project_id'],
                title=project['title'],
                description=project['description'],
                difficulty=project['difficulty'],
                estimated_time=project['estimated_time'],
                technologies=project['technologies'],
                categories=project['categories'],
                learning_objectives=project['learning_objectives'],
                prerequisites=project['prerequisites'],
                project_type=project['project_type'],
                domain=project['domain'],
                complexity_score=project['complexity_score'],
                popularity_score=project['popularity_score'],
                tags=project['tags']
            ))
        
        return {
            "trending_projects": project_responses,
            "total_count": len(project_responses),
            "domain": domain
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting trending projects: {str(e)}")

@app.get("/api/recommend/projects/by-difficulty/{difficulty}")
async def get_projects_by_difficulty(
    difficulty: str,
    limit: int = Query(10, description="Number of projects to return", ge=1, le=50)
):
    """Get projects filtered by difficulty level"""
    
    if recommendation_engine is None:
        raise HTTPException(status_code=500, detail="Recommendation engine not available")
    
    if difficulty not in ['beginner', 'intermediate', 'advanced']:
        raise HTTPException(status_code=400, detail="Invalid difficulty level. Must be: beginner, intermediate, or advanced")
    
    try:
        projects = recommendation_engine.get_projects_by_difficulty(difficulty, limit)
        
        # Convert to response format
        project_responses = []
        for project in projects:
            project_responses.append(ProjectResponse(
                project_id=project['project_id'],
                title=project['title'],
                description=project['description'],
                difficulty=project['difficulty'],
                estimated_time=project['estimated_time'],
                technologies=project['technologies'],
                categories=project['categories'],
                learning_objectives=project['learning_objectives'],
                prerequisites=project['prerequisites'],
                project_type=project['project_type'],
                domain=project['domain'],
                complexity_score=project['complexity_score'],
                popularity_score=project['popularity_score'],
                tags=project['tags']
            ))
        
        return {
            "projects": project_responses,
            "total_count": len(project_responses),
            "difficulty": difficulty
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting projects by difficulty: {str(e)}")

@app.get("/api/recommend/projects/by-technology/{technology}")
async def get_projects_by_technology(
    technology: str,
    limit: int = Query(10, description="Number of projects to return", ge=1, le=50)
):
    """Get projects that use a specific technology"""
    
    if recommendation_engine is None:
        raise HTTPException(status_code=500, detail="Recommendation engine not available")
    
    try:
        projects = recommendation_engine.get_projects_by_technology(technology, limit)
        
        # Convert to response format
        project_responses = []
        for project in projects:
            project_responses.append(ProjectResponse(
                project_id=project['project_id'],
                title=project['title'],
                description=project['description'],
                difficulty=project['difficulty'],
                estimated_time=project['estimated_time'],
                technologies=project['technologies'],
                categories=project['categories'],
                learning_objectives=project['learning_objectives'],
                prerequisites=project['prerequisites'],
                project_type=project['project_type'],
                domain=project['domain'],
                complexity_score=project['complexity_score'],
                popularity_score=project['popularity_score'],
                tags=project['tags']
            ))
        
        return {
            "projects": project_responses,
            "total_count": len(project_responses),
            "technology": technology
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting projects by technology: {str(e)}")

@app.get("/api/recommend/statistics", response_model=DomainStatsResponse)
async def get_domain_statistics():
    """Get statistics about project distribution across domains"""
    
    if recommendation_engine is None:
        raise HTTPException(status_code=500, detail="Recommendation engine not available")
    
    try:
        stats = recommendation_engine.get_domain_statistics()
        
        return DomainStatsResponse(
            domains=stats['domains'],
            difficulties=stats['difficulties'],
            technologies=stats['technologies'],
            avg_complexity_by_domain=stats['avg_complexity_by_domain']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")

@app.get("/api/recommend/projects/search")
async def search_projects(
    query: str = Query(..., description="Search query"),
    domain: Optional[str] = Query(None, description="Filter by domain"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    limit: int = Query(10, description="Number of projects to return", ge=1, le=50)
):
    """Search projects using text search"""
    
    if recommendation_engine is None:
        raise HTTPException(status_code=500, detail="Recommendation engine not available")
    
    try:
        # Use content-based recommendations for search
        recommendations = recommendation_engine.content_based_recommendations(
            user_goal=query,
            user_domain=domain,
            difficulty_preference=difficulty,
            limit=limit
        )
        
        # Convert to response format
        project_responses = []
        for rec in recommendations:
            project_responses.append(ProjectResponse(
                project_id=rec['project_id'],
                title=rec['title'],
                description=rec['description'],
                difficulty=rec['difficulty'],
                estimated_time=rec['estimated_time'],
                technologies=rec['technologies'],
                categories=rec['categories'],
                learning_objectives=rec['learning_objectives'],
                prerequisites=rec['prerequisites'],
                project_type=rec['project_type'],
                domain=rec['domain'],
                complexity_score=rec['complexity_score'],
                popularity_score=rec['popularity_score'],
                tags=rec['tags'],
                similarity_score=rec.get('similarity_score')
            ))
        
        return {
            "search_results": project_responses,
            "total_count": len(project_responses),
            "query": query,
            "domain": domain,
            "difficulty": difficulty
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching projects: {str(e)}")

if __name__ == "__main__":
    # Generate dataset if it doesn't exist
    if not os.path.exists("project_dataset.json"):
        print("Generating project dataset...")
        from dataset_generator import save_dataset
        save_dataset()
    
    # Load user interactions if they exist
    if recommendation_engine:
        recommendation_engine.load_user_interactions()
    
    # Run the server
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8002,  # Different port from roadmap API (8000) and resume parser (8001)
        reload=True
    )
