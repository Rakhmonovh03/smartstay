@echo off
cd /d "%~dp0"
echo === SmartStay compile check === > compile_report.txt
echo Date: %date% %time% >> compile_report.txt
echo. >> compile_report.txt

set PY=python
if exist venv\Scripts\python.exe set PY=venv\Scripts\python.exe

%PY% --version >> compile_report.txt 2>&1
echo. >> compile_report.txt

for %%f in (main.py database.py buffet.py telegram.py config.py notifications.py crypto_util.py) do (
    %PY% -m py_compile %%f >> compile_report.txt 2>&1
    if errorlevel 1 (
        echo [FAIL] %%f >> compile_report.txt
    ) else (
        echo [OK]   %%f >> compile_report.txt
    )
)

echo. >> compile_report.txt
echo --- templates --- >> compile_report.txt
for %%f in (templates\*.py) do (
    %PY% -m py_compile %%f >> compile_report.txt 2>&1
    if errorlevel 1 (
        echo [FAIL] %%f >> compile_report.txt
    ) else (
        echo [OK]   %%f >> compile_report.txt
    )
)

echo. >> compile_report.txt
echo --- app import --- >> compile_report.txt
%PY% -c "import main; print('IMPORT OK, routes:', len(main.app.routes))" >> compile_report.txt 2>&1

echo Done. See compile_report.txt
pause
