@echo off
echo ========================================
echo Tech Skills Demand Checker
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python first.
    pause
    exit /b
)

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Select mode:
echo 1. Command Line Version
echo 2. Web Application
echo ========================================
echo.

set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Starting Command Line Version...
    python tech_skills_scraper.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Web Application...
    echo Open browser and go to: http://localhost:5000
    python app.py
) else (
    echo Invalid choice!
    pause
    exit /b
)

pause
