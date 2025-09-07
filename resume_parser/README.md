# Resume Parser API

A FastAPI-based service for parsing resumes and extracting structured information.

## Features

- **File Support**: PDF and DOCX files
- **Data Extraction**: Name, email, phone, skills, experience, education, etc.
- **CORS Enabled**: Ready for frontend integration
- **Error Handling**: Comprehensive error handling and validation
- **Auto-cleanup**: Temporary files are automatically removed after processing

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Spacy Model

```bash
python -m spacy download en_core_web_sm
```

### 3. Start the Server

```bash
python start_server.py
```

Or directly with uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Health Check
- **GET** `/health`
- Returns server status

### Upload Resume
- **POST** `/upload-resume`
- **Content-Type**: `multipart/form-data`
- **Body**: File (PDF or DOCX)
- **Response**: Parsed resume data

## Example Usage

```bash
curl -X POST "http://localhost:8000/upload-resume" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"
```

## Response Format

```json
{
  "status": "success",
  "message": "Resume parsed successfully",
  "data": {
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "location": "New York, NY",
    "summary": "Experienced software engineer...",
    "skills": ["Python", "JavaScript", "React"],
    "education": [
      {
        "degree": "B.Tech",
        "institution": "University Name",
        "year_start": "2018",
        "year_end": "2022"
      }
    ],
    "experience": [
      {
        "role": "Software Engineer",
        "company": "Tech Corp",
        "year_start": "2022",
        "year_end": "2024"
      }
    ],
    "linkedin": "linkedin.com/in/johndoe",
    "github": "github.com/johndoe"
  }
}
```

## Configuration

The server runs on `http://localhost:8000` by default. To change the port or host, modify the `start_server.py` file.

## CORS

CORS is configured to allow requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (React dev server)

To add more origins, update the `allow_origins` list in `main.py`.
