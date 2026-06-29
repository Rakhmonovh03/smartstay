@echo off
cd /d "C:\Users\Victus\Desktop\smartstay"
git add -A
git commit -m "Fix JS SyntaxError (UZ apostrophe broke single-quoted string) + i18n wiring for dashboard/edit page"
git push
pause
