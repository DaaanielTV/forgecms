@echo off
echo Setting up ForgeCMS development environment...

:: Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate.bat

:: Install requirements
pip install -r requirements.txt

:: Set up the Flask environment
set FLASK_APP=wsgi.py
set FLASK_ENV=development

:: Initialize database migrations
python -m flask db init
python -m flask db migrate -m "Initial migration"
python -m flask db upgrade

echo Setup complete! You can now run the application with: flask run