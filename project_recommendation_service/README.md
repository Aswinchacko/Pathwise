# Project Recommendation Service

Microservice that recommends projects based on completed roadmap topics.

## Features

- **Smart Recommendations**: Suggests projects based on completed skills and domain
- **Difficulty Scaling**: Adjusts project difficulty based on completion percentage
- **Skill Matching**: Calculates how well completed topics match project requirements
- **Progress Tracking**: Provides milestone messages based on completion percentage

## API Endpoints

### `POST /api/projects/recommend`
Get project recommendations based on completed topics.

**Request Body:**
```json
{
  "user_id": "user123",
  "roadmap_id": "roadmap_20240101_123456_7890",
  "completed_topics": ["Python", "Pandas", "NumPy"],
  "domain": "Data Science",
  "completion_percentage": 45.5
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "project_id": "ds_001",
      "title": "Stock Price Prediction Model",
      "description": "Build a machine learning model...",
      "difficulty": "intermediate",
      "estimated_duration": "3-4 weeks",
      "skills_required": ["Python", "Pandas", "NumPy", "Scikit-learn"],
      "skills_learned": ["Time Series Analysis", "Feature Engineering"],
      "project_type": "data_analysis",
      "github_template": "https://github.com/example/stock-prediction",
      "tutorial_links": ["https://www.kaggle.com/learn/..."],
      "tags": ["finance", "machine-learning", "time-series"]
    }
  ],
  "message": "Found 3 project recommendations based on your progress!",
  "completion_percentage": 45.5,
  "next_milestone": "Great progress! Try some beginner projects to apply your skills."
}
```

### `GET /api/projects/domains`
Get list of available domains with project counts.

### `GET /api/projects/domain/{domain}`
Get all projects for a specific domain.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Service

```bash
python main.py
```

The service will run on `http://localhost:8003`

## Environment Variables

- `MONGODB_URL`: MongoDB connection string (default: mongodb://localhost:27017)
- `ROADMAP_API_URL`: Roadmap API URL (default: http://localhost:8001)
- `RECOMMENDATION_SERVICE_URL`: Recommendation service URL (default: http://localhost:8002)

## Project Database

Projects are organized by domain:
- **Data Science**: ML models, data analysis projects
- **Frontend Development**: Web applications, dashboards
- **Backend Development**: APIs, microservices
- **Mobile Development**: Mobile apps, cross-platform solutions

Each project includes:
- Difficulty level (beginner, intermediate, advanced)
- Required skills and skills to be learned
- Estimated duration
- GitHub templates and tutorial links
- Project type and tags

