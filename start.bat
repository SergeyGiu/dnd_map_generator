@echo off
call .venv\Scripts\activate.bat
pip freeze
pause
python main_console.py
pause