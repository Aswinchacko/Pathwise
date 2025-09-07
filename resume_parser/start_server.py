#!/usr/bin/env python3
"""
Startup script for the Resume Parser FastAPI server
"""

import uvicorn
import sys
import os
from pathlib import Path

def main():
    # Add the current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    # Check if spacy model is installed
    try:
        import spacy
        spacy.load("en_core_web_sm")
        print("✓ Spacy model 'en_core_web_sm' is available")
    except OSError:
        print("❌ Spacy model 'en_core_web_sm' not found!")
        print("Please install it by running: python -m spacy download en_core_web_sm")
        sys.exit(1)
    
    # Start the server
    print("🚀 Starting Resume Parser API server...")
    print("📝 API Documentation: http://localhost:8000/docs")
    print("🔗 Health Check: http://localhost:8000/health")
    print("📤 Upload Endpoint: http://localhost:8000/upload-resume")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
