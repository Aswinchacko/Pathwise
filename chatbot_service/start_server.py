#!/usr/bin/env python3
"""
PathWise Chatbot Service Startup Script
"""

import uvicorn
import sys
import os

def main():
    """Start the chatbot service"""
    print("🤖 Starting PathWise Chatbot Service...")
    print("📍 Service will be available at: http://localhost:8004")
    print("📚 API Documentation: http://localhost:8004/docs")
    print("🔍 Health Check: http://localhost:8004/health")
    print("\n" + "="*50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8004,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Chatbot service stopped.")
    except Exception as e:
        print(f"❌ Error starting service: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
