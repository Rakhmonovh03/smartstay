from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.responses import Response
from anthropic import Anthropic
from dotenv import load_dotenv
import json, sqlite3, asyncio
import qrcode, io

from config import MANAGER_PASSWORD, ADMIN_PASSWORD
from database import (
    init_db, get_priority, save_message, get_messages,
    create_hotel, get_hotel, get_all_hotels, get_hotel_messages,
    save_hotel_message, mark_hotel_read, mark_all_read,
    update_hotel, get_hotel_stats
)
from telegram import send_urgent_alert
from templates.chat_html import get_chat_html
from templates.dashboard_html import get_dashboard_html
from templates.admin_html import get_admin_html, get_admin_login_html
from templates.other_html import get_login_html, get_register_html, get_edit_html

load_dotenv()

app = FastAPI()
client = Anthropic()

HOTEL_INFO = """
Ты AI консьерж отеля SmartStay Resort 5* в Анталии, Турция.
Отвечай ТОЛЬКО на языке на котором пишет гость.
Отвечай коротко, дружелюбно и по делу.
Если не знаешь ответ — скажи "Уточню у персонала".
"""

init_db()

# ===== ГЛАВНАЯ =====
@app.get("/", response_class=HTMLResponse)
def home():
    return get_chat_html()

# ===== РЕГИСТРАЦИЯ =====
@app.get("/register", response_class=HTMLResponse)
def register_page():
    return get_register_html()

@app.post("/api/register")
def api_register(data: dict):
    slug = data.get("slug", "").strip()
    name = data.get("name", "").strip()
    password = data.get("password", "").strip()
    info = data.get("info", "").strip()
    tg_token = data.get("tg_token", "").strip()
    tg_chat = data.get("tg_chat", "").strip()

    if not all([slug, name, password, info]):
        return {"ok": False, "error": "Zorunlu alanlar eksik"}
    if get_hotel(slug):
        return {"ok": False, "error": "Bu slug zaten kullanılıyor"}

    create_hotel(slug, name, password, info, tg_token, tg_chat)
    return {"ok": True, "slug": slug}

# ===== LOGIN =====
@app.get("/login", response_class=HTMLResponse)
def login_page():
    return get_login_html()

@app.post("/api/login")
def api_login(data: dict, response: Response):
    if data.get("password") == MANAGER_PASSWORD:
        response.set_cookie("manager_auth", "yes", max_age=86400)
        return {"ok": True}
    return {"ok": False}

@app.get("/hotel/{slug}/login", response_class=HTMLResponse)
def hotel_login_page(slug: str):
    hotel = get_hotel(slug)
    if not hotel:
        return HTMLResponse("❌ Otel bulunamadı", status_code=404)
    return get_login_html(hotel["name"])

from fastapi import Response as FastAPIResponse

@app.post("/api/hotel-login")
async def api_hotel_login(request: Request):
    from fastapi.responses import JSONResponse
    data = await request.json()
    slug = data.get("slug", "")
    password = data.get("password", "")
    hotel = get_hotel(slug)
    if hotel and hotel["password"] == password:
        response = JSONResponse({"ok": True})
        response.set_cookie(
            key=f"auth_{slug}",
            value="yes",
            max_age=86400,
            httponly=False,
            samesite="lax",
            path="/"
        )
        return response
    return JSONResponse({"ok": False})

# ===== DASHBOARD =====
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if request.cookies.get("manager_auth") != "yes":
        return RedirectResponse("/login")
    return get_dashboard_html()

@app.get("/hotel/{slug}/dashboard", response_class=HTMLResponse)
def hotel_dashboard(slug: str, request: Request):
    hotel = get_hotel(slug)
    if not hotel:
        return HTMLResponse("❌ Otel bulunamadı", status_code=404)
    auth = request.cookies.get(f"auth_{slug}")
    if auth != "yes":
        return RedirectResponse(f"/hotel/{slug}/login", status_code=302)
    return get_dashboard_html(hotel["name"])

# ===== HOTEL CHAT =====
@app.get("/hotel/{slug}", response_class=HTMLResponse)
def hotel_chat(slug: str):
    hotel = get_hotel(slug)
    if not hotel:
        return HTMLResponse("❌ Otel bulunamadı", status_code=404)
    return get_chat_html(hotel["name"])

@app.post("/hotel/{slug}/chat")
async def hotel_chat_api(slug: str, data: dict):
    hotel = get_hotel(slug)
    if not hotel:
        return {"error": "Hotel not found"}

    history = data.get("history", [])
    message = data.get("message", "")
    room = data.get("room", "101")

    priority = save_hotel_message(slug, room, "user", message)
    if priority == "urgent":
        asyncio.create_task(send_urgent_alert(
            hotel_name=hotel["name"],
            room=room,
            message=message,
            token=hotel.get("telegram_token"),
            chat_id=hotel.get("telegram_chat_id")
        ))

    history.append({"role": "user", "content": message})
    system = hotel["info"] + f"\n\nОтель: {hotel['name']}\nНомер гостя: {room}. Не спрашивай номер снова.\nОтвечай на языке гостя."

    def generate():
        full_response = []
        with client.messages.stream(
            model="claude-sonnet-4-5",
            max_tokens=500,
            system=system,
            messages=history
        ) as stream:
            for text in stream.text_stream:
                full_response.append(text)
                yield f"data: {json.dumps({'text': text})}\n\n"
        save_hotel_message(slug, room, "bot", "".join(full_response))
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

# ===== MAIN CHAT =====
@app.post("/chat")
async def chat(data: dict):
    history = data.get("history", [])
    message = data.get("message", "")
    room = data.get("room", "101")

    save_message(room, "user", message)
    history.append({"role": "user", "content": message})

    def generate():
        full_response = []
        with client.messages.stream(
            model="claude-sonnet-4-5",
            max_tokens=500,
            system=HOTEL_INFO + f"\n\nНомер гостя: {room}.",
            messages=history
        ) as stream:
            for text in stream.text_stream:
                full_response.append(text)
                yield f"data: {json.dumps({'text': text})}\n\n"
        save_message(room, "bot", "".join(full_response))
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

# ===== API MESSAGES =====
@app.get("/api/messages")
def api_messages():
    rows = get_messages()
    return [{"room": r[0], "role": r[1], "message": r[2], "created_at": r[3], "priority": r[4], "is_read": r[5]} for r in rows]

@app.post("/api/mark-read")
def mark_read():
    mark_all_read()
    return {"status": "ok"}

@app.get("/api/hotel/{slug}/stats")
def hotel_stats(slug: str):
    conn = sqlite3.connect("smartstay.db")
    
    # Сообщения по дням за последние 7 дней
    days = conn.execute("""
        SELECT 
            substr(created_at, 1, 10) as day,
            COUNT(*) as total,
            SUM(CASE WHEN priority='urgent' THEN 1 ELSE 0 END) as urgent,
            SUM(CASE WHEN role='user' THEN 1 ELSE 0 END) as guests
        FROM messages 
        WHERE hotel_slug=?
        AND created_at >= date('now', '-7 days')
        GROUP BY day
        ORDER BY day ASC
    """, (slug,)).fetchall()
    
    # Топ запросы
    top_rooms = conn.execute("""
        SELECT room, COUNT(*) as count
        FROM messages
        WHERE hotel_slug=? AND role='user'
        GROUP BY room
        ORDER BY count DESC
        LIMIT 5
    """, (slug,)).fetchall()
    
    conn.close()
    
    return {
        "days": [{"day": r[0], "total": r[1], "urgent": r[2], "guests": r[3]} for r in days],
        "top_rooms": [{"room": r[0], "count": r[1]} for r in top_rooms]
    }

@app.get("/api/hotel/{slug}/messages")
def hotel_messages(slug: str):
    rows = get_hotel_messages(slug)
    return [{"room": r[0], "role": r[1], "message": r[2], "created_at": r[3], "priority": r[4], "is_read": r[5]} for r in rows]

@app.post("/api/hotel/{slug}/mark-read")
def hotel_mark_read_api(slug: str):
    mark_hotel_read(slug)
    return {"status": "ok"}

@app.get("/api/hotel/{slug}/info")
def hotel_info(slug: str):
    hotel = get_hotel(slug)
    if not hotel:
        return {"error": "Not found"}
    return {
        "name": hotel["name"],
        "info": hotel["info"],
        "telegram_token": hotel.get("telegram_token", ""),
        "telegram_chat_id": hotel.get("telegram_chat_id", "")
    }

@app.post("/api/hotel/{slug}/update")
def hotel_update(slug: str, data: dict, request: Request):
    if request.cookies.get(f"auth_{slug}") != "yes":
        return {"ok": False, "error": "Unauthorized"}
    name = data.get("name", "").strip()
    info = data.get("info", "").strip()
    password = data.get("password", "").strip()
    tg_token = data.get("tg_token", "").strip()
    tg_chat = data.get("tg_chat", "").strip()
    if not name or not info:
        return {"ok": False, "error": "Ad ve bilgiler gerekli"}
    update_hotel(slug, name, info,
                 password if password else None,
                 tg_token, tg_chat)
    return {"ok": True}

# ===== EDIT =====
@app.get("/hotel/{slug}/edit", response_class=HTMLResponse)
def hotel_edit(slug: str, request: Request):
    hotel = get_hotel(slug)
    if not hotel:
        return HTMLResponse("❌ Otel bulunamadı", status_code=404)
    if request.cookies.get(f"auth_{slug}") != "yes":
        return RedirectResponse(f"/hotel/{slug}/login")
    return get_edit_html()

# ===== QR CODES =====
@app.get("/hotel/{slug}/qr/{room}")
def hotel_qr(slug: str, room: str, request: Request):
    base = str(request.base_url).rstrip("/")
    url = f"{base}/hotel/{slug}?room={room}"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#C9A84C", back_color="#0a0a0a")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return Response(content=buf.getvalue(), media_type="image/png")

@app.get("/hotel/{slug}/qrcodes", response_class=HTMLResponse)
def hotel_qrcodes(slug: str, request: Request):
    hotel = get_hotel(slug)
    if not hotel:
        return HTMLResponse("❌ Otel bulunamadı", status_code=404)
    rooms = list(range(101, 111)) + list(range(201, 211)) + list(range(301, 311))
    cards = "".join([f"""
        <div class="card">
            <img src="/hotel/{slug}/qr/{room}">
            <div class="room">🚪 {room}</div>
        </div>""" for room in rooms])
    return f"""<!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>QR — {hotel['name']}</title>
    <style>
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{background:#0a0a0a;color:white;font-family:sans-serif;padding:40px}}
        h1{{color:#C9A84C;font-size:28px;margin-bottom:8px}}
        p{{color:#666;margin-bottom:32px;font-size:14px}}
        .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:20px}}
        .card{{background:#111;border-radius:12px;padding:24px;text-align:center;border:1px solid #222}}
        .card img{{width:140px;height:140px;border-radius:8px}}
        .room{{font-size:16px;font-weight:700;color:#C9A84C;margin-top:12px}}
        .btn{{background:#C9A84C;color:#000;border:none;padding:12px 32px;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;margin-bottom:32px}}
    </style></head>
    <body>
        <h1>🏨 {hotel['name']} — QR Kodlar</h1>
        <p>Her odaya yapıştırın. Misafir tarar → sohbete girer.</p>
        <button class="btn" onclick="window.print()">🖨️ Yazdır</button>
        <div class="grid">{cards}</div>
    </body></html>"""

@app.get("/qr/{room}")
def get_qr(room: str):
    url = f"https://web-production-467dd.up.railway.app?room={room}"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#C9A84C", back_color="#0a0a0a")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return Response(content=buf.getvalue(), media_type="image/png")

@app.get("/qrcodes", response_class=HTMLResponse)
def qrcodes():
    rooms = list(range(101, 111)) + list(range(201, 211)) + list(range(301, 311))
    cards = "".join([f"""
        <div class="card">
            <img src="/qr/{room}">
            <div class="room">🚪 {room}</div>
        </div>""" for room in rooms])
    return f"""<!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>QR Kodlar</title>
    <style>
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{background:#0a0a0a;color:white;font-family:sans-serif;padding:40px}}
        h1{{color:#C9A84C;font-size:28px;margin-bottom:32px}}
        .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:20px}}
        .card{{background:#111;border-radius:12px;padding:24px;text-align:center;border:1px solid #222}}
        .card img{{width:140px;height:140px;border-radius:8px}}
        .room{{font-size:16px;font-weight:700;color:#C9A84C;margin-top:12px}}
        .btn{{background:#C9A84C;color:#000;border:none;padding:12px 32px;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;margin-bottom:32px}}
    </style></head>
    <body>
        <h1>🏨 QR Kodlar</h1>
        <button class="btn" onclick="window.print()">🖨️ Yazdır</button>
        <div class="grid">{cards}</div>
    </body></html>"""

# ===== ADMIN =====
@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_page():
    return get_admin_login_html()

@app.post("/api/admin/login")
def api_admin_login(data: dict, response: Response):
    if data.get("password") == ADMIN_PASSWORD:
        response.set_cookie("admin_auth", "yes", max_age=86400)
        return {"ok": True}
    return {"ok": False}

@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request):
    if request.cookies.get("admin_auth") != "yes":
        return RedirectResponse("/admin/login")
    return get_admin_html()

@app.get("/admin/logout")
def admin_logout(response: Response):
    response.delete_cookie("admin_auth")
    return RedirectResponse("/admin/login")

@app.get("/api/admin/hotels")
def api_admin_hotels(request: Request):
    if request.cookies.get("admin_auth") != "yes":
        return {"error": "Unauthorized"}
    hotels = get_all_hotels()
    conn = sqlite3.connect("smartstay.db")
    total_messages = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    for hotel in hotels:
        count = conn.execute(
            "SELECT COUNT(*) FROM messages WHERE hotel_slug=?",
            (hotel["slug"],)
        ).fetchone()[0]
        hotel["message_count"] = count
        hotel["telegram_token"] = conn.execute(
            "SELECT telegram_token FROM hotels WHERE slug=?",
            (hotel["slug"],)
        ).fetchone()[0] or ""
    conn.close()
    return {"hotels": hotels, "total_messages": total_messages}