@echo off
call venv\Scripts\activate.bat
set FLASK_APP=wsgi.py
set FLASK_ENV=development
python -m flask run