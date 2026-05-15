@echo off
echo ========================================
echo   RAG System - Dependency Troubleshooter
echo ========================================
echo.

echo [Step 1] Checking Python version...
python --version
echo.

echo [Step 2] Checking pip version...
python -m pip --version
echo.

echo [Step 3] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [Step 4] Installing dependencies one by one...
echo This will help identify which package is causing issues.
echo.

call venv\Scripts\activate.bat 2>nul
if errorlevel 1 (
    echo Creating virtual environment first...
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo Installing sentence-transformers...
pip install sentence-transformers==2.2.2
if errorlevel 1 (
    echo [ERROR] Failed to install sentence-transformers
    echo This package requires: torch, transformers, numpy
    pause
    exit /b 1
)

echo Installing chromadb...
pip install chromadb==0.4.22
if errorlevel 1 (
    echo [ERROR] Failed to install chromadb
    pause
    exit /b 1
)

echo Installing ollama...
pip install ollama==0.1.6
if errorlevel 1 (
    echo [ERROR] Failed to install ollama
    pause
    exit /b 1
)

echo Installing streamlit...
pip install streamlit==1.31.0
if errorlevel 1 (
    echo [ERROR] Failed to install streamlit
    pause
    exit /b 1
)

echo Installing pypdf...
pip install pypdf==4.0.1
if errorlevel 1 (
    echo [ERROR] Failed to install pypdf
    pause
    exit /b 1
)

echo Installing rich...
pip install rich==13.7.0
if errorlevel 1 (
    echo [ERROR] Failed to install rich
    pause
    exit /b 1
)

echo Installing typer...
pip install typer==0.9.0
if errorlevel 1 (
    echo [ERROR] Failed to install typer
    pause
    exit /b 1
)

echo Installing tiktoken...
pip install tiktoken==0.5.2
if errorlevel 1 (
    echo [ERROR] Failed to install tiktoken
    pause
    exit /b 1
)

echo.
echo ========================================
echo   All dependencies installed successfully!
echo ========================================
echo.
echo You can now run: run.bat
echo.

deactivate
pause
