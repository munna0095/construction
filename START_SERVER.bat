@echo off
REM ============================================
REM SIDDHI CONSTRUCTION WEBSITE - START SERVER
REM ============================================
REM This script starts a local web server
REM Opens the website in your default browser

echo.
echo   ⚙️  SIDDHI CONSTRUCTION WEBSITE
echo   ════════════════════════════════════════
echo.
echo   Starting local server...
echo   Opening: http://localhost:8000
echo.
echo   Press Ctrl+C to stop the server
echo.
echo   ════════════════════════════════════════
echo.

REM Change to the correct directory
cd /d "%~dp0"

REM Start Python HTTP server
python -m http.server 8000

REM If Python not found, try python3
if %errorlevel% neq 0 (
    echo Trying python3...
    python3 -m http.server 8000
)

REM If both fail
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python not found!
    echo Please install Python from: https://www.python.org
    echo.
    pause
)
