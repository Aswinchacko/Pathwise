#!/usr/bin/env python3
"""
Comprehensive script to run the recommendation service
"""

import os
import sys
import subprocess
import time
import requests
import json

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'pandas', 'numpy', 
        'scikit-learn', 'pydantic', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("💡 Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def check_dataset():
    """Check if dataset exists"""
    print("\n🔍 Checking dataset...")
    
    if os.path.exists('project_dataset.json'):
        print("✅ Dataset exists")
        return True
    else:
        print("❌ Dataset not found, generating...")
        try:
            from dataset_generator import save_dataset
            save_dataset()
            print("✅ Dataset generated successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to generate dataset: {e}")
            return False

def start_service():
    """Start the recommendation service"""
    print("\n🚀 Starting Recommendation Service...")
    print("📍 Service URL: http://localhost:8002")
    print("📖 API Docs: http://localhost:8002/docs")
    print("=" * 50)
    
    try:
        # Import and run the service
        from main import app
        import uvicorn
        
        print("✅ Service components loaded successfully")
        print("🔄 Starting server...")
        
        # Run the service
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8002,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Service stopped by user")
    except Exception as e:
        print(f"❌ Error starting service: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_service():
    """Test if the service is working"""
    print("\n🧪 Testing service...")
    
    # Wait for service to start
    time.sleep(3)
    
    try:
        response = requests.get("http://localhost:8002/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service is running! Status: {data['status']}")
            print(f"📊 Total projects: {data.get('total_projects', 'Unknown')}")
            return True
        else:
            print(f"❌ Service returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to service: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("🎯 PATHWISE RECOMMENDATION SERVICE")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check dataset
    if not check_dataset():
        sys.exit(1)
    
    # Test service components
    print("\n🔍 Testing service components...")
    try:
        from main import app
        print("✅ FastAPI app loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load FastAPI app: {e}")
        sys.exit(1)
    
    # Start the service
    print("\n🚀 Starting service...")
    print("💡 Press Ctrl+C to stop the service")
    print("=" * 60)
    
    start_service()

if __name__ == "__main__":
    main()
