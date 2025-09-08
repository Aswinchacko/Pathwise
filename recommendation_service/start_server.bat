@echo off
echo Starting Recommendation Service...
cd /d "%~dp0"
python start_server.py
pause

