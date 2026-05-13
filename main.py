from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime
import json, os, sqlite3

load_dotenv()

app = FastAPI()
client = Anthropic()

HOTEL_INFO = """
Ты AI консьерж отеля SmartStay Resort 5* в Анталии, Турция.
Отвечай ТОЛЬКО на языке на котором пишет гость — русский, турецкий, английский, немецкий, арабский.
Отвечай коротко, дружелюбно и по делу.

=== ИНФОРМАЦИЯ ОБ ОТЕЛЕ ===

🏊 БАССЕЙНЫ:
- Главный бассейн: 08:00 - 22:00
- Крытый бассейн: 07:00 - 23:00
- Детский бассейн: 09:00 - 20:00

🍽️ РЕСТОРАНЫ:
- Главный ресторан (шведский стол): завтрак 07:00-10:00, обед 12:30-14:30, ужин 19:00-21:30
- Ресторан à la carte "Akdeniz": 19:00-23:00, требуется резервация
- Снэк-бар у бассейна: 10:00-18:00
- Ночной бар: 21:00-02:00

☕ БАРЫ:
- Лобби-бар: 09:00-24:00
- Пляжный бар: 10:00-19:00
- Бар у бассейна: 10:00-20:00

💆 СПА И ФИТНЕС:
- СПА центр: 09:00-21:00
- Турецкая баня (хаммам): 10:00-20:00
- Фитнес зал: 07:00-22:00
- Запись в СПА: через этот чат или ресепшн (добавочный 9)

🏖️ ПЛЯЖ:
- Пляж: 08:00-20:00
- Лежаки и зонтики: бесплатно для гостей

🎭 АНИМАЦИЯ И РАЗВЛЕЧЕНИЯ:
- Дневная анимация у бассейна: 10:00-18:00
- Вечернее шоу: каждый день в 21:00 в амфитеатре
- Детский клуб: 09:00-18:00 (дети 4-12 лет)

🛎️ УСЛУГИ:
- Ресепшн: 24/7, добавочный 0
- Заказ еды в номер: 07:00-23:00, добавочный 8
- Уборка номера: каждый день до 14:00
- Дополнительная уборка: через этот чат
- Трансфер в аэропорт: добавочный 5
- Аренда авто: добавочный 6

🏥 ЭКСТРЕННЫЕ КОНТАКТЫ:
- Скорая помощь: 112
- Врач отеля: добавочный 7 (24/7)
- Пожарная: 110

📍 ЛОКАЦИЯ:
- Отель находится в Белеке, Анталия
- До аэропорта Анталии: 35 км, ~30 минут

=== ПРАВИЛА ===
- Если гость просит уборку или услугу — скажи "Передаю вашу просьбу персоналу, ожидайте"
- Если гость злится или есть проблема — посочувствуй и скажи что менеджер свяжется в течение 5 минут
- Если не знаешь ответ — скажи "Уточню у персонала и отвечу вам"
- Никогда не выдумывай информацию которой нет выше
"""

# База данных
def init_db():
    conn = sqlite3.connect("smartstay.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT,
            role TEXT,
            message TEXT,
            created_at TEXT,
            priority TEXT DEFAULT 'normal',
            is_read INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

URGENT_KEYWORDS = [
    "сломан", "сломался", "не работает", "авария", "пожар", "помогите",
    "срочно", "плохо", "болит", "врач", "горячей воды нет", "нет воды",
    "затопило", "сломана", "broken", "emergency", "help", "urgent",
    "doctor", "fire", "acil", "yardım", "bozuk", "çalışmıyor",
    "кран", "огонь", "горит", "течет", "течёт", "воды нет",
    "холодно", "жарко", "шум", "запах", "дым", "не открывается",
    "застрял", "лифт", "упал", "травма", "кровь"
]

def get_priority(message):
    msg_lower = message.lower()
    for keyword in URGENT_KEYWORDS:
        if keyword in msg_lower:
            return "urgent"
    return "normal"

def save_message(room, role, message):
    priority = get_priority(message) if role == "user" else "normal"
    conn = sqlite3.connect("smartstay.db")
    conn.execute(
        "INSERT INTO messages (room, role, message, created_at, priority, is_read) VALUES (?, ?, ?, ?, ?, ?)",
        (room, role, message, datetime.now().strftime("%Y-%m-%d %H:%M"), priority, 0)
    )
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect("smartstay.db")
    rows = conn.execute(
        """SELECT room, role, message, created_at, priority, is_read 
        FROM messages ORDER BY 
        CASE priority WHEN 'urgent' THEN 0 ELSE 1 END,
        id DESC LIMIT 100"""
    ).fetchall()
    conn.close()
    return rows

def get_unread_count():
    conn = sqlite3.connect("smartstay.db")
    count = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE is_read=0 AND role='user'"
    ).fetchone()[0]
    conn.close()
    return count

def mark_all_read():
    conn = sqlite3.connect("smartstay.db")
    conn.execute("UPDATE messages SET is_read=1")
    conn.commit()
    conn.close()

init_db()

# Чат страница для гостей
CHAT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartStay AI</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: sans-serif; background:#0a0a0a; color:white; height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; }
        .chat-box { width:380px; background:#1a1a1a; border-radius:16px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,0.5); }
        .chat-header { background:#C9A84C; padding:20px; text-align:center; }
        .chat-header h2 { font-size:18px; color:#000; }
        .chat-header p { font-size:12px; color:#333; margin-top:4px; }
        .room-bar { background:#111; padding:10px 20px; font-size:13px; color:#C9A84C; text-align:center; }
        .messages { height:380px; overflow-y:auto; padding:20px; display:flex; flex-direction:column; gap:12px; }
        .msg { padding:12px 16px; border-radius:12px; max-width:85%; font-size:14px; line-height:1.5; }
        .bot { background:#2a2a2a; align-self:flex-start; }
        .user { background:#C9A84C; color:#000; align-self:flex-end; }
        .input-area { padding:16px; display:flex; gap:8px; border-top:1px solid #333; }
        input { flex:1; background:#2a2a2a; border:none; border-radius:8px; padding:12px; color:white; font-size:14px; outline:none; }
        button { background:#C9A84C; border:none; border-radius:8px; padding:12px 16px; cursor:pointer; font-size:18px; }
    </style>
</head>
<body>
    <div class="chat-box">
        <div class="chat-header">
            <h2>🏨 SmartStay AI</h2>
            <p>Консьерж • Concierge • Konsiyerj</p>
        </div>
        <div class="room-bar">🚪 Номер: <span id="roomNum">101</span></div>
        <div class="messages" id="messages">
            <div class="msg bot">Добро пожаловать! 👋 Чем могу помочь?<br><br>Welcome! How can I help you?<br><br>Hoş geldiniz!</div>
        </div>
        <div class="input-area">
            <input type="text" id="input" placeholder="Напишите сообщение..." onkeypress="if(event.key==='Enter') send()">
            <button onclick="send()">➤</button>
        </div>
    </div>
    <script>
        const messages = [];
        const room = new URLSearchParams(window.location.search).get('room') || '101';
        document.getElementById('roomNum').textContent = room;

        async function send() {
            const input = document.getElementById('input');
            const text = input.value.trim();
            if (!text) return;

            addMessage(text, 'user');
            messages.push({role: 'user', content: text});
            input.value = '';
            input.disabled = true;

            const botDiv = document.createElement('div');
            botDiv.className = 'msg bot';
            botDiv.textContent = '...';
            document.getElementById('messages').appendChild(botDiv);

            const res = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text, history: messages.slice(0,-1), room: room})
            });

            const reader = res.body.getReader();
            const decoder = new TextDecoder();
            let fullText = '';

            while (true) {
                const {done, value} = await reader.read();
                if (done) break;
                const lines = decoder.decode(value).split('\\n');
                for (const line of lines) {
                    if (line.startsWith('data: ') && line !== 'data: [DONE]') {
                        try {
                            const data = JSON.parse(line.slice(6));
                            fullText += data.text;
                            botDiv.textContent = fullText;
                            document.getElementById('messages').scrollTop = 99999;
                        } catch(e) {}
                    }
                }
            }
            messages.push({role: 'assistant', content: fullText});
            input.disabled = false;
            input.focus();
        }

        function addMessage(text, type) {
            const div = document.createElement('div');
            div.className = 'msg ' + (type === 'user' ? 'user' : 'bot');
            div.textContent = text;
            document.getElementById('messages').appendChild(div);
            document.getElementById('messages').scrollTop = 99999;
        }
    </script>
</body>
</html>
"""

# Дашборд для менеджера
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartStay — Менеджер</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: sans-serif; background:#0a0a0a; color:white; padding:32px; }
        h1 { color:#C9A84C; font-size:24px; margin-bottom:8px; }
        .subtitle { color:#666; font-size:14px; margin-bottom:24px; }
        .stats { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:32px; }
        .stat { background:#1a1a1a; border-radius:12px; padding:24px; text-align:center; border-bottom:3px solid #C9A84C; }
        .stat.urgent { border-bottom-color:#E05555; }
        .stat .num { font-size:40px; font-weight:900; color:#C9A84C; }
        .stat.urgent .num { color:#E05555; }
        .stat .label { font-size:13px; color:#666; margin-top:8px; }
        .btns { display:flex; gap:12px; margin-bottom:24px; }
        .btn { padding:10px 24px; border-radius:8px; font-size:14px; font-weight:500; cursor:pointer; border:none; }
        .btn-gold { background:#C9A84C; color:#000; }
        .btn-dark { background:#1a1a1a; color:#fff; border:1px solid #333; }
        table { width:100%; border-collapse:collapse; background:#1a1a1a; border-radius:12px; overflow:hidden; }
        th { background:#C9A84C; color:#000; padding:14px 16px; text-align:left; font-size:13px; }
        td { padding:14px 16px; border-bottom:1px solid #222; font-size:14px; }
        tr:last-child td { border-bottom:none; }
        tr:hover td { background:#222; }
        tr.urgent-row td { background:rgba(224,85,85,0.08); }
        tr.urgent-row:hover td { background:rgba(224,85,85,0.15); }
        .badge { display:inline-block; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:500; }
        .badge-urgent { background:rgba(224,85,85,0.2); color:#E05555; border:1px solid rgba(224,85,85,0.4); }
        .badge-normal { background:rgba(76,175,80,0.2); color:#4CAF50; border:1px solid rgba(76,175,80,0.4); }
        .badge-bot { background:rgba(201,168,76,0.2); color:#C9A84C; border:1px solid rgba(201,168,76,0.4); }
        .room-tag { background:#222; padding:4px 10px; border-radius:20px; font-size:12px; color:#C9A84C; }
        .unread-badge { background:#E05555; color:white; border-radius:50%; padding:2px 8px; font-size:12px; margin-left:8px; }
        .filter-bar { display:flex; gap:8px; margin-bottom:16px; }
        .filter { padding:6px 16px; border-radius:20px; font-size:12px; cursor:pointer; border:1px solid #333; background:#1a1a1a; color:#fff; }
        .filter.active { background:#C9A84C; color:#000; border-color:#C9A84C; }
    </style>
</head>
<body>
    <h1>🏨 SmartStay — Панель менеджера <span id="unreadBadge"></span></h1>
    <p class="subtitle">Все запросы гостей в реальном времени</p>

    <div class="stats" id="stats"></div>

    <div class="btns">
        <button class="btn btn-gold" onclick="location.reload()">🔄 Обновить</button>
        <button class="btn btn-dark" onclick="markRead()">✅ Отметить все прочитанными</button>
        <button class="btn btn-dark" onclick="window.open('/qrcodes')">📱 QR Коды</button>
    </div>

    <div class="filter-bar">
        <button class="filter active" onclick="filterMessages('all', this)">Все</button>
        <button class="filter" onclick="filterMessages('urgent', this)">🔴 Срочные</button>
        <button class="filter" onclick="filterMessages('user', this)">👤 Гости</button>
        <button class="filter" onclick="filterMessages('bot', this)">🤖 AI</button>
    </div>

    <table>
        <thead>
            <tr>
                <th>Приоритет</th>
                <th>Номер</th>
                <th>Кто</th>
                <th>Сообщение</th>
                <th>Время</th>
            </tr>
        </thead>
        <tbody id="tbody"></tbody>
    </table>

    <script>
        let allData = [];
        let currentFilter = 'all';

        fetch('/api/messages')
            .then(r => r.json())
            .then(data => {
                allData = data;
                renderTable(data);

                const urgent = data.filter(m => m.priority === 'urgent').length;
                const rooms = new Set(data.map(m => m.room)).size;
                const userMsgs = data.filter(m => m.role === 'user').length;
                const unread = data.filter(m => m.is_read === 0 && m.role === 'user').length;

                if (unread > 0) {
                    document.getElementById('unreadBadge').innerHTML = 
                        `<span class="unread-badge">${unread} новых</span>`;
                }

                document.getElementById('stats').innerHTML = `
                    <div class="stat"><div class="num">${data.length}</div><div class="label">Всего сообщений</div></div>
                    <div class="stat"><div class="num">${rooms}</div><div class="label">Активных номеров</div></div>
                    <div class="stat"><div class="num">${userMsgs}</div><div class="label">Запросов гостей</div></div>
                    <div class="stat urgent"><div class="num">${urgent}</div><div class="label">🔴 Срочных</div></div>
                `;
            });

        function renderTable(data) {
            document.getElementById('tbody').innerHTML = data.map(m => `
                <tr class="${m.priority === 'urgent' ? 'urgent-row' : ''}">
                    <td>
                        ${m.priority === 'urgent' 
                            ? '<span class="badge badge-urgent">🔴 Срочно</span>' 
                            : '<span class="badge badge-normal">🟢 Норм</span>'}
                    </td>
                    <td><span class="room-tag">🚪 ${m.room}</span></td>
                    <td>${m.role === 'user' 
                        ? '<span class="badge badge-bot">👤 Гость</span>' 
                        : '<span class="badge badge-bot">🤖 AI</span>'}</td>
                    <td>${m.message}</td>
                    <td style="color:#666">${m.created_at}</td>
                </tr>
            `).join('');
        }

        function filterMessages(filter, btn) {
            currentFilter = filter;
            document.querySelectorAll('.filter').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            if (filter === 'all') renderTable(allData);
            else if (filter === 'urgent') renderTable(allData.filter(m => m.priority === 'urgent'));
            else renderTable(allData.filter(m => m.role === filter));
        }

        function markRead() {
            fetch('/api/mark-read', {method:'POST'})
                .then(() => location.reload());
                
        }
        // Автообновление каждые 3 секунды
        setInterval(() => {
            fetch('/api/messages')
                .then(r => r.json())
                .then(data => {
                    allData = data;
                    if (currentFilter === 'all') renderTable(data);
                    else if (currentFilter === 'urgent') renderTable(data.filter(m => m.priority === 'urgent'));
                    else renderTable(data.filter(m => m.role === currentFilter));

                    const urgent = data.filter(m => m.priority === 'urgent').length;
                    const rooms = new Set(data.map(m => m.room)).size;
                    const userMsgs = data.filter(m => m.role === 'user').length;
                    const unread = data.filter(m => m.is_read === 0 && m.role === 'user').length;

                    document.getElementById('unreadBadge').innerHTML = unread > 0 
                        ? `<span class="unread-badge">${unread} новых</span>` : '';

                    document.getElementById('stats').innerHTML = `
                        <div class="stat"><div class="num">${data.length}</div><div class="label">Всего сообщений</div></div>
                        <div class="stat"><div class="num">${rooms}</div><div class="label">Активных номеров</div></div>
                        <div class="stat"><div class="num">${userMsgs}</div><div class="label">Запросов гостей</div></div>
                        <div class="stat urgent"><div class="num">${urgent}</div><div class="label">🔴 Срочных</div></div>
                    `;
                });
        }, 3000);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return CHAT_HTML

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return DASHBOARD_HTML

@app.get("/api/messages")
def api_messages():
    rows = get_messages()
    return [{"room": r[0], "role": r[1], "message": r[2], "created_at": r[3], "priority": r[4], "is_read": r[5]} for r in rows]
@app.post("/api/mark-read")
def mark_read():
    mark_all_read()
    return {"status": "ok"}

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
            system=HOTEL_INFO + f"\n\nГость находится в номере: {room}. Ты уже знаешь номер — не спрашивай его снова.",
            messages=history
        ) as stream:
            for text in stream.text_stream:
                full_response.append(text)
                yield f"data: {json.dumps({'text': text})}\n\n"
        save_message(room, "bot", "".join(full_response))
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

import qrcode
import io
from fastapi.responses import Response

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
    cards = ""
    for room in rooms:
        cards += f"""
        <div class="card">
            <img src="/qr/{room}" alt="QR {room}">
            <div class="room">🚪 Номер {room}</div>
            <div class="hint">Сканируй для помощи</div>
        </div>
        """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>QR Коды — SmartStay</title>
        <style>
            * {{ margin:0; padding:0; box-sizing:border-box; }}
            body {{ background:#0a0a0a; color:white; font-family:sans-serif; padding:40px; }}
            h1 {{ color:#C9A84C; font-size:28px; margin-bottom:8px; }}
            p {{ color:#666; margin-bottom:32px; font-size:14px; }}
            .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(180px, 1fr)); gap:20px; }}
            .card {{ background:#1a1a1a; border-radius:12px; padding:24px; text-align:center; border:1px solid #333; }}
            .card img {{ width:140px; height:140px; border-radius:8px; }}
            .room {{ font-size:16px; font-weight:700; color:#C9A84C; margin-top:12px; }}
            .hint {{ font-size:12px; color:#666; margin-top:4px; }}
            .print-btn {{ background:#C9A84C; color:#000; border:none; padding:12px 32px; border-radius:8px; font-size:15px; font-weight:600; cursor:pointer; margin-bottom:32px; }}
        </style>
    </head>
    <body>
        <h1>🏨 QR Коды для номеров</h1>
        <p>Распечатай и повесь в каждый номер. Гость сканирует — попадает в чат.</p>
        <button class="print-btn" onclick="window.print()">🖨️ Распечатать все</button>
        <div class="grid">{cards}</div>
    </body>
    </html>
    """