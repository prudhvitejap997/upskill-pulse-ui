@echo off
echo.
echo  ==============================
echo   Upskill Pulse - Local Server
echo  ==============================
echo.

if "%GROQ_API_KEY%"=="" (
    set /p GROQ_API_KEY=Paste your Groq API key (or press Enter to use offline mode):
    echo.
)

echo Installing dependencies...
pip install -r requirements.txt -q
echo.
echo Starting Upskill Pulse...
echo Open your browser at: http://localhost:3000
echo Press Ctrl+C to stop the server.
echo.

python server.py
pause
