@echo off
echo ========================================
echo   RAG System - Quick Setup (Python 3.14)
echo ========================================
echo.

echo [1/5] Checking Python...
py --version
echo.

echo [2/5] Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists, skipping...
) else (
    py -m venv venv
    echo Created!
)
echo.

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [4/5] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [5/5] Installing packages (this may take 5-10 minutes)...
echo Installing latest compatible versions for Python 3.14...
echo.

pip install --upgrade sentence-transformers
pip install --upgrade chromadb
pip install --upgrade ollama
pip install --upgrade streamlit
pip install --upgrade pypdf
pip install --upgrade rich
pip install --upgrade typer
pip install --upgrade tiktoken

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Start Ollama: ollama serve
echo   2. Pull model: ollama pull llama3.1:8b
echo   3. Run app: streamlit run app.py
echo.
pause
