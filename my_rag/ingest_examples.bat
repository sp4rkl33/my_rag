@echo off
echo ========================================
echo   RAG System - Ingest Example Documents
echo ========================================
echo.

REM Activate virtual environment
if not exist "venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run run.bat first to set up the environment.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo Ingesting example documents from data/documents/examples/
echo.

python ingest.py --dir data/documents/examples

echo.
echo ========================================
echo   Ingestion Complete!
echo ========================================
echo.
echo You can now:
echo   1. Run queries via CLI: python query.py "Your question here"
echo   2. Launch the web UI: run.bat
echo.

deactivate
pause
