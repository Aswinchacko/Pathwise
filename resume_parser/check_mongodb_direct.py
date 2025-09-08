import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def check_mongodb_resumes():
    """Check if resumes are stored in MongoDB"""
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    
    try:
        print(f"Connecting to MongoDB: {MONGODB_URL}")
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client.pathwise
        collection = db.resume
        
        # Count total documents
        total_count = await collection.count_documents({})
        print(f"Total documents in 'resume' collection: {total_count}")
        
        if total_count > 0:
            print("\nRecent resumes:")
            # Get recent documents
            cursor = collection.find({}).sort("created_at", -1).limit(5)
            async for doc in cursor:
                print(f"  - {doc['parsed_data']['name']} ({doc['file_name']})")
                print(f"    User ID: {doc.get('user_id', 'None')}")
                print(f"    Created: {doc['created_at']}")
                print(f"    Skills: {len(doc['parsed_data']['skills'])} skills")
                print()
        else:
            print("No resumes found in the collection")
        
        # Check for test user resumes
        test_user_count = await collection.count_documents({"user_id": "test_user_123"})
        print(f"Resumes for test_user_123: {test_user_count}")
        
        client.close()
        return total_count > 0
        
    except Exception as e:
        print(f"❌ Error checking MongoDB: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(check_mongodb_resumes())
