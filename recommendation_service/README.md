# Project Recommendation System Microservice

An AI-powered recommendation system that suggests personalized project ideas based on user goals, skill levels, and preferences.

## 🚀 Features

- **ML-Powered Recommendations**: Uses TF-IDF and cosine similarity for content-based filtering
- **Collaborative Filtering**: Learns from user feedback and similar users
- **Hybrid Approach**: Combines multiple recommendation strategies
- **Smart Matching**: Matches user goals to relevant project categories
- **Comprehensive Dataset**: 200+ curated project ideas across multiple domains
- **RESTful API**: FastAPI-based with automatic documentation

## 📊 Project Categories

- **Web Development**: Frontend, Backend, Full-stack applications
- **Mobile Development**: React Native, Flutter, Native apps
- **Data Science & ML**: Analysis, Visualization, Machine Learning models
- **DevOps & Cloud**: Docker, CI/CD, Infrastructure as Code
- **Game Development**: 2D/3D games, Web games, Mobile games
- **Desktop Applications**: Electron, Native desktop apps

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework
- **scikit-learn**: Machine learning algorithms
- **pandas/numpy**: Data processing
- **TF-IDF**: Text vectorization for content-based filtering
- **Cosine Similarity**: Recommendation scoring
- **Pydantic**: Data validation

## 📁 Project Structure

```
recommendation_service/
├── main.py                 # FastAPI application
├── ml_models.py           # ML recommendation engine
├── dataset_generator.py   # Project dataset generator
├── start_server.py        # Server startup script
├── start_server.bat       # Windows batch file
├── test_api.py           # API testing script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Dataset

```bash
python dataset_generator.py
```

### 3. Start Server

```bash
python main.py
```

Or on Windows:
```bash
start_server.bat
```

### 4. Test API

```bash
python test_api.py
```

The service will run on **port 8002** to avoid conflicts with other services.

## 📡 API Endpoints

### Core Endpoints

- `POST /api/recommend/projects` - Get personalized recommendations
- `GET /api/recommend/categories` - Get available categories
- `POST /api/recommend/feedback` - Submit user feedback
- `GET /api/recommend/trending` - Get trending projects
- `GET /api/recommend/statistics` - Get domain statistics

### Filtering Endpoints

- `GET /api/recommend/projects/by-difficulty/{difficulty}` - Filter by difficulty
- `GET /api/recommend/projects/by-technology/{technology}` - Filter by technology
- `GET /api/recommend/projects/search` - Text search projects

## 💡 Usage Examples

### Get Recommendations

```python
import requests

# Basic recommendation
response = requests.post("http://localhost:8002/api/recommend/projects", json={
    "goal": "I want to become a full-stack developer",
    "domain": "web-development",
    "difficulty": "intermediate",
    "limit": 5
})

recommendations = response.json()
```

### Search Projects

```python
# Search for React projects
response = requests.get("http://localhost:8002/api/recommend/projects/search?query=React&limit=10")
```

### Submit Feedback

```python
# Submit user feedback
response = requests.post("http://localhost:8002/api/recommend/feedback", json={
    "user_id": "user123",
    "project_id": "web_001",
    "rating": 5,
    "feedback": "Great project for learning!"
})
```

## 🧠 ML Algorithm Details

### Content-Based Filtering
- Uses TF-IDF vectorization on project descriptions, technologies, and categories
- Calculates cosine similarity between user goals and project features
- Provides personalized recommendations based on content similarity

### Collaborative Filtering
- Learns from user interactions and ratings
- Finds similar users based on project preferences
- Recommends projects liked by similar users

### Hybrid Approach
- Combines content-based and collaborative filtering
- Weighted scoring system (default: 70% content, 30% collaborative)
- Continuously improves with user feedback

## 📈 Dataset Statistics

The system includes 200+ project ideas with:
- **6 Domains**: Web Dev, Mobile, Data Science, DevOps, Games, Desktop
- **3 Difficulty Levels**: Beginner, Intermediate, Advanced
- **50+ Technologies**: React, Python, Docker, Machine Learning, etc.
- **Rich Metadata**: Prerequisites, learning objectives, time estimates

## 🔧 Configuration

### Environment Variables
- `PORT`: Server port (default: 8001)
- `HOST`: Server host (default: 0.0.0.0)

### ML Parameters
- `content_weight`: Weight for content-based filtering (default: 0.7)
- `collaborative_weight`: Weight for collaborative filtering (default: 0.3)
- `max_features`: TF-IDF max features (default: 1000)

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_api.py
```

Tests include:
- Health check
- Recommendation generation
- Category filtering
- Search functionality
- Feedback submission
- Statistics retrieval

## 📊 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8002/docs
- **ReDoc**: http://localhost:8002/redoc

## 🔄 Integration with PathWise

This service integrates with your existing PathWise system:
- Connects to the same MongoDB database
- Works alongside the roadmap API
- Can be called from the dashboard frontend
- Stores user preferences for continuous improvement

## 🚀 Deployment

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Production Considerations
- Use a production ASGI server like Gunicorn
- Set up proper logging and monitoring
- Implement rate limiting
- Add authentication if needed
- Use a proper database for user interactions

## 🤝 Contributing

1. Add new project ideas to `dataset_generator.py`
2. Improve ML algorithms in `ml_models.py`
3. Add new API endpoints in `main.py`
4. Update tests in `test_api.py`

## 📝 License

This project is part of the PathWise system and follows the same licensing terms.
