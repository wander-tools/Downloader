@echo off
title Fast Downloader Pro - Auto Setup
mode con: cols=80 lines=25
color 0A

echo ========================================
echo    Fast Downloader Pro - Auto Setup
echo ========================================
echo.

:: Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo 🔗 Please install Python from https://python.org
    echo 📁 After installation, run this file again
    pause
    exit /b 1
)

echo ✅ Python is installed

:: Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo 📋 Python Version: %python_version%

:: Create virtual environment
echo [2/5] Creating virtual environment...
python -m venv downloader_env
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment created

:: Activate virtual environment and install requirements
echo [3/5] Installing required packages...
call downloader_env\Scripts\activate.bat
pip install --upgrade pip >nul 2>&1
pip install requests >nul 2>&1

if %errorlevel% neq 0 (
    echo ❌ Failed to install required packages
    pause
    exit /b 1
)
echo ✅ Packages installed successfully

:: Run the installer
echo [4/5] Running application setup...
python install.py
if %errorlevel% neq 0 (
    echo ❌ Setup failed
    pause
    exit /b 1
)

:: Launch the application
echo [5/5] Launching Fast Downloader Pro...
echo.
echo 🚀 Application is starting...
echo ⚡ Terminal will minimize automatically...
echo.

:: Wait a moment before minimizing
timeout /t 3 /nobreak >nul

:: Minimize the current window
powershell -window minimized -command ""

:: Run the application
python fast_downloader.py

:: When application closes, show message
echo.
echo ========================================
echo    Fast Downloader Pro - Session Ended
echo ========================================
echo.
echo ℹ️  Application closed.
echo 🔄 To run again, double-click this file.
echo.
timeout /t 5
exit