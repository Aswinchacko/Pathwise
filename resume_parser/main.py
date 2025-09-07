from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pathlib import Path
from parsers import extract_text, parse_resume
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Pathwise Resume Parser API",
    description="API for parsing resumes and extracting structured data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Resume Parser API is running"}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse a resume file (PDF or DOCX)
    Returns extracted profile data in structured format
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in ['.pdf', '.docx']:
            raise HTTPException(
                status_code=400, 
                detail="Only PDF and DOCX files are supported"
            )
        
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Processing file: {file.filename}")
        
        # Extract text from file
        try:
            text = extract_text(str(file_path))
            if not text.strip():
                raise HTTPException(status_code=400, detail="Could not extract text from file")
        except Exception as e:
            logger.error(f"Text extraction failed: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to extract text from file")
        
        # Parse resume data
        try:
            parsed_data = parse_resume(text)
            logger.info(f"Successfully parsed resume for: {parsed_data.get('full_name', 'Unknown')}")
        except Exception as e:
            logger.error(f"Resume parsing failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to parse resume data")
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except Exception as e:
            logger.warning(f"Failed to delete uploaded file: {str(e)}")
        
        return {
            "status": "success",
            "message": "Resume parsed successfully",
            "data": parsed_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
