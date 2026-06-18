@echo off
cd /d "%~dp0"
echo === SmartStay AI — запуск сервера ===

echo Останавливаем старые процессы на порту 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /PID %%a /F >nul 2>&1
)
timeout /t 1 /nobreak >nul

python -m py_compile main.py
IF ERRORLEVEL 1 (
    echo.
    echo [ОШИБКА] Синтаксическая ошибка в main.py!
    pause
    exit /b 1
)
python -m py_compile database.py
IF ERRORLEVEL 1 (
    echo.
    echo [ОШИБКА] Синтаксическая ошибка в database.py!
    pause
    exit /b 1
)
echo [OK] Синтаксис проверен
echo.
echo Запускаю на http://127.0.0.1:8000
uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
