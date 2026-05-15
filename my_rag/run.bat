@echo off
echo ========================================
echo   RAG System Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [2/4] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
) else (
    echo [2/4] Virtual environment already exists.
    echo.
)

REM Activate virtual environment
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing/updating dependencies...
echo This may take a few minutes on first run...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo.
    echo Common solutions:
    echo   1. Check your internet connection
    echo   2. Try upgrading pip: python -m pip install --upgrade pip
    echo   3. Install dependencies one by one to find the problematic package
    echo.
    echo Press any key to see detailed error and exit...
    pause
    exit /b 1
)
echo.
echo Dependencies installed successfully!
echo.

REM Check if Ollama is running
echo [4/4] Checking Ollama status...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARNING] Ollama is not running!
    echo.
    echo Please start Ollama in another terminal:
    echo   1. Open a new terminal
    echo   2. Run: ollama serve
    echo   3. Pull model: ollama pull llama3.1:8b
    echo.
    echo Press any key to continue anyway (UI will show errors)...
    pause >nul
) else (
    echo Ollama is running!
    echo.
)

REM Launch Streamlit app
echo ========================================
echo   Launching RAG System Web UI...
echo ========================================
echo.
echo The app will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py

REM Deactivate virtual environment on exit
deactivate
