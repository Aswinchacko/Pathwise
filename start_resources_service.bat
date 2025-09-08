@echo off
echo 🚀 Starting PathWise Resources Service...
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js is available

REM Navigate to resources service directory
cd /d "%~dp0resources_service"
if not exist "package.json" (
    echo ❌ Resources service not found in resources_service directory
    echo Please ensure you're running this from the PathWise root directory
    pause
    exit /b 1
)

echo ✅ Found resources service

REM Check if node_modules exists, if not install dependencies
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
) else (
    echo ✅ Dependencies already installed
)

REM Check for .env file
if not exist ".env" (
    if exist "env.example" (
        echo 📝 Creating .env file from env.example...
        copy "env.example" ".env" >nul
        echo ⚠️  Please configure your .env file with proper values
        echo Opening .env file for editing...
        start notepad ".env"
        echo Press any key after configuring .env file...
        pause >nul
    ) else (
        echo ❌ No .env or env.example file found
        echo Please create a .env file with your configuration
        pause
        exit /b 1
    )
)

echo ✅ Environment configuration found

REM Start the service
echo 🔍 Starting Resources Service with Web Scraping...
echo.
echo Service will be available at:
echo - Main API: http://localhost:8001/api/resources
echo - Scraping API: http://localhost:8001/api/scraping
echo - Health Check: http://localhost:8001/health
echo.
echo Press Ctrl+C to stop the service
echo.

npm start

if errorlevel 1 (
    echo.
    echo ❌ Service failed to start
    echo Check the error messages above for details
    pause
)
