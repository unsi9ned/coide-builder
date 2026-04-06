@echo off
title CoIDE Environment Setup

echo ========================================
echo   CoIDE Environment Setup
echo ========================================
echo.

:: Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.7+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Установка зависимостей
echo Installing Python dependencies...
pip install -r requirements.txt

:: Запуск основного скрипта
python setup.py

pause