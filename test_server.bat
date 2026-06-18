@echo off
echo === Диагностика сервера ===
echo.
echo --- Процессы Python:
tasklist | findstr /i python
echo.
echo --- Что слушает порт 8000:
netstat -ano | findstr :8000
echo.
echo --- Проверка подключения:
python -c "import urllib.request; r = urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5); print('OK:', r.read()[:100])"
echo.
pause
