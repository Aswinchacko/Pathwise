import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def test_mongodb_connection():
    """Test MongoDB connection"""
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    
    try:
        print(f"Testing MongoDB connection to: {MONGODB_URL}")
        
        client = AsyncIOMotorClient(MONGODB_URL)
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Test database and collection
        db = client.pathwise
        collection = db.resume
        
        # Test collection operations
        count = await collection.count_documents({})
        print(f"✅ Collection 'resume' accessible. Document count: {count}")
        
        # Test insert
        test_doc = {
            "test": True,
            "message": "MongoDB connection test"
        }
        
        result = await collection.insert_one(test_doc)
        print(f"✅ Test document inserted with ID: {result.inserted_id}")
        
        # Clean up test document
        await collection.delete_one({"_id": result.inserted_id})
        print("✅ Test document cleaned up")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_mongodb_connection())
