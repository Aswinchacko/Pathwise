@echo off
echo Starting Recommendation Service on port 8002...
cd /d "%~dp0"
python -c "from main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8002)"
pause

