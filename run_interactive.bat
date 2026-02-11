@echo off
REM Interactive DFS0 Analyzer - Windows Batch Launcher
REM This script launches the interactive analyzer on Windows systems

echo ========================================
echo DFS0 Interactive Analyzer Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found. Checking dependencies...
echo.

REM Check if required packages are installed
python -c "import mikeio" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting Interactive DFS0 Analyzer...
echo ========================================
echo.

REM Run the interactive analyzer
python interactive_analyzer.py

echo.
echo ========================================
echo Analysis session ended
echo ========================================
pause
