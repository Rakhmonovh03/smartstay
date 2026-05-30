import json
import urllib.request
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

async def send_telegram(message: str, token: str = None, chat_id: str = None):
    use_token = token if token else TELEGRAM_TOKEN
    use_chat_id = chat_id if chat_id else TELEGRAM_CHAT_ID

    if not use_token or not use_chat_id:
        return

    try:
        url = f"https://api.telegram.org/bot{use_token}/sendMessage"
        data = json.dumps({
            "chat_id": use_chat_id,
            "text": message,
            "parse_mode": "HTML"
        }).encode()
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"Telegram error: {e}")

async def send_urgent_alert(hotel_name: str, room: str, message: str,
                             token: str = None, chat_id: str = None):
    from datetime import datetime
    text = (
        f"🔴 <b>СРОЧНО!</b>\n"
        f"🏨 Отель: {hotel_name}\n"
        f"🚪 Номер: {room}\n"
        f"💬 Сообщение: {message}\n"
        f"⏰ Время: {datetime.now().strftime('%H:%M')}"
    )
    await send_telegram(text, token=token, chat_id=chat_id)