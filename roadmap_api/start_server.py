#!/usr/bin/env python3
"""
Startup script for the Roadmap Generator API
"""
import os
import sys
import subprocess
import uvicorn

def check_csv_file():
    """Check if CSV file exists"""
    csv_path = "cross_domain_roadmaps_520.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found!")
        print("Please ensure the CSV file is in the same directory as this script.")
        return False
    return True

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    if not check_csv_file():
        return
    
    print("Starting Roadmap Generator API...")
    print("API will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    start_server()
