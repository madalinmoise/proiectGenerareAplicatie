@echo off
TITLE Enterprise Document Hub - Launcher
SETLOCAL EnableDelayedExpansion

echo ===================================================
echo   ENTERPRISE DOCUMENT HUB - SYSTEM INITIALIZATION
echo ===================================================
echo.

:: Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.9+ and add it to PATH.
    pause
    exit /b
)

:: Check for Virtual Environment
if not exist "venv" (
    echo [INFO] Creating Virtual Environment...
    python -m venv venv
)

:: Activate Virtual Environment and install requirements
echo [INFO] Updating dependencies...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [SUCCESS] Environment ready. Starting application...
echo.

:: Start the app
python main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application exited with code %errorlevel%
    pause
)

deactivate
