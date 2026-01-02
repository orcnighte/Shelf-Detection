@echo off
REM Quick start script for backend (Windows)

echo Starting Inventory Management Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r backend\requirements.txt

REM Create storage directory
if not exist "backend\storage\images" mkdir backend\storage\images
if not exist "backend\models" mkdir backend\models

REM Start the server
echo Starting FastAPI server...
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000




