@echo off
title LinkedIn Post Generator Launcher
color 0A

echo ========================================
echo    LINKEDIN POST GENERATOR
echo ========================================
echo.
echo [1/3] Starting Backend Server...
cd backend
start "Backend Server" cmd /k "python app.py"
cd ..

echo [2/3] Waiting for backend to initialize...
timeout /t 3 /nobreak > nul

echo [3/3] Opening Frontend...
cd frontend
start "" "index.html"
cd ..

echo.
echo ========================================
echo ✅ SYSTEM READY!
echo ========================================
echo 📍 Backend: http://localhost:5000
echo 📍 Frontend: Open in your browser
echo.
echo Press any key to exit this window...
pause > nul