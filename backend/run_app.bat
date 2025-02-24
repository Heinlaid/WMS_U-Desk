@echo off
cd /d "%~dp0"
call venv\Scripts\activate
start "" "http://127.0.0.1:5000/"
flask run --reload
pause