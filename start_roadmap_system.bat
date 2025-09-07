@echo off
echo ========================================
echo    PathWise Roadmap Generator System
echo ========================================
echo.

echo Starting FastAPI Server...
start "Roadmap API Server" cmd /k "cd roadmap_api && python main.py"

echo Waiting for server to start...
timeout /t 5 /nobreak >nul

echo Testing API...
cd roadmap_api
python test_frontend_integration.py

echo.
echo ========================================
echo API Server is running at: http://localhost:8000
echo Frontend should connect to this API
echo ========================================
echo.
echo Press any key to open the frontend...
pause >nul

echo Starting Frontend...
cd ..\dashboard
npm run dev
