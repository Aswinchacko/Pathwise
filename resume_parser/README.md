# Resume Parser API

A simple, professional FastAPI microservice for parsing resumes and extracting structured data.

## Features

- Extract contact information (name, email, phone, location)
- Parse work experience with job titles, companies, and descriptions
- Extract education history
- Identify skills and technologies
- Extract professional summary
- Support for text file uploads
- RESTful API with proper error handling
- CORS enabled for frontend integration

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8001`

## API Endpoints

### Health Check
- `GET /health` - Check service health

### Parse Resume
- `POST /parse` - Upload and parse a resume file (currently supports .txt files)
- `POST /parse-text` - Parse resume text directly

## Usage Examples

### Parse Text Directly
```bash
curl -X POST "http://localhost:8001/parse-text" \
  -H "Content-Type: application/json" \
  -d "John Doe\nSoftware Engineer\njohn.doe@email.com\n(555) 123-4567"
```

### Upload File
```bash
curl -X POST "http://localhost:8001/parse" \
  -F "file=@resume.txt"
```

## Response Format

```json
{
  "success": true,
  "data": {
    "name": "John Doe",
    "email": "john.doe@email.com",
    "phone": "(555) 123-4567",
    "location": "San Francisco, CA",
    "summary": "Experienced software engineer...",
    "experience": [
      {
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "dates": "2020 - Present",
        "description": "Led development of..."
      }
    ],
    "education": [
      {
        "degree": "Bachelor of Computer Science",
        "institution": "University of California",
        "dates": "2016 - 2020"
      }
    ],
    "skills": ["Python", "JavaScript", "React", "Node.js"],
    "languages": [],
    "certifications": [],
    "projects": [],
    "raw_text": "Full resume text..."
  }
}
```

## Future Enhancements

- Support for .doc, .docx, and .pdf files
- Enhanced parsing algorithms
- Machine learning-based extraction
- Database integration for storing parsed resumes
- Batch processing capabilities

