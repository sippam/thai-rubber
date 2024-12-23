@echo off
REM Start Flask app with watchdog auto-restart
watchmedo auto-restart --patterns="*.py" --recursive -- python line.py
pause
