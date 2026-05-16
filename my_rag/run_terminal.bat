@echo off
echo ========================================
echo   RAG Terminal Mode
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/4] Activating virtual environment...
if not exist "venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup_py314.bat or run.bat first.
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo.

echo [2/4] Checking Ollama status...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARNING] Ollama is not running!
    echo Please start Ollama in another terminal:
    echo   ollama serve
    echo.
    echo Press any key to continue anyway...
    pause >nul
) else (
    echo Ollama is running!
)
echo.

echo [3/4] Starting Terminal RAG...
echo.
echo ========================================
echo   Terminal Mode Active
echo ========================================
echo.
echo Type your questions or use slash commands
echo Type /help for available commands
echo Press Ctrl+C to interrupt, Ctrl+D to exit
echo.

python terminal.py

echo.
echo [4/4] Cleaning up...
deactivate
