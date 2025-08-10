from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path
from parsers import extract_text, parse_resume

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Pathwise Resume Parser API")

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(str(file_path))
    parsed_data = parse_resume(text)
    return {"status": "success", "profile_data": parsed_data}
