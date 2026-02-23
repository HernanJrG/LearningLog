@echo off
setlocal

set "WIN_DIR=%~dp0"
for /f "usebackq delims=" %%I in (`wsl wslpath "%WIN_DIR%"`) do set "WSL_DIR=%%I"

if not defined WSL_DIR (
  echo Failed to resolve WSL path for %WIN_DIR%
  exit /b 1
)

if "%~1"=="" (
  wsl bash -lc "cd '%WSL_DIR%' && ./run.sh"
) else (
  wsl bash -lc "cd '%WSL_DIR%' && ./run.sh %*"
)

endlocal
