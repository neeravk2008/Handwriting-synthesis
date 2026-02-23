@echo off
title Handwriting Generator
color 0A

echo.
echo ========================================================
echo    HANDWRITING GENERATOR
echo ========================================================
echo.
echo Starting application...
echo.

python gui_app.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo.
    echo Please make sure you have run SETUP.bat first!
    echo.
    pause
)

exit
