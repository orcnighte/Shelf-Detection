@echo off
REM Quick start script for backend (Windows)

echo Starting Inventory Management Backend...

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo Creating virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

REM Activate virtual environment
call backend\venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r backend\requirements.txt

REM Create storage directory
if not exist "backend\storage\images" mkdir backend\storage\images
if not exist "backend\media" mkdir backend\media

REM Run migrations
echo Running database migrations...
cd backend
python manage.py migrate

REM Start the server
echo Starting Django server...
echo Server will be available at: http://127.0.0.1:8000
python manage.py runserver




