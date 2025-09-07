#!/usr/bin/env python3
"""
Migrate title field to existing MongoDB documents
"""
from pymongo import MongoClient

def migrate_title_field():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['pathwise']
    collection = db['roadmap']

    print('=== MIGRATING TITLE FIELD ===')
    
    # Get all documents without title field
    docs_without_title = list(collection.find({'title': {'$exists': False}}))
    print(f'Found {len(docs_without_title)} documents without title field')

    if docs_without_title:
        print('Adding title field to all documents...')
        updated_count = 0
        for doc in docs_without_title:
            result = collection.update_one(
                {'_id': doc['_id']},
                {'$set': {'title': doc['goal']}}
            )
            if result.modified_count > 0:
                updated_count += 1
        print(f'Migration completed! Updated {updated_count} documents')
    else:
        print('All documents already have title field!')

    # Verify
    print('\n=== VERIFICATION ===')
    with_title = collection.count_documents({'title': {'$exists': True}})
    without_title = collection.count_documents({'title': {'$exists': False}})
    print(f'Documents WITH title field: {with_title}')
    print(f'Documents WITHOUT title field: {without_title}')

    # Show sample with title
    sample = collection.find_one({'title': {'$exists': True}})
    if sample:
        print(f'\nSample document with title:')
        print(f'  title: {sample.get("title", "NOT FOUND")}')
        print(f'  goal: {sample.get("goal", "NOT FOUND")}')
        print(f'  source: {sample.get("source", "NOT FOUND")}')

if __name__ == "__main__":
    migrate_title_field()
