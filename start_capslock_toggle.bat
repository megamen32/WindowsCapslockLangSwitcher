@echo off
rem -----------------------------------------------------------------------------
rem CapsLock Language Toggle Launcher
rem Place this .bat file in the same folder as "main.pyw" and the .venv directory.
rem Double-click to start the app silently (no console window).
rem -----------------------------------------------------------------------------

:: Resolve script directory
set "SCRIPT_DIR=%~dp0"

:: Check for venv pythonw.exe
if exist "%SCRIPT_DIR%.venv\Scripts\pythonw.exe" (
    start "" "%SCRIPT_DIR%.venv\Scripts\pythonw.exe" "%SCRIPT_DIR%main.pyw"
    goto :EOF
)

:: Fallback to venv python.exe (will briefly show console)
if exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
    start "" "%SCRIPT_DIR%.venv\Scripts\python.exe" "%SCRIPT_DIR%main.pyw"
    goto :EOF
)

:: Fallback to system pythonw or file association
where pythonw >nul 2>&1 && (
    start "" pythonw "%SCRIPT_DIR%main.pyw"
    goto :EOF
)

start "" "%SCRIPT_DIR%main.pyw"
:EOF
exit /b 0