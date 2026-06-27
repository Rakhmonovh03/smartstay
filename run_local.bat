@echo off
chcp 65001 >nul
cd /d "%~dp0"
title SmartStay — локальный запуск

echo ============================================
echo   SmartStay — локальный запуск для просмотра
echo ============================================
echo.

REM --- 1. Виртуальное окружение ---
if not exist venv (
    echo [1/4] Создаю виртуальное окружение...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo [!] Python не найден. Установи Python 3 с https://python.org и поставь галочку "Add to PATH".
        pause
        exit /b 1
    )
) else (
    echo [1/4] Виртуальное окружение уже есть.
)
call venv\Scripts\activate

REM --- 2. Зависимости ---
echo [2/4] Устанавливаю зависимости (может занять минуту)...
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo.
    echo [!] Не удалось установить зависимости. Смотри сообщение выше.
    pause
    exit /b 1
)

REM --- 3. Проверка компиляции (синтаксис всех файлов) ---
echo [3/4] Проверяю код на ошибки...
python -m py_compile main.py database.py buffet.py telegram.py config.py notifications.py
if errorlevel 1 (
    echo.
    echo [!] ОШИБКА КОМПИЛЯЦИИ — смотри сообщение выше. Сервер не запускаю.
    pause
    exit /b 1
)
echo     Код в порядке.

REM --- 4. Запуск ---
echo [4/4] Запускаю сервер...
echo.
echo ============================================
echo   Открой в браузере:  http://127.0.0.1:8000
echo   Остановить сервер:   Ctrl + C
echo ============================================
echo.
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
