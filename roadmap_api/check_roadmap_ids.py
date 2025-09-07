#!/usr/bin/env python3
"""
Check roadmap IDs in database
"""
from pymongo import MongoClient

def check_roadmap_ids():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['pathwise']
    collection = db['roadmap']

    # Get user roadmaps
    user_roadmaps = list(collection.find({'user_id': 'test_user_123', 'source': 'user_generated'}))

    print('User roadmaps in database:')
    for roadmap in user_roadmaps:
        print(f'  _id: {roadmap["_id"]}')
        print(f'  roadmap_id: {roadmap.get("roadmap_id", "NOT FOUND")}')
        print(f'  goal: {roadmap["goal"]}')
        print(f'  user_id: {roadmap["user_id"]}')
        print('  ---')

if __name__ == "__main__":
    check_roadmap_ids()
