"""
Mentor Recommendation Service
Web scraping service for finding mentors in specific topics/domains
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import asyncio
import aiohttp
import re

load_dotenv()

app = FastAPI(title="Mentor Recommendation Service", version="1.0.0")

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
ROADMAP_API_URL = os.getenv("ROADMAP_API_URL", "http://localhost:8001")

class MentorRecommendationRequest(BaseModel):
    user_id: str
    domain: str
    topics: List[str]
    experience_level: str = "intermediate"  # beginner, intermediate, advanced
    preferred_platforms: List[str] = ["linkedin", "github", "stackoverflow"]

class MentorProfile(BaseModel):
    mentor_id: str
    name: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    expertise: List[str]
    experience_years: Optional[int] = None
    rating: Optional[float] = None
    profile_url: str
    platform: str  # linkedin, github, stackoverflow, etc.
    bio: Optional[str] = None
    skills: List[str]
    availability: str = "unknown"  # available, busy, unknown
    contact_info: Optional[Dict[str, str]] = None

class MentorRecommendationResponse(BaseModel):
    mentors: List[MentorProfile]
    total_found: int
    search_criteria: Dict[str, Any]
    message: str

# Web scraping configurations
SCRAPING_CONFIGS = {
    "linkedin": {
        "base_url": "https://www.linkedin.com/search/results/people/",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        "search_params": {
            "keywords": "{topic}",
            "origin": "GLOBAL_SEARCH_HEADER",
            "page": "1"
        }
    },
    "github": {
        "base_url": "https://api.github.com/search/users",
        "headers": {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "MentorRecommendationService/1.0"
        },
        "search_params": {
            "q": "{topic}",
            "sort": "followers",
            "order": "desc",
            "per_page": "20"
        }
    },
    "stackoverflow": {
        "base_url": "https://stackoverflow.com/users",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    }
}

# Sample mentor database (in production, this would be populated by scraping)
SAMPLE_MENTORS = {
    "Data Science": [
        {
            "mentor_id": "mentor_ds_001",
            "name": "Dr. Sarah Chen",
            "title": "Senior Data Scientist",
            "company": "Google",
            "location": "San Francisco, CA",
            "expertise": ["Machine Learning", "Deep Learning", "Python", "TensorFlow"],
            "experience_years": 8,
            "rating": 4.9,
            "profile_url": "https://linkedin.com/in/sarah-chen-ds",
            "platform": "linkedin",
            "bio": "Experienced data scientist with expertise in ML and deep learning. Passionate about mentoring newcomers.",
            "skills": ["Python", "R", "TensorFlow", "PyTorch", "Pandas", "Scikit-learn"],
            "availability": "available",
            "contact_info": {"email": "sarah.chen@example.com", "linkedin": "https://linkedin.com/in/sarah-chen-ds"}
        },
        {
            "mentor_id": "mentor_ds_002",
            "name": "Alex Rodriguez",
            "title": "ML Engineer",
            "company": "Microsoft",
            "location": "Seattle, WA",
            "expertise": ["Computer Vision", "NLP", "Python", "PyTorch"],
            "experience_years": 6,
            "rating": 4.7,
            "profile_url": "https://github.com/alex-rodriguez-ml",
            "platform": "github",
            "bio": "Open source contributor and ML engineer. Active in the data science community.",
            "skills": ["Python", "PyTorch", "OpenCV", "NLTK", "spaCy", "Docker"],
            "availability": "available",
            "contact_info": {"github": "https://github.com/alex-rodriguez-ml"}
        }
    ],
    "Frontend Development": [
        {
            "mentor_id": "mentor_fe_001",
            "name": "Emily Johnson",
            "title": "Senior Frontend Developer",
            "company": "Netflix",
            "location": "Los Gatos, CA",
            "expertise": ["React", "TypeScript", "Next.js", "Web Performance"],
            "experience_years": 7,
            "rating": 4.8,
            "profile_url": "https://linkedin.com/in/emily-johnson-fe",
            "platform": "linkedin",
            "bio": "Frontend expert with focus on React ecosystem and performance optimization.",
            "skills": ["React", "TypeScript", "Next.js", "GraphQL", "Jest", "Webpack"],
            "availability": "available",
            "contact_info": {"email": "emily.johnson@example.com", "linkedin": "https://linkedin.com/in/emily-johnson-fe"}
        },
        {
            "mentor_id": "mentor_fe_002",
            "name": "David Kim",
            "title": "Full Stack Developer",
            "company": "Stripe",
            "location": "San Francisco, CA",
            "expertise": ["Vue.js", "Node.js", "AWS", "Microservices"],
            "experience_years": 5,
            "rating": 4.6,
            "profile_url": "https://github.com/david-kim-dev",
            "platform": "github",
            "bio": "Full stack developer with expertise in modern web technologies and cloud architecture.",
            "skills": ["Vue.js", "Node.js", "AWS", "Docker", "Kubernetes", "PostgreSQL"],
            "availability": "busy",
            "contact_info": {"github": "https://github.com/david-kim-dev"}
        }
    ],
    "Backend Development": [
        {
            "mentor_id": "mentor_be_001",
            "name": "Michael Brown",
            "title": "Principal Software Engineer",
            "company": "Amazon",
            "location": "Seattle, WA",
            "expertise": ["Microservices", "AWS", "Python", "System Design"],
            "experience_years": 10,
            "rating": 4.9,
            "profile_url": "https://linkedin.com/in/michael-brown-be",
            "platform": "linkedin",
            "bio": "Experienced backend engineer specializing in scalable systems and cloud architecture.",
            "skills": ["Python", "Java", "AWS", "Docker", "Kubernetes", "PostgreSQL", "Redis"],
            "availability": "available",
            "contact_info": {"email": "michael.brown@example.com", "linkedin": "https://linkedin.com/in/michael-brown-be"}
        }
    ]
}

async def scrape_linkedin_mentors(topic: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Scrape LinkedIn for mentors in specific topic"""
    # Note: This is a simplified example. Real LinkedIn scraping requires proper authentication
    # and handling of anti-bot measures. In production, use LinkedIn API or official partnerships.
    
    mentors = []
    try:
        # Simulate scraping delay
        await asyncio.sleep(1)
        
        # Mock data for demonstration
        mock_mentors = [
            {
                "mentor_id": f"linkedin_mentor_{topic}_{i}",
                "name": f"LinkedIn Expert {i+1}",
                "title": f"Senior {topic} Professional",
                "company": "Tech Company",
                "location": "San Francisco, CA",
                "expertise": [topic, "Leadership", "Strategy"],
                "experience_years": 5 + i,
                "rating": 4.5 + (i * 0.1),
                "profile_url": f"https://linkedin.com/in/expert-{topic}-{i}",
                "platform": "linkedin",
                "bio": f"Experienced {topic} professional with {5+i} years of experience.",
                "skills": [topic, "Leadership", "Communication"],
                "availability": "available" if i % 2 == 0 else "busy",
                "contact_info": {"linkedin": f"https://linkedin.com/in/expert-{topic}-{i}"}
            }
            for i in range(min(limit, 3))
        ]
        mentors.extend(mock_mentors)
        
    except Exception as e:
        print(f"Error scraping LinkedIn: {e}")
    
    return mentors

async def scrape_github_mentors(topic: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Scrape GitHub for mentors in specific topic"""
    mentors = []
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.github.com/search/users?q={topic}+in:bio+type:user&sort=followers&order=desc&per_page={limit}"
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "MentorRecommendationService/1.0"
            }
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    for i, user in enumerate(data.get("items", [])[:limit]):
                        mentor = {
                            "mentor_id": f"github_mentor_{topic}_{i}",
                            "name": user.get("login", "GitHub User"),
                            "title": "Open Source Contributor",
                            "company": None,
                            "location": None,
                            "expertise": [topic, "Open Source", "Software Development"],
                            "experience_years": None,
                            "rating": 4.0 + (i * 0.2),
                            "profile_url": user.get("html_url", ""),
                            "platform": "github",
                            "bio": user.get("bio", f"GitHub user interested in {topic}"),
                            "skills": [topic, "Git", "Open Source"],
                            "availability": "unknown",
                            "contact_info": {"github": user.get("html_url", "")}
                        }
                        mentors.append(mentor)
                        
    except Exception as e:
        print(f"Error scraping GitHub: {e}")
    
    return mentors

async def scrape_stackoverflow_mentors(topic: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Scrape Stack Overflow for mentors in specific topic"""
    # Note: Stack Overflow has strict scraping policies. In production, use their API.
    mentors = []
    try:
        # Simulate scraping delay
        await asyncio.sleep(1)
        
        # Mock data for demonstration
        mock_mentors = [
            {
                "mentor_id": f"so_mentor_{topic}_{i}",
                "name": f"Stack Overflow Expert {i+1}",
                "title": f"{topic} Specialist",
                "company": "Software Company",
                "location": "Remote",
                "expertise": [topic, "Problem Solving", "Code Review"],
                "experience_years": 3 + i,
                "rating": 4.2 + (i * 0.1),
                "profile_url": f"https://stackoverflow.com/users/expert-{topic}-{i}",
                "platform": "stackoverflow",
                "bio": f"Active Stack Overflow contributor with expertise in {topic}.",
                "skills": [topic, "Debugging", "Code Review"],
                "availability": "available",
                "contact_info": {"stackoverflow": f"https://stackoverflow.com/users/expert-{topic}-{i}"}
            }
            for i in range(min(limit, 2))
        ]
        mentors.extend(mock_mentors)
        
    except Exception as e:
        print(f"Error scraping Stack Overflow: {e}")
    
    return mentors

async def find_mentors_by_topic(topic: str, platforms: List[str], limit_per_platform: int = 5) -> List[Dict[str, Any]]:
    """Find mentors across multiple platforms for a specific topic"""
    all_mentors = []
    
    # Get sample mentors from database
    for domain, mentors in SAMPLE_MENTORS.items():
        if topic.lower() in domain.lower() or any(topic.lower() in skill.lower() for mentor in mentors for skill in mentor["skills"]):
            all_mentors.extend(mentors[:2])  # Limit sample mentors
    
    # Scrape from platforms
    scraping_tasks = []
    
    if "linkedin" in platforms:
        scraping_tasks.append(scrape_linkedin_mentors(topic, limit_per_platform))
    if "github" in platforms:
        scraping_tasks.append(scrape_github_mentors(topic, limit_per_platform))
    if "stackoverflow" in platforms:
        scraping_tasks.append(scrape_stackoverflow_mentors(topic, limit_per_platform))
    
    if scraping_tasks:
        scraped_results = await asyncio.gather(*scraping_tasks, return_exceptions=True)
        for result in scraped_results:
            if isinstance(result, list):
                all_mentors.extend(result)
    
    # Remove duplicates based on name and platform
    seen = set()
    unique_mentors = []
    for mentor in all_mentors:
        key = (mentor["name"], mentor["platform"])
        if key not in seen:
            seen.add(key)
            unique_mentors.append(mentor)
    
    return unique_mentors

def calculate_mentor_relevance(mentor: Dict[str, Any], topics: List[str], experience_level: str) -> float:
    """Calculate how relevant a mentor is based on topics and experience level"""
    relevance_score = 0.0
    
    # Check topic overlap
    mentor_skills = [skill.lower() for skill in mentor.get("skills", [])]
    topic_matches = sum(1 for topic in topics if any(topic.lower() in skill for skill in mentor_skills))
    relevance_score += (topic_matches / len(topics)) * 0.6 if topics else 0
    
    # Check experience level match
    experience_years = mentor.get("experience_years", 0)
    if experience_level == "beginner" and experience_years >= 2:
        relevance_score += 0.2
    elif experience_level == "intermediate" and 3 <= experience_years <= 8:
        relevance_score += 0.2
    elif experience_level == "advanced" and experience_years >= 5:
        relevance_score += 0.2
    
    # Check availability
    if mentor.get("availability") == "available":
        relevance_score += 0.1
    elif mentor.get("availability") == "busy":
        relevance_score += 0.05
    
    # Check rating
    rating = mentor.get("rating", 0)
    if rating >= 4.5:
        relevance_score += 0.1
    elif rating >= 4.0:
        relevance_score += 0.05
    
    return min(relevance_score, 1.0)

@app.get("/")
async def root():
    return {"message": "Mentor Recommendation Service is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/mentors/recommend", response_model=MentorRecommendationResponse)
async def recommend_mentors(request: MentorRecommendationRequest):
    """Get mentor recommendations based on domain and topics"""
    try:
        all_mentors = []
        
        # Find mentors for each topic
        for topic in request.topics:
            topic_mentors = await find_mentors_by_topic(
                topic, 
                request.preferred_platforms, 
                limit_per_platform=3
            )
            all_mentors.extend(topic_mentors)
        
        # Remove duplicates and calculate relevance
        unique_mentors = []
        seen = set()
        
        for mentor in all_mentors:
            key = (mentor["name"], mentor["platform"])
            if key not in seen:
                seen.add(key)
                mentor["relevance_score"] = calculate_mentor_relevance(
                    mentor, 
                    request.topics, 
                    request.experience_level
                )
                unique_mentors.append(mentor)
        
        # Sort by relevance score
        unique_mentors.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Convert to MentorProfile objects
        mentor_profiles = []
        for mentor in unique_mentors[:10]:  # Top 10 mentors
            mentor_profiles.append(MentorProfile(**mentor))
        
        return MentorRecommendationResponse(
            mentors=mentor_profiles,
            total_found=len(mentor_profiles),
            search_criteria={
                "domain": request.domain,
                "topics": request.topics,
                "experience_level": request.experience_level,
                "platforms": request.preferred_platforms
            },
            message=f"Found {len(mentor_profiles)} mentors matching your criteria!"
        )
        
    except Exception as e:
        print(f"Error in mentor recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating mentor recommendations: {str(e)}")

@app.get("/api/mentors/domains")
async def get_available_domains():
    """Get list of domains with available mentors"""
    return {
        "domains": list(SAMPLE_MENTORS.keys()),
        "total_mentors": sum(len(mentors) for mentors in SAMPLE_MENTORS.values())
    }

@app.get("/api/mentors/domain/{domain}")
async def get_mentors_by_domain(domain: str):
    """Get all mentors for a specific domain"""
    if domain not in SAMPLE_MENTORS:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    mentors = [MentorProfile(**mentor) for mentor in SAMPLE_MENTORS[domain]]
    return {
        "domain": domain,
        "mentors": mentors,
        "count": len(mentors)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)

