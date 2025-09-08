# Mentor Recommendation Service

Web scraping microservice for finding mentors in specific topics/domains.

## Features

- **Multi-Platform Scraping**: Searches LinkedIn, GitHub, and Stack Overflow
- **Smart Matching**: Matches mentors based on skills, experience, and availability
- **Relevance Scoring**: Calculates mentor relevance based on topic overlap and experience level
- **Real-time Data**: Scrapes live data from professional platforms

## API Endpoints

### `POST /api/mentors/recommend`
Get mentor recommendations based on domain and topics.

**Request Body:**
```json
{
  "user_id": "user123",
  "domain": "Data Science",
  "topics": ["Machine Learning", "Python", "Pandas"],
  "experience_level": "intermediate",
  "preferred_platforms": ["linkedin", "github", "stackoverflow"]
}
```

**Response:**
```json
{
  "mentors": [
    {
      "mentor_id": "mentor_ds_001",
      "name": "Dr. Sarah Chen",
      "title": "Senior Data Scientist",
      "company": "Google",
      "location": "San Francisco, CA",
      "expertise": ["Machine Learning", "Deep Learning", "Python"],
      "experience_years": 8,
      "rating": 4.9,
      "profile_url": "https://linkedin.com/in/sarah-chen-ds",
      "platform": "linkedin",
      "bio": "Experienced data scientist with expertise in ML...",
      "skills": ["Python", "R", "TensorFlow", "PyTorch"],
      "availability": "available",
      "contact_info": {
        "email": "sarah.chen@example.com",
        "linkedin": "https://linkedin.com/in/sarah-chen-ds"
      }
    }
  ],
  "total_found": 5,
  "search_criteria": {
    "domain": "Data Science",
    "topics": ["Machine Learning", "Python", "Pandas"],
    "experience_level": "intermediate",
    "platforms": ["linkedin", "github", "stackoverflow"]
  },
  "message": "Found 5 mentors matching your criteria!"
}
```

### `GET /api/mentors/domains`
Get list of available domains with mentor counts.

### `GET /api/mentors/domain/{domain}`
Get all mentors for a specific domain.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Service

```bash
python main.py
```

The service will run on `http://localhost:8004`

## Environment Variables

- `MONGODB_URL`: MongoDB connection string (default: mongodb://localhost:27017)
- `ROADMAP_API_URL`: Roadmap API URL (default: http://localhost:8001)

## Web Scraping

The service scrapes mentors from:
- **LinkedIn**: Professional profiles and expertise
- **GitHub**: Open source contributors and developers
- **Stack Overflow**: Technical experts and community leaders

### Note on Scraping
- LinkedIn scraping requires proper authentication and handling of anti-bot measures
- GitHub API is used for better reliability
- Stack Overflow has strict scraping policies - use their official API in production
- Rate limiting is implemented to respect platform policies

## Mentor Database

Sample mentors are organized by domain:
- **Data Science**: ML engineers, data scientists, researchers
- **Frontend Development**: React/Vue experts, UI/UX developers
- **Backend Development**: API developers, system architects

Each mentor profile includes:
- Professional information and experience
- Skills and expertise areas
- Availability status
- Contact information
- Platform-specific profile URLs

