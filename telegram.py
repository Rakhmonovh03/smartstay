import json
import urllib.request
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


async def send_telegram(message: str, token: str = None, chat_id: str = None) -> int | None:
    """
    Send a Telegram message. Returns the Telegram message_id on success, else None.
    Needed for 2-way reply routing: we store (hotel_slug, room, message_id) so that
    when staff replies in Telegram, we know which room the reply belongs to.
    """
    use_token   = token   if token   else TELEGRAM_TOKEN
    use_chat_id = chat_id if chat_id else TELEGRAM_CHAT_ID

    if not use_token or not use_chat_id:
        return None

    try:
        url  = f"https://api.telegram.org/bot{use_token}/sendMessage"
        data = json.dumps({
            "chat_id":    use_chat_id,
            "text":       message,
            "parse_mode": "HTML",
        }).encode()
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            return result.get("result", {}).get("message_id")
    except Exception as e:
        print(f"Telegram error: {e}")
        return None


async def set_webhook(token: str, webhook_url: str) -> dict:
    """Register our webhook URL with Telegram for a given bot token."""
    try:
        url  = f"https://api.telegram.org/bot{token}/setWebhook"
        data = json.dumps({"url": webhook_url, "allowed_updates": ["message"]}).encode()
        req  = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"ok": False, "error": str(e)}


async def send_urgent_alert(hotel_name: str, room: str, message: str,
                             token: str = None, chat_id: str = None) -> int | None:
    from datetime import datetime
    text = (
        f"🔴 <b>СРОЧНО!</b>\n"
        f"🏨 Отель: {hotel_name}\n"
        f"🚪 Номер: {room}\n"
        f"💬 Сообщение: {message}\n"
        f"⏰ Время: {datetime.now().strftime('%H:%M')}\n\n"
        f"<i>↩️ Ответьте на это сообщение, чтобы написать гостю.</i>"
    )
    return await send_telegram(text, token=token, chat_id=chat_id)
