@echo off
REM ==========================================================
REM  Python Terminal - Persian beginner course launcher
REM  NOTE: keep this file ASCII-only. cmd.exe cannot read
REM  Persian text from a .bat file reliably. The Persian
REM  welcome message is printed by app.py itself.
REM ==========================================================
chcp 65001 >nul 2>&1
title Python Terminal - Persian Course
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
    echo.
    echo   [ERROR] Python was not found on your PATH.
    echo.
    echo   Please install Python 3.11+ from python.org
    echo   and make sure to tick "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

echo.
echo   Starting Python Terminal...
echo   If your browser does not open automatically,
echo   go to:  http://127.0.0.1:8765/
echo.

python app.py

if errorlevel 1 (
    echo.
    echo   [ERROR] The program stopped with an error. Read the message above.
    pause
)
