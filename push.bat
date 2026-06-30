@echo off
cd /d "C:\Users\Victus\Desktop\smartstay"
git add -A
git commit -m "Fix buffet page JS SyntaxError (UZ/TR apostrophes) + encrypt guest PII at rest"
git push
pause
