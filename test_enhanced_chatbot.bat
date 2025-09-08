@echo off
echo 🚀 Testing Enhanced PathWise Chatbot with Roadmap Integration
echo ============================================================
echo.

echo 📋 Prerequisites Check:
echo - MongoDB should be running on localhost:27017
echo - Roadmap API should be running on localhost:8000
echo - Chatbot Service should be running on localhost:8004
echo.

echo 🧪 Running Integration Tests...
echo.

cd chatbot_service
python test_roadmap_integration.py

echo.
echo ✅ Test completed! Check the results above.
echo.
echo 💡 To test manually:
echo 1. Open http://localhost:5173 in your browser
echo 2. Navigate to the Chatbot page
echo 3. Try: "Create a roadmap for becoming a Python developer"
echo 4. Click on the roadmap preview to see full details
echo.

pause

