#!/usr/bin/env python3
"""
Check MongoDB data structure
"""
from pymongo import MongoClient

def check_mongodb_data():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['pathwise']
    collection = db['roadmap']

    print('=== CHECKING MONGODB DATA STRUCTURE ===')

    # Check the specific documents you mentioned
    react_docs = list(collection.find({'goal': {'$regex': 'React Developer'}}).limit(3))
    print(f'Found {len(react_docs)} React Developer documents')

    for i, doc in enumerate(react_docs):
        print(f'\n--- Document {i+1} ---')
        print(f'ID: {doc["_id"]}')
        print(f'CSV ID: {doc.get("csv_id", "N/A")}')
        print(f'Title: {doc.get("title", "NOT FOUND")}')
        print(f'Goal: {doc.get("goal", "NOT FOUND")}')
        print(f'Domain: {doc.get("domain", "NOT FOUND")}')
        print(f'Source: {doc.get("source", "NOT FOUND")}')
        print(f'Steps: {len(doc.get("steps", []))} categories')
        print(f'Created: {doc.get("created_at", "NOT FOUND")}')

    # Check for any missing fields
    print('\n=== CHECKING FOR MISSING FIELDS ===')
    missing_title = collection.count_documents({'title': {'$exists': False}})
    missing_goal = collection.count_documents({'goal': {'$exists': False}})
    missing_domain = collection.count_documents({'domain': {'$exists': False}})
    missing_steps = collection.count_documents({'steps': {'$exists': False}})

    print(f'Documents missing title: {missing_title}')
    print(f'Documents missing goal: {missing_goal}')
    print(f'Documents missing domain: {missing_domain}')
    print(f'Documents missing steps: {missing_steps}')

    if missing_title == 0 and missing_goal == 0 and missing_domain == 0 and missing_steps == 0:
        print('✅ All required fields are present!')
    else:
        print('❌ Some fields are missing!')

    # Check total counts
    print('\n=== COLLECTION STATISTICS ===')
    total_docs = collection.count_documents({})
    csv_docs = collection.count_documents({'source': 'csv_import'})
    user_docs = collection.count_documents({'source': 'user_generated'})
    
    print(f'Total documents: {total_docs}')
    print(f'CSV imported: {csv_docs}')
    print(f'User generated: {user_docs}')

if __name__ == "__main__":
    check_mongodb_data()
