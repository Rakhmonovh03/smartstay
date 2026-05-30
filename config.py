import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TELEGRAM_TOKEN = "8644783291:AAFdATLmPL3vityqTyvSfhLi0yRMDwbl8Oc"
TELEGRAM_CHAT_ID = "916372970"
MANAGER_PASSWORD = "smartstay2025"
ADMIN_PASSWORD = "admin_smartstay_2026"
DATABASE_PATH = "smartstay.db"

URGENT_KEYWORDS = [
    "сломан", "сломался", "не работает", "авария", "пожар", "помогите",
    "срочно", "плохо", "болит", "врач", "горячей воды нет", "нет воды",
    "затопило", "сломана", "broken", "emergency", "help", "urgent",
    "doctor", "fire", "acil", "yardım", "bozuk", "çalışmıyor",
    "кран", "огонь", "горит", "течет", "течёт", "воды нет",
    "холодно", "жарко", "шум", "запах", "дым", "не открывается",
    "застрял", "лифт", "упал", "травма", "кровь"
]