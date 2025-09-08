import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def test_direct_mongodb_storage():
    """Test storing resume data directly in MongoDB"""
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    
    try:
        print("Connecting to MongoDB...")
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client.pathwise
        collection = db.resume
        
        # Test data
        test_resume = {
            "user_id": "test_user_123",
            "parsed_data": {
                "name": "John Smith",
                "email": "john.smith@email.com",
                "phone": "(555) 123-4567",
                "location": "San Francisco, CA",
                "summary": "Experienced software engineer",
                "experience": [
                    {
                        "title": "Senior Software Engineer",
                        "company": "Tech Corp",
                        "dates": "2020 - Present",
                        "description": "Led development of microservices"
                    }
                ],
                "education": [
                    {
                        "degree": "Bachelor of Computer Science",
                        "institution": "University of California",
                        "dates": "2014 - 2018"
                    }
                ],
                "skills": ["Python", "JavaScript", "React", "Node.js"],
                "languages": [],
                "certifications": [],
                "projects": [],
                "raw_text": "Test resume content"
            },
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "file_name": "test_resume.txt",
            "file_type": "text/plain"
        }
        
        print("Inserting test resume...")
        result = await collection.insert_one(test_resume)
        print(f"✅ Resume inserted with ID: {result.inserted_id}")
        
        # Verify insertion
        print("Verifying insertion...")
        count = await collection.count_documents({})
        print(f"Total documents in collection: {count}")
        
        # Get the inserted document
        doc = await collection.find_one({"_id": result.inserted_id})
        if doc:
            print(f"✅ Document found: {doc['parsed_data']['name']}")
            print(f"   Email: {doc['parsed_data']['email']}")
            print(f"   Skills: {doc['parsed_data']['skills']}")
        else:
            print("❌ Document not found")
        
        # Test query by user_id
        user_resumes = await collection.find({"user_id": "test_user_123"}).to_list(length=None)
        print(f"✅ Found {len(user_resumes)} resumes for user test_user_123")
        
        # Clean up
        await collection.delete_one({"_id": result.inserted_id})
        print("✅ Test document cleaned up")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_direct_mongodb_storage())
