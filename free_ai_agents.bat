@echo off
:: free_ai_agents.bat - Smart Launcher for AI Coding Agents
title AI Coding Agents - Smart Launcher
color 0B
setlocal EnableDelayedExpansion

:: تغيير ترميز الشاشة إلى UTF-8 لدعم الرموز والألوان في واجهة البايثون
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

:: الانتقال إلى مجلد السكربت الحالي
cd /d "%~dp0"

echo ===================================================
echo      AI Coding Agents - Smart Launcher
echo ===================================================
echo.

:: 1. فحص وجود لغة بايثون
where python >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo [INFO] Opening Python download page...
    start "" "https://www.python.org/downloads/"
    pause
    exit /b 1
)

:: 2. فحص وجود Node.js و npm
where node >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Node.js is not installed.
    echo [INFO] Opening Node.js download page...
    start "" "https://nodejs.org/"
    pause
    exit /b 1
)
where npm >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] npm is not installed.
    start "" "https://nodejs.org/"
    pause
    exit /b 1
)

:: 3. تثبيت المتطلبات (يتم مرة واحدة فقط)
if not exist ".setup_complete" (
    echo [SETUP] First-time setup initiated. This may take a few minutes...
    echo.
    
    echo [SETUP] Installing Python packages...
    python -m pip install rich questionary colorama pyfiglet pyyaml
    
    echo.
    echo [SETUP] Installing Claude Code CLI globally...
    call npm install -g @anthropic-ai/claude-code
    
    echo.
    echo ===================================================
    echo [WARNING] If you see any prompts asking you to log in 
    echo or press Enter during the next steps, please interact with them.
    echo ===================================================
    echo.
    
    echo Installing frontend-design plugin...
    call claude plugin add anthropic/frontend-design
    
    echo.
    echo Installing ui-ux-pro-max-skill plugin...
    call claude plugin add nextlevelbuilder/ui-ux-pro-max-skill
    
    echo.
    echo Adding wunderui MCP server...
    call claude mcp add wunderui -- npx -y wunderui-mcp
    
    echo.
    echo Adding schemaflow MCP server...
    call claude mcp add schemaflow -- npx -y schemaflow-mcp
    
    echo.
    echo Installing Claude MCP...
    call npx -y @lotwhite/model-context-protocol install-claude-mcp
    
    echo.
    echo [SETUP] Setup complete. Creating marker file...
    echo %DATE% %TIME% > ".setup_complete"
)

:: 4. تشغيل واجهة البايثون
if not exist "free_ai_agents.py" (
    echo [ERROR] free_ai_agents.py not found in the current directory!
    pause
    exit /b 1
)

echo.
echo [LAUNCH] Starting AI Coding Agents Interface...
python "free_ai_agents.py"

if !errorlevel! neq 0 (
    echo.
    echo [ERROR] Failed to launch the Python interface.
    pause
    exit /b 1
)