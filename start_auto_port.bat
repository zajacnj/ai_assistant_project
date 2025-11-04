@echo off
REM VA AI Assistant - Auto Port Finder
REM This script will try ports 8502-8510 until it finds an available one

setlocal enabledelayedexpansion
set BASE_PORT=8502
set MAX_PORT=8510
set FOUND_PORT=0

echo ========================================
echo VA AI Assistant - Auto Port Finder
echo ========================================
echo.

for /L %%p in (%BASE_PORT%,1,%MAX_PORT%) do (
    if !FOUND_PORT!==0 (
        netstat -an | findstr ":%%p " | findstr "LISTENING" >nul
        if errorlevel 1 (
            set FOUND_PORT=%%p
            echo Found available port: %%p
            echo.
            echo Starting app on port %%p...
            echo App will open at http://localhost:%%p
            echo Press Ctrl+C to stop the server
            echo.
            py -3 -m streamlit run "main.py" --server.port=%%p --server.fileWatcherType=poll --server.runOnSave=true
            goto :end
        ) else (
            echo Port %%p is in use, trying next...
        )
    )
)

echo.
echo ERROR: No available ports found between %BASE_PORT% and %MAX_PORT%
echo Please close some applications or manually specify a different port.
pause
goto :end

:end
