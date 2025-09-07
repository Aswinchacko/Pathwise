# Roadmap Generator API

A FastAPI-based service for generating personalized learning roadmaps using CSV data.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy the CSV file to the API directory:
```bash
cp ../cross_domain_roadmaps_520.csv .
```

3. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /api/roadmap/generate-roadmap` - Generate a new roadmap
- `GET /api/roadmap/roadmaps/domains` - Get available domains
- `GET /api/roadmap/roadmaps/similar` - Find similar roadmaps
- `GET /api/roadmap/roadmaps/user/{user_id}` - Get user's saved roadmaps
- `DELETE /api/roadmap/roadmaps/{roadmap_id}` - Delete a roadmap

## Usage

The API expects requests in the format:
```json
{
  "goal": "Become a Full Stack Developer",
  "domain": "Frontend Development",
  "user_id": "optional_user_id"
}
```
