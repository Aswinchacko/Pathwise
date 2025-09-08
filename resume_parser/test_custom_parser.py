from main import parse_aswin_resume

# Read the test file
with open('test_aswin_resume.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Test the custom parser
result = parse_aswin_resume(text)

print("Custom Parser Result:")
print(f"Name: {result.name}")
print(f"Email: {result.email}")
print(f"Phone: {result.phone}")
print(f"Location: {result.location}")
print(f"Summary: {result.summary[:100]}..." if result.summary else "Summary: None")
print(f"Skills: {result.skills[:5]}...")  # First 5 skills
print(f"Experience: {len(result.experience)} entries")
print(f"Education: {len(result.education)} entries")
print(f"Projects: {len(result.projects)} entries")
print(f"Certifications: {len(result.certifications)} entries")

