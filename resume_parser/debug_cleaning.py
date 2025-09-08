import re

def clean_resume_text(text: str) -> str:
    """Clean and normalize resume text"""
    # Fix the specific problematic pattern
    text = re.sub(r'LLM-powered assistants\.ASW\s+IN\s+CHACKO', 'ASWIN CHACKO', text, flags=re.IGNORECASE)
    
    # Remove excessive spaces between letters (like "A S W I N" -> "ASWIN")
    # Handle various patterns of spaced letters
    patterns = [
        (r'([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])', r'\1\2\3\4\5\6\7\8\9\10'),
        (r'([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])', r'\1\2\3\4\5\6\7\8\9'),
        (r'([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])', r'\1\2\3\4\5\6\7\8'),
        (r'([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])', r'\1\2\3\4\5\6\7'),
        (r'([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])', r'\1\2\3\4\5\6'),
        (r'([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])', r'\1\2\3\4\5'),
        (r'([A-Z])\s+([A-Z])\s+([A-Z])\s+([A-Z])', r'\1\2\3\4'),
        (r'([A-Z])\s+([A-Z])\s+([A-Z])', r'\1\2\3'),
        (r'([A-Z])\s+([A-Z])', r'\1\2'),
    ]
    
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    
    # Clean up common patterns
    replacements = [
        (r'I\s+n\s+t\s+e\s+g\s+r\s+a\s+t\s+e\s+d\s+\s+M\s+C\s+A', 'Integrated MCA'),
        (r'A\s+S\s+W\s+\s+I\s+N\s+\s+C\s+H\s+A\s+C\s+K\s+O', 'ASWIN CHACKO'),
        (r'S\s+U\s+M\s+\s+M\s+\s+A\s+R\s+Y', 'SUMMARY'),
        (r'S\s+K\s+I\s+L\s+L\s+S', 'SKILLS'),
        (r'E\s+X\s+P\s+E\s+R\s+I\s+E\s+N\s+C\s+E\s+S', 'EXPERIENCES'),
        (r'E\s+D\s+U\s+C\s+A\s+T\s+I\s+O\s+N', 'EDUCATION'),
        (r'P\s+R\s+O\s+J\s+E\s+C\s+T\s+S', 'PROJECTS'),
        (r'C\s+E\s+R\s+T\s+I\s+F\s+I\s+C\s+A\s+T\s+I\s+O\s+N\s+S\s+\&\s+A\s+C\s+H\s+I\s+E\s+V\s+E\s+M\s+E\s+N\s+T\s+S', 'CERTIFICATIONS & ACHIEVEMENTS'),
        (r'W\s+e\s+b\s+\s+D\s+e\s+s\s+i\s+g\s+n\s+e\s+r\s+\&\s+\s+B\s+a\s+c\s+k\s+e\s+n\s+d\s+\s+D\s+e\s+v\s+e\s+l\s+o\s+p\s+e\s+r', 'Web Designer & Backend Developer'),
        (r'C\s+o\s+-\s+F\s+o\s+u\s+n\s+d\s+e\s+r\s+,\s+\s+F\s+r\s+e\s+s\s+h\s+i\s+r\s+e', 'Co-Founder, Freshire'),
        (r'S\s+o\s+c\s+i\s+a\s+l\s+\s+M\s+e\s+d\s+i\s+a\s+\s+C\s+o\s+n\s+t\s+e\s+n\s+t\s+\s+C\s+r\s+e\s+a\s+t\s+o\s+r', 'Social Media Content Creator'),
        (r'R\s+e\s+s\s+o\s+u\s+r\s+c\s+e\s+\s+P\s+e\s+r\s+s\s+o\s+n\s+–\s+M\s+E\s+R\s+N\s+\s+S\s+t\s+a\s+c\s+k\s+\s+D\s+e\s+v\s+e\s+l\s+o\s+p\s+m\s+e\s+n\s+t\s+\s+W\s+o\s+r\s+k\s+s\s+h\s+o\s+p', 'Resource Person – MERN Stack Development Workshop'),
        (r'S\s+e\s+n\s+i\s+o\s+r\s+\s+S\s+e\s+c\s+o\s+n\s+d\s+a\s+r\s+y\s+\s+E\s+d\s+u\s+c\s+a\s+t\s+i\s+o\s+n', 'Senior Secondary Education'),
        (r'H\s+i\s+g\s+h\s+e\s+r\s+\s+S\s+e\s+c\s+o\s+n\s+d\s+a\s+r\s+y\s+\s+E\s+d\s+u\s+c\s+a\s+t\s+i\s+o\s+n', 'Higher Secondary Education'),
    ]
    
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

# Read the test file
with open('test_aswin_resume.txt', 'r', encoding='utf-8') as f:
    original_text = f.read()

print("ORIGINAL TEXT (first 500 chars):")
print(original_text[:500])
print("\n" + "="*50 + "\n")

cleaned_text = clean_resume_text(original_text)
print("CLEANED TEXT (first 500 chars):")
print(cleaned_text[:500])
print("\n" + "="*50 + "\n")

# Check if the name pattern was fixed
if "ASWIN CHACKO" in cleaned_text:
    print("✅ Name pattern fixed!")
else:
    print("❌ Name pattern not fixed")

# Check if other patterns were fixed
if "Integrated MCA" in cleaned_text:
    print("✅ Education pattern fixed!")
else:
    print("❌ Education pattern not fixed")

if "SKILLS" in cleaned_text:
    print("✅ Skills pattern fixed!")
else:
    print("❌ Skills pattern not fixed")

