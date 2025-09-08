"""
Start script for the Recommendation Service
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def generate_dataset():
    """Generate the project dataset if it doesn't exist"""
    if not os.path.exists("project_dataset.json"):
        print("Generating project dataset...")
        from dataset_generator import save_dataset
        save_dataset()
    else:
        print("Dataset already exists")

def start_server():
    """Start the FastAPI server"""
    print("Starting Recommendation Service...")
    subprocess.run([sys.executable, "main.py"])

if __name__ == "__main__":
    try:
        # Install requirements
        install_requirements()
        
        # Generate dataset
        generate_dataset()
        
        # Start server
        start_server()
        
    except KeyboardInterrupt:
        print("\nShutting down Recommendation Service...")
    except Exception as e:
        print(f"Error starting service: {e}")
        sys.exit(1)

