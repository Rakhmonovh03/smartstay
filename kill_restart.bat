@echo off
echo === Останавливаем все Python процессы ===
taskkill /F /IM python.exe /T
echo.
echo === Ждём 2 секунды ===
timeout /t 2 /nobreak
echo.
echo === Запускаем сервер заново ===
cd /d "%~dp0"
python -m py_compile main.py
IF ERRORLEVEL 1 (
    echo [ОШИБКА] Синтаксическая ошибка в main.py!
    pause
    exit /b 1
)
echo [OK] Синтаксис проверен
echo.
echo Запускаю на http://127.0.0.1:8000
uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
