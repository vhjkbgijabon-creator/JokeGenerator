@echo off
REM ========================================
REM Joke Generator - Build to EXE
REM ========================================

chcp 65001 >nul
cls

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║           Joke Generator - EXE Builder                    ║
echo ║              ساخت فایل Joke Generator.exe                ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH
    echo [!] Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [✓] Python detected
echo.

REM Update pip
echo [*] Updating pip...
python -m pip install --upgrade pip -q

REM Install requirements
echo [*] Installing required packages...
pip install requests pyperclip pyinstaller -q

if %errorlevel% neq 0 (
    echo [!] Failed to install requirements
    pause
    exit /b 1
)

echo [✓] All packages installed
echo.

REM Build EXE
echo [*] Building Joke Generator.exe...
echo [*] This may take 2-3 minutes...
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --name="Joke Generator" ^
    --icon=NONE ^
    --add-data ".:" ^
    joke_generator.py

if %errorlevel% neq 0 (
    echo.
    echo [!] Build failed!
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                  BUILD SUCCESSFUL!                       ║
echo ║                                                          ║
echo ║  Your executable:                                       ║
echo ║  dist\Joke Generator.exe                                ║
echo ║                                                          ║
echo ║  Just double-click and start laughing! 😂               ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Open dist folder
explorer dist

pause
