@echo off
echo ========================================
echo Running Soccer Analysis
echo ========================================
echo.

python soccer_analysis.py

if errorlevel 1 (
    echo.
    echo ERROR: Script failed to run
    echo Make sure you have run setup.bat first
    pause
    exit /b 1
)

echo.
pause
