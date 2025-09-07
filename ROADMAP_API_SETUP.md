# Roadmap Generator API Setup

This guide will help you set up the FastAPI-based roadmap generation system using the CSV data.

## Quick Start

### 1. Start the FastAPI Server

Navigate to the `roadmap_api` directory and run:

**Windows:**
```bash
cd roadmap_api
start_server.bat
```

**Linux/Mac:**
```bash
cd roadmap_api
python start_server.py
```

The API will be available at `http://localhost:8000`

### 2. Configure the Frontend

Create a `.env` file in the `dashboard` directory:

```bash
# In dashboard/.env
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Start the Dashboard

```bash
cd dashboard
npm run dev
```

## API Endpoints

- `POST /api/roadmap/generate-roadmap` - Generate a new roadmap
- `GET /api/roadmap/roadmaps/domains` - Get available domains  
- `GET /api/roadmap/roadmaps/similar` - Find similar roadmaps
- `GET /api/roadmap/roadmaps/user/{user_id}` - Get user's saved roadmaps
- `DELETE /api/roadmap/roadmaps/{roadmap_id}` - Delete a roadmap

## Testing

Run the test script to verify the API is working:

```bash
cd roadmap_api
python test_api.py
```

## Features

- **Smart Matching**: Uses keyword matching to find the best roadmap from the CSV data
- **Domain Filtering**: Filter roadmaps by specific domains
- **User Roadmaps**: Save and manage roadmaps for specific users
- **Similar Roadmaps**: Find similar roadmaps based on goals
- **CORS Enabled**: Ready for frontend integration

## Data Structure

The API parses the CSV roadmap data into structured format:

```json
{
  "id": "roadmap_20241201_143022_1234",
  "goal": "Become a Full Stack Developer", 
  "domain": "Frontend Development",
  "steps": [
    {
      "category": "Foundations",
      "skills": ["CSS Grid", "Responsive design", "Accessibility basics"]
    }
  ],
  "created_at": "2024-12-01T14:30:22"
}
```

## Troubleshooting

1. **CSV not found**: Ensure `cross_domain_roadmaps_520.csv` is in the `roadmap_api` directory
2. **Port already in use**: Change the port in `main.py` if 8000 is occupied
3. **CORS issues**: Update the allowed origins in `main.py` for your frontend URL
4. **Dependencies**: Run `pip install -r requirements.txt` if packages are missing
