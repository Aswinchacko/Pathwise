import re
import spacy
import fitz
import docx
from collections import OrderedDict

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Section keyword mappings
SECTION_HEADERS = {
    "summary": ["summary", "profile", "career objective", "objective", "about me", "professional profile"],
    "skills": ["skills", "technical skills", "core competencies", "areas of expertise"],
    "experience": ["experience", "work experience", "professional experience", "employment history", "internships"],
    "education": ["education", "academic background", "academic qualifications"]
}

ROLE_KEYWORDS = ["engineer", "developer", "intern", "manager", "consultant", "analyst", "specialist"]
DEGREE_KEYWORDS = ["btech", "b.tech", "mtech", "m.tech", "mca", "bca", "bachelor", "master", "msc", "bsc", "phd", "b.e", "m.e"]

def extract_text(file_path: str):
    """Extracts text from PDF or DOCX"""
    if file_path.lower().endswith(".pdf"):
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text("text") + "\n"
        return text
    elif file_path.lower().endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def find_section(line: str):
    """Finds which section a line belongs to"""
    line_clean = re.sub(r'[^a-zA-Z\s]', '', line).strip().lower()
    for section, keywords in SECTION_HEADERS.items():
        for kw in keywords:
            if kw in line_clean:
                return section
    return None

def split_sections(text: str):
    """Splits resume into sections"""
    sections = OrderedDict()
    current_section = "preamble"
    sections[current_section] = []

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        sec = find_section(line)
        if sec:
            current_section = sec
            sections[current_section] = []
            continue
        sections[current_section].append(line)

    for sec in sections:
        sections[sec] = "\n".join(sections[sec]).strip()

    return sections

def extract_name(text: str):
    """Finds candidate name from top lines"""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    top_chunk = "\n".join(lines[:8])
    doc = nlp(top_chunk)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not any(rk in ent.text.lower() for rk in ROLE_KEYWORDS):
            return ent.text.strip()
    for l in lines:
        if l.isupper() or l.istitle():
            return l
    return None

def clean_skills(skills_text: str):
    """Cleans skill list from extra text"""
    tokens = re.split(r'[,\n•]', skills_text)
    cleaned = []
    for t in tokens:
        t = re.sub(r'\(.*?\)', '', t).strip()
        if t and len(t.split()) <= 4:
            cleaned.append(t)
    return list(dict.fromkeys(cleaned))

def parse_education_block(text: str):
    """Parses education section into structured list"""
    entries = []
    for block in re.split(r'\n{2,}', text):
        block = block.strip()
        if not block:
            continue
        degree = None
        for d in DEGREE_KEYWORDS:
            if d in block.lower():
                degree = re.search(d, block, re.IGNORECASE).group()
                break
        years = re.findall(r'(?:19|20)\d{2}', block)
        inst = None
        doc = nlp(block)
        for ent in doc.ents:
            if ent.label_ == "ORG":
                inst = ent.text
                break
        entries.append({
            "degree": degree,
            "institution": inst,
            "year_start": years[0] if years else None,
            "year_end": years[-1] if years else None
        })
    return entries

def parse_experience_block(text: str):
    """Parses experience section into structured list"""
    entries = []
    for block in re.split(r'\n{2,}', text):
        block = block.strip()
        if not block:
            continue
        years = re.findall(r'(?:19|20)\d{2}', block)
        role = block.split("\n")[0] if block else None
        company = None
        doc = nlp(block)
        for ent in doc.ents:
            if ent.label_ == "ORG":
                company = ent.text
                break
        entries.append({
            "role": role,
            "company": company,
            "year_start": years[0] if years else None,
            "year_end": years[-1] if years else None
        })
    return entries

def parse_resume(text: str):
    """Parses resume into Pathwise profile format"""
    sections = split_sections(text)
    name = extract_name(text)
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.search(r'\+?\d[\d\s-]{8,}\d', text)
    location = None
    linkedin = None
    github = None

    if match := re.search(r'linkedin\.com/[^\s,]+', text, re.IGNORECASE):
        linkedin = match.group().strip()
    if match := re.search(r'github\.com/[^\s,]+', text, re.IGNORECASE):
        github = match.group().strip()
    if match := re.search(r'\b[A-Za-z\s]+,\s*[A-Za-z\s]+$', text.split("\n")[0]):
        location = match.group().strip()

    parsed = {
        "full_name": name,
        "email": email.group() if email else None,
        "phone": phone.group() if phone else None,
        "location": location,
        "summary": sections.get("summary") or " ".join(sections.get("preamble", "").split()[:50]),
        "skills": clean_skills(sections.get("skills", "")),
        "education": parse_education_block(sections.get("education", "")),
        "experience": parse_experience_block(sections.get("experience", "")),
        "linkedin": linkedin,
        "github": github
    }
    return parsed
