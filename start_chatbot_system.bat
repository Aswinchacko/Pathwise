@echo off
echo 🤖 Starting PathWise Chatbot System...
echo ==========================================
echo.

echo 📦 Installing Python dependencies...
cd chatbot_service
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🚀 Starting Chatbot Service...
echo 📍 Service will be available at: http://localhost:8004
echo 📚 API Documentation: http://localhost:8004/docs
echo 🔍 Health Check: http://localhost:8004/health
echo.

start "Chatbot Service" python start_server.py

echo.
echo ⏳ Waiting for service to start...
timeout /t 5 /nobreak > nul

echo.
echo 🧪 Running integration test...
python test_integration.py

echo.
echo ✅ Chatbot system is ready!
echo 🌐 Open your dashboard and navigate to the Chatbot page
echo.

pause
