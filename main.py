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
Ты AI консьерж отеля SmartStay в Анталии.
Отвечай на любом языке на котором пишет гость.
Ты помогаешь с:
- Информацией об отеле (спа, рестораны, бассейн, часы работы)
- Заказом еды в номер
- Записью в спа
- Уборкой номера
- Любыми вопросами гостя
Будь вежливым и дружелюбным. Отвечай коротко и по делу.
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
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(room, role, message):
    conn = sqlite3.connect("smartstay.db")
    conn.execute(
        "INSERT INTO messages (room, role, message, created_at) VALUES (?, ?, ?, ?)",
        (room, role, message, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect("smartstay.db")
    rows = conn.execute(
        "SELECT room, role, message, created_at FROM messages ORDER BY id DESC LIMIT 100"
    ).fetchall()
    conn.close()
    return rows

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
        .subtitle { color:#666; font-size:14px; margin-bottom:32px; }
        .stats { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-bottom:32px; }
        .stat { background:#1a1a1a; border-radius:12px; padding:24px; text-align:center; border-bottom:3px solid #C9A84C; }
        .stat .num { font-size:40px; font-weight:900; color:#C9A84C; }
        .stat .label { font-size:13px; color:#666; margin-top:8px; }
        table { width:100%; border-collapse:collapse; background:#1a1a1a; border-radius:12px; overflow:hidden; }
        th { background:#C9A84C; color:#000; padding:14px 16px; text-align:left; font-size:13px; }
        td { padding:14px 16px; border-bottom:1px solid #222; font-size:14px; }
        tr:last-child td { border-bottom:none; }
        tr:hover td { background:#222; }
        .role-user { color:#C9A84C; font-weight:500; }
        .role-bot { color:#4CAF50; }
        .room-tag { background:#222; padding:4px 10px; border-radius:20px; font-size:12px; color:#C9A84C; }
        .refresh { background:#C9A84C; color:#000; border:none; padding:10px 24px; border-radius:8px; cursor:pointer; font-size:14px; font-weight:500; margin-bottom:24px; }
    </style>
</head>
<body>
    <h1>🏨 SmartStay — Панель менеджера</h1>
    <p class="subtitle">Все запросы гостей в реальном времени</p>
    <button class="refresh" onclick="location.reload()">🔄 Обновить</button>
    <div class="stats" id="stats"></div>
    <table>
        <thead>
            <tr>
                <th>Номер</th>
                <th>Кто</th>
                <th>Сообщение</th>
                <th>Время</th>
            </tr>
        </thead>
        <tbody id="tbody"></tbody>
    </table>
    <script>
        fetch('/api/messages')
            .then(r => r.json())
            .then(data => {
                const rooms = new Set(data.map(m => m.room)).size;
                const userMsgs = data.filter(m => m.role === 'user').length;
                document.getElementById('stats').innerHTML = `
                    <div class="stat"><div class="num">${data.length}</div><div class="label">Всего сообщений</div></div>
                    <div class="stat"><div class="num">${rooms}</div><div class="label">Активных номеров</div></div>
                    <div class="stat"><div class="num">${userMsgs}</div><div class="label">Запросов гостей</div></div>
                `;
                document.getElementById('tbody').innerHTML = data.map(m => `
                    <tr>
                        <td><span class="room-tag">🚪 ${m.room}</span></td>
                        <td class="${m.role === 'user' ? 'role-user' : 'role-bot'}">${m.role === 'user' ? '👤 Гость' : '🤖 AI'}</td>
                        <td>${m.message}</td>
                        <td>${m.created_at}</td>
                    </tr>
                `).join('');
            });
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
    return [{"room": r[0], "role": r[1], "message": r[2], "created_at": r[3]} for r in rows]

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
            system=HOTEL_INFO,
            messages=history
        ) as stream:
            for text in stream.text_stream:
                full_response.append(text)
                yield f"data: {json.dumps({'text': text})}\n\n"
        save_message(room, "bot", "".join(full_response))
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")