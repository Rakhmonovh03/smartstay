import os
import warnings
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Passwords — warn loudly if using insecure defaults
_manager_pw = os.getenv("MANAGER_PASSWORD")
if not _manager_pw:
    warnings.warn("⚠️  MANAGER_PASSWORD not set — using insecure default. Set it in .env before production!", stacklevel=2)
MANAGER_PASSWORD = _manager_pw or "smartstay2025"

_admin_pw = os.getenv("ADMIN_PASSWORD")
if not _admin_pw:
    warnings.warn("⚠️  ADMIN_PASSWORD not set — using insecure default. Set it in .env before production!", stacklevel=2)
ADMIN_PASSWORD = _admin_pw or "admin_smartstay_2026"

DATABASE_PATH = os.getenv("DATABASE_PATH", "smartstay.db")

# Registration invite code. Empty string = open registration (dev/pilot mode).
# Set INVITE_CODE=xyz in .env to require a code on the register page.
INVITE_CODE = os.getenv("INVITE_CODE", "")

# Set SECURE_COOKIES=true in Railway (HTTPS). Keep false for local HTTP dev.
SECURE_COOKIES = os.getenv("SECURE_COOKIES", "false").lower() == "true"

# Message limits per plan per calendar month (user messages only).
# -1 = unlimited.
PLAN_LIMITS = {
    "trial":   500,
    "starter": 2000,
    "pro":     10000,
    "premium": -1,
}

# Secret for the /api/cron/* endpoints — set to a random string in production.
# Leave empty to disable cron endpoints entirely.
CRON_SECRET = os.getenv("CRON_SECRET", "")

URGENT_KEYWORDS = [
    "сломан", "сломался", "не работает", "авария", "пожар", "помогите",
    "срочно", "плохо", "болит", "врач", "горячей воды нет", "нет воды",
    "затопило", "сломана", "broken", "emergency", "help", "urgent",
    "doctor", "fire", "acil", "yardım", "bozuk", "çalışmıyor",
    "кран", "огонь", "горит", "течет", "течёт", "воды нет",
    "холодно", "жарко", "шум", "запах", "дым", "не открывается",
    "застрял", "лифт", "упал", "травма", "кровь"
]