@echo off
echo ========================================
echo Stopping All Streamlit Processes
echo ========================================
echo.

REM Kill any Python processes running streamlit
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *streamlit*" 2>nul
taskkill /F /IM py.exe /FI "WINDOWTITLE eq *streamlit*" 2>nul

REM Alternative: Kill all streamlit processes
for /f "tokens=2" %%a in ('tasklist ^| findstr /i "streamlit"') do (
    taskkill /F /PID %%a 2>nul
)

REM Kill processes using ports 8502-8510
for /L %%p in (8502,1,8510) do (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%%p" ^| findstr "LISTENING"') do (
        echo Killing process on port %%p (PID: %%a)
        taskkill /F /PID %%a 2>nul
    )
)

echo.
echo All Streamlit processes have been stopped.
echo You can now run start.bat to restart the app.
echo.
pause
