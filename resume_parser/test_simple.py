#!/usr/bin/env python3
"""
Simple test to verify resume parsing works
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_parsing():
    """Test resume parsing without server"""
    try:
        from parsers import extract_text, parse_resume
        
        # Test with existing resume file
        test_file = "uploads/Aswin Chacko - Software Engineer .pdf"
        
        if not os.path.exists(test_file):
            print(f"❌ Test file not found: {test_file}")
            print("Available files in uploads:")
            uploads_dir = Path("uploads")
            if uploads_dir.exists():
                for file in uploads_dir.iterdir():
                    print(f"  - {file.name}")
            return False
        
        print(f"📄 Testing with file: {test_file}")
        
        # Extract text
        print("🔍 Extracting text...")
        text = extract_text(test_file)
        print(f"✅ Extracted {len(text)} characters")
        
        # Parse resume
        print("🧠 Parsing resume...")
        parsed_data = parse_resume(text)
        
        print("✅ Parsing successful!")
        print(f"📝 Name: {parsed_data.get('full_name', 'Not found')}")
        print(f"📧 Email: {parsed_data.get('email', 'Not found')}")
        print(f"📱 Phone: {parsed_data.get('phone', 'Not found')}")
        print(f"🎯 Skills: {len(parsed_data.get('skills', []))} found")
        print(f"💼 Experience: {len(parsed_data.get('experience', []))} entries")
        print(f"🎓 Education: {len(parsed_data.get('education', []))} entries")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Resume Parser")
    print("=" * 40)
    
    if test_parsing():
        print("\n✅ Resume parsing works! The issue is with the server.")
        print("💡 Next step: Start the server manually")
    else:
        print("\n❌ Resume parsing failed. Check the error above.")
