#!/usr/bin/env python3
"""
Debug script to test the recommendation service components
"""

import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import json
        print("✓ json imported")
    except Exception as e:
        print(f"✗ json import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ pandas imported")
    except Exception as e:
        print(f"✗ pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy imported")
    except Exception as e:
        print(f"✗ numpy import failed: {e}")
        return False
    
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        print("✓ scikit-learn imported")
    except Exception as e:
        print(f"✗ scikit-learn import failed: {e}")
        return False
    
    try:
        from fastapi import FastAPI
        print("✓ fastapi imported")
    except Exception as e:
        print(f"✗ fastapi import failed: {e}")
        return False
    
    return True

def test_dataset_generation():
    """Test dataset generation"""
    print("\nTesting dataset generation...")
    
    try:
        from dataset_generator import generate_project_dataset
        projects = generate_project_dataset()
        print(f"✓ Generated {len(projects)} projects")
        
        # Save dataset
        import json
        with open('project_dataset.json', 'w', encoding='utf-8') as f:
            json.dump(projects, f, indent=2, ensure_ascii=False)
        print("✓ Dataset saved to project_dataset.json")
        return True
        
    except Exception as e:
        print(f"✗ Dataset generation failed: {e}")
        traceback.print_exc()
        return False

def test_ml_models():
    """Test ML models initialization"""
    print("\nTesting ML models...")
    
    try:
        from ml_models import ProjectRecommendationEngine
        engine = ProjectRecommendationEngine()
        print("✓ Recommendation engine initialized")
        return True
        
    except Exception as e:
        print(f"✗ ML models failed: {e}")
        traceback.print_exc()
        return False

def test_fastapi_app():
    """Test FastAPI app initialization"""
    print("\nTesting FastAPI app...")
    
    try:
        from main import app
        print("✓ FastAPI app imported")
        return True
        
    except Exception as e:
        print(f"✗ FastAPI app failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("RECOMMENDATION SERVICE DEBUG TEST")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_dataset_generation,
        test_ml_models,
        test_fastapi_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"Test {test.__name__} failed with exception: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All tests passed! Service should work.")
    else:
        print("❌ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
