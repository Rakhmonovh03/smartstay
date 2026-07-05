@echo off
cd /d "%~dp0"

set /p MSG="Commit message: "
if "%MSG%"=="" set MSG=update

git add -A
git commit -m "%MSG%"
git push
pause
