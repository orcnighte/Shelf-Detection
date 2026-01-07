@echo off
REM Script to fix database issues

echo Fixing database issues...

cd backend

REM Check if virtual environment exists
if exist "venv" (
    call venv\Scripts\activate.bat
)

REM Run migrations
echo Running migrations...
python manage.py migrate

REM Create superuser if needed (optional)
echo.
echo Database fixed!
echo.
echo If you need to create a superuser, run:
echo python manage.py createsuperuser

pause

