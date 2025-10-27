@echo off
echo ========================================
echo AI Assistant Setup Script
echo ========================================
echo.

echo Installing Python packages...
pip install -r requirements.txt

echo.
echo Setting up project structure...
python ai_assistant_setup.py

echo.
echo Setting up database...
python database_setup.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run your application:
echo   streamlit run main.py
echo.
echo To import your real data:
echo   1. Place your CSV files in ai_assistant/data/
echo   2. Run: python import_real_data.py
echo.
pause
