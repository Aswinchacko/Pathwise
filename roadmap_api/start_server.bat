@echo off
echo Starting Roadmap Generator API...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install requirements
echo Installing requirements...
python -m pip install -r requirements.txt

REM Start the server
echo.
echo Starting server...
python start_server.py

pause
