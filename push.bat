@echo off
cd /d "C:\Users\Victus\Desktop\smartstay"
git add -A
git commit -m "Security (signed cookies, XSS fixes), bug fixes, full i18n (chat/public/admin), QR in dashboard, staff-reply delivery fix"
git push
pause
