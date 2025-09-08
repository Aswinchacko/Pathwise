#!/usr/bin/env python3
"""
Simple startup script for the recommendation service
"""

import uvicorn
import sys
import os
from main import app

def start_service():
    """Start the recommendation service"""
    print("🚀 Starting Recommendation Service...")
    print("📍 Service will run on: http://localhost:8002")
    print("📖 API Documentation: http://localhost:8002/docs")
    print("🔧 Alternative Docs: http://localhost:8002/redoc")
    print("=" * 50)
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8002,
            log_level="info",
            reload=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Service stopped by user")
    except Exception as e:
        print(f"❌ Error starting service: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_service()
