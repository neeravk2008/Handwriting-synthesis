@echo off
title Handwriting Generator - Setup
color 0A

echo.
echo ========================================================
echo    HANDWRITING GENERATOR - AUTOMATIC SETUP
echo ========================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/2] Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/2] Generating handwriting database...
python setup.py
if errorlevel 1 (
    echo.
    echo ERROR: Setup failed
    pause
    exit /b 1
)

echo.
echo ========================================================
echo    SETUP COMPLETE!
echo ========================================================
echo.
echo You can now run the application by double-clicking:
echo    RUN_APP.bat
echo.
pause
