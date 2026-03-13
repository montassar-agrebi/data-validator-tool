@echo off
color 0F
title Data Validation Tool

echo ======================================
echo        DATA VALIDATION TOOL
echo ======================================

set PYTHON_EXE=%~dp0python_portable\python.exe

if not exist "%PYTHON_EXE%" (
    echo.
    echo ERROR: Portable Python not found.
    echo Expected: python_portable\python.exe
    echo.
    pause
    exit /b
)

echo.
echo [1/3] Checking Streamlit installation...

if exist "%~dp0python_portable\Scripts\streamlit.exe" goto launch

echo.
echo [2/3] Installing required libraries...

"%PYTHON_EXE%" -m pip install -r "%~dp0requirements.txt" --quiet --no-warn-script-location

:launch
echo.
echo [3/3] Launching Data Validation Tool...
echo.

start "" http://localhost:8501

"%PYTHON_EXE%" -m streamlit run "%~dp0app.py" --browser.gatherUsageStats false --server.headless true

pause