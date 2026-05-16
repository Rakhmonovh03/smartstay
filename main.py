from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime
import json, os, sqlite3

load_dotenv()


TELEGRAM_TOKEN = "8644783291:AAFdATLmPL3vityqTyvSfhLi0yRMDwbl8Oc"
TELEGRAM_CHAT_ID = "916372970"

async def send_telegram(message: str):
    try:
        import urllib.request
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"Telegram error: {e}")


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

def init_db():
    conn = sqlite3.connect("smartstay.db")
    
    # Таблица отелей
    conn.execute("""
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE,
            name TEXT,
            password TEXT,
            info TEXT,
            created_at TEXT
        )
    """)
    
    # Таблица сообщений
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_slug TEXT,
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

def create_hotel(slug, name, password, info):
    conn = sqlite3.connect("smartstay.db")
    conn.execute(
        "INSERT INTO hotels (slug, name, password, info, created_at) VALUES (?, ?, ?, ?, ?)",
        (slug, name, password, info, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()

def get_hotel(slug):
    conn = sqlite3.connect("smartstay.db")
    row = conn.execute(
        "SELECT slug, name, password, info FROM hotels WHERE slug=?", (slug,)
    ).fetchone()
    conn.close()
    if row:
        return {"slug": row[0], "name": row[1], "password": row[2], "info": row[3]}
    return None

def get_all_hotels():
    conn = sqlite3.connect("smartstay.db")
    rows = conn.execute(
        "SELECT slug, name, created_at FROM hotels ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [{"slug": r[0], "name": r[1], "created_at": r[2]} for r in rows]

def get_hotel_messages(slug):
    conn = sqlite3.connect("smartstay.db")
    rows = conn.execute(
        """SELECT room, role, message, created_at, priority, is_read 
        FROM messages WHERE hotel_slug=?
        ORDER BY CASE priority WHEN 'urgent' THEN 0 ELSE 1 END, id DESC LIMIT 100""",
        (slug,)
    ).fetchall()
    conn.close()
    return rows

def save_hotel_message(slug, room, role, message):
    priority = get_priority(message) if role == "user" else "normal"
    conn = sqlite3.connect("smartstay.db")
    conn.execute(
        "INSERT INTO messages (hotel_slug, room, role, message, created_at, priority, is_read) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (slug, room, role, message, datetime.now().strftime("%Y-%m-%d %H:%M"), priority, 0)
    )
    conn.commit()
    conn.close()
    return priority

def mark_hotel_read(slug):
    conn = sqlite3.connect("smartstay.db")
    conn.execute("UPDATE messages SET is_read=1 WHERE hotel_slug=?", (slug,))
    conn.commit()
    conn.close()


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

            const slug = window.location.pathname.split('/')[2] || '';
            const chatUrl = slug ? '/hotel/' + slug + '/chat' : '/chat';
            const res = await fetch(chatUrl, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text, history: messages.slice(0,-1), room: room, slug: slug})
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


EDIT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartStay — Настройки</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:sans-serif; background:#0a0a0a; color:white; min-height:100vh; display:flex; align-items:center; justify-content:center; padding:40px 20px; }
        .box { background:#1a1a1a; border-radius:16px; padding:48px; width:100%; max-width:560px; }
        .logo { color:#C9A84C; font-size:22px; font-weight:900; margin-bottom:4px; }
        .sub { color:#666; font-size:14px; margin-bottom:32px; }
        .field { margin-bottom:20px; }
        label { display:block; font-size:13px; color:#888; margin-bottom:8px; letter-spacing:1px; }
        input, textarea { width:100%; background:#2a2a2a; border:1px solid #333; border-radius:8px; padding:14px; color:white; font-size:14px; outline:none; font-family:sans-serif; }
        input:focus, textarea:focus { border-color:#C9A84C; }
        textarea { height:300px; resize:vertical; }
        .btns { display:flex; gap:12px; margin-top:8px; }
        .btn { flex:1; padding:14px; border:none; border-radius:8px; font-size:14px; font-weight:600; cursor:pointer; }
        .btn-gold { background:#C9A84C; color:#000; }
        .btn-dark { background:#2a2a2a; color:#fff; border:1px solid #333; }
        .success { color:#4CAF50; font-size:13px; margin-top:12px; display:none; }
        .error { color:#E05555; font-size:13px; margin-top:12px; display:none; }
        .back { color:#C9A84C; font-size:13px; text-decoration:none; display:inline-block; margin-bottom:24px; }
    </style>
</head>
<body>
    <div class="box">
        <a class="back" href="javascript:history.back()">← Panele dön</a>
        <div class="logo">🏨 SmartStay AI</div>
        <div class="sub">Otel bilgilerini düzenle</div>

        <div class="field">
            <label>OTELİN ADI</label>
            <input type="text" id="name" placeholder="Otel adı">
        </div>

        <div class="field">
            <label>OTEL BİLGİLERİ</label>
            <textarea id="info" placeholder="Otel bilgileri..."></textarea>
        </div>

        <div class="field">
            <label>YENİ ŞİFRE (değiştirmek istemiyorsanız boş bırakın)</label>
            <input type="password" id="password" placeholder="Yeni şifre">
        </div>

        <div class="btns">
            <button class="btn btn-gold" onclick="save()">💾 Kaydet</button>
            <button class="btn btn-dark" onclick="window.location.href=dashUrl">📊 Panele Git</button>
        </div>
        <div class="success" id="success">✅ Kaydedildi!</div>
        <div class="error" id="error"></div>
    </div>

    <script>
        const slug = window.location.pathname.split('/')[2];
        const dashUrl = '/hotel/' + slug + '/dashboard';

        fetch('/api/hotel/' + slug + '/info')
            .then(r => r.json())
            .then(data => {
                document.getElementById('name').value = data.name || '';
                document.getElementById('info').value = data.info || '';
            });

        async function save() {
            const name = document.getElementById('name').value.trim();
            const info = document.getElementById('info').value.trim();
            const password = document.getElementById('password').value.trim();

            const res = await fetch('/api/hotel/' + slug + '/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name, info, password})
            });

            const data = await res.json();
            if (data.ok) {
                document.getElementById('success').style.display = 'block';
                setTimeout(() => document.getElementById('success').style.display = 'none', 3000);
            } else {
                document.getElementById('error').textContent = '❌ ' + data.error;
                document.getElementById('error').style.display = 'block';
            }
        }
    </script>
</body>
</html>
"""



MANAGER_PASSWORD = "smartstay2025"

REGISTER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartStay — Регистрация отеля</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:sans-serif; background:#0a0a0a; color:white; min-height:100vh; display:flex; align-items:center; justify-content:center; padding:40px 20px; }
        .box { background:#1a1a1a; border-radius:16px; padding:48px; width:100%; max-width:560px; }
        .logo { color:#C9A84C; font-size:24px; font-weight:900; margin-bottom:8px; }
        .sub { color:#666; font-size:14px; margin-bottom:40px; }
        .field { margin-bottom:20px; }
        label { display:block; font-size:13px; color:#888; margin-bottom:8px; letter-spacing:1px; }
        input, textarea { width:100%; background:#2a2a2a; border:1px solid #333; border-radius:8px; padding:14px; color:white; font-size:14px; outline:none; font-family:sans-serif; }
        input:focus, textarea:focus { border-color:#C9A84C; }
        textarea { height:200px; resize:vertical; }
        .hint { font-size:12px; color:#555; margin-top:6px; }
        .btn { width:100%; background:#C9A84C; color:#000; border:none; border-radius:8px; padding:16px; font-size:15px; font-weight:600; cursor:pointer; margin-top:8px; }
        .btn:hover { background:#E8C96A; }
        .error { color:#E05555; font-size:13px; margin-top:12px; display:none; }
        .success { display:none; text-align:center; padding:32px; }
        .success h2 { color:#C9A84C; font-size:24px; margin-bottom:16px; }
        .success p { color:#888; font-size:14px; margin-bottom:24px; line-height:1.7; }
        .link-box { background:#2a2a2a; border:1px solid rgba(201,168,76,0.3); padding:14px; border-radius:8px; color:#C9A84C; font-size:13px; word-break:break-all; }
    </style>
</head>
<body>
    <div class="box">
        <div id="form-view">
            <div class="logo">🏨 SmartStay AI</div>
            <div class="sub">Otelinizi sisteme kaydedin — 2 dakikada hazır</div>

            <div class="field">
                <label>OTELİN ADI</label>
                <input type="text" id="name" placeholder="Örn: Rixos Premium Belek">
            </div>

            <div class="field">
                <label>OTELİN KISALTMASI (URL için)</label>
                <input type="text" id="slug" placeholder="Örn: rixos-premium">
                <div class="hint">Sadece küçük harf ve tire kullanın. Örn: grand-hotel, sunrise-resort</div>
            </div>

            <div class="field">
                <label>YÖNETİCİ ŞİFRESİ</label>
                <input type="password" id="password" placeholder="Güvenli bir şifre girin">
            </div>

            <div class="field">
                <label>OTELİN BİLGİLERİ</label>
                <textarea id="info" placeholder="Otelin bilgilerini yazın:
- Havuz saatleri
- Restoran saatleri  
- Spa saatleri
- Önemli telefon numaraları
- Diğer hizmetler

Bu bilgileri AI misafir sorularını yanıtlamak için kullanacak."></textarea>
                <div class="hint">Ne kadar detaylı yazarsanız AI o kadar iyi yanıt verir</div>
            </div>

            <button class="btn" onclick="register()">Oteli Kaydet →</button>
            <div class="error" id="err"></div>
        </div>

        <div class="success" id="success-view">
            <h2>✅ Otel Kaydedildi!</h2>
            <p>Sisteminiz hazır. Aşağıdaki linkleri kaydedin:</p>
            <p style="color:#888; margin-bottom:8px; font-size:13px;">👤 Misafir linki:</p>
            <div class="link-box" id="guest-link"></div>
            <br>
            <p style="color:#888; margin-bottom:8px; font-size:13px;">📊 Yönetici paneli:</p>
            <div class="link-box" id="manager-link"></div>
            <br><br>
            <button class="btn" onclick="window.location.href=document.getElementById('manager-link').textContent">Panele Git →</button>
        </div>
    </div>

    <script>
        document.getElementById('name').addEventListener('input', function() {
            const slug = this.value.toLowerCase()
                .replace(/[^a-z0-9\\s-]/g, '')
                .replace(/\\s+/g, '-')
                .replace(/-+/g, '-');
            document.getElementById('slug').value = slug;
        });

        async function register() {
            const name = document.getElementById('name').value.trim();
            const slug = document.getElementById('slug').value.trim();
            const password = document.getElementById('password').value.trim();
            const info = document.getElementById('info').value.trim();
            const err = document.getElementById('err');

            if (!name || !slug || !password || !info) {
                err.textContent = '❌ Lütfen tüm alanları doldurun';
                err.style.display = 'block';
                return;
            }

            const res = await fetch('/api/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name, slug, password, info})
            });

            const data = await res.json();

            if (data.ok) {
                const base = window.location.origin;
                document.getElementById('guest-link').textContent = base + '/hotel/' + slug;
                document.getElementById('manager-link').textContent = base + '/hotel/' + slug + '/dashboard';
                document.getElementById('form-view').style.display = 'none';
                document.getElementById('success-view').style.display = 'block';
            } else {
                err.textContent = '❌ ' + (data.error || 'Hata oluştu');
                err.style.display = 'block';
            }
        }
    </script>
</body>
</html>
"""

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartStay — Вход</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:sans-serif; background:#0a0a0a; color:white; height:100vh; display:flex; align-items:center; justify-content:center; }
        .box { background:#1a1a1a; border-radius:16px; padding:48px; width:360px; text-align:center; }
        .logo { color:#C9A84C; font-size:28px; font-weight:900; margin-bottom:8px; }
        .sub { color:#666; font-size:14px; margin-bottom:32px; }
        input { width:100%; background:#2a2a2a; border:1px solid #333; border-radius:8px; padding:14px; color:white; font-size:15px; outline:none; margin-bottom:16px; text-align:center; }
        input:focus { border-color:#C9A84C; }
        button { width:100%; background:#C9A84C; color:#000; border:none; border-radius:8px; padding:14px; font-size:15px; font-weight:600; cursor:pointer; }
        button:hover { background:#E8C96A; }
        .error { color:#E05555; font-size:13px; margin-top:12px; display:none; }
    </style>
</head>
<body>
    <div class="box">
        <div class="logo">🏨 SmartStay</div>
        <div class="sub">Панель менеджера</div>
        <input type="password" id="pwd" placeholder="Введите пароль" onkeypress="if(event.key==='Enter') login()">
        <button onclick="login()">Войти</button>
        <div class="error" id="err">❌ Неверный пароль</div>
    </div>
    <script>
        function login() {
            const pwd = document.getElementById('pwd').value;
            const slug = window.location.pathname.split('/')[2] || '';
            const loginUrl = slug ? '/api/hotel-login' : '/api/login';
            const body = slug ? {password: pwd, slug: slug} : {password: pwd};
            fetch(loginUrl, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(body)
            })
            .then(r => r.json())
            .then(data => {
                if (data.ok) {
                    window.location.href = slug ? '/hotel/' + slug + '/dashboard' : '/dashboard';
                } else {
                    document.getElementById('err').style.display = 'block';
                }
            });
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
        @keyframes slideIn {
            from { transform:translateX(100px); opacity:0; }
            to { transform:translateX(0); opacity:1; }
        }
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
        <button class="btn btn-dark" onclick="goToEdit()">⚙️ Настройки</button>
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
                    checkUrgentSound(data);       
                });
        }, 3000);

        // Звуковое уведомление
        let lastUrgentCount = 0;
        function checkUrgentSound(data) {
            const urgentCount = data.filter(m => m.priority === 'urgent' && m.is_read === 0).length;
            if (urgentCount > lastUrgentCount) {
                playAlert();
                showPopup(data.find(m => m.priority === 'urgent' && m.is_read === 0));
            }
            lastUrgentCount = urgentCount;
        }

        function playAlert() {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            [0, 0.3, 0.6].forEach(delay => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.frequency.value = 880;
                osc.type = 'sine';
                gain.gain.setValueAtTime(0.3, ctx.currentTime + delay);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + delay + 0.3);
                osc.start(ctx.currentTime + delay);
                osc.stop(ctx.currentTime + delay + 0.3);
            });
        }

        function showPopup(msg) {
            if (!msg) return;
            const popup = document.createElement('div');
            popup.style.cssText = `
                position:fixed; top:20px; right:20px; z-index:9999;
                background:#E05555; color:white; padding:20px 24px;
                border-radius:12px; font-size:15px; font-weight:500;
                box-shadow:0 8px 32px rgba(224,85,85,0.4);
                animation:slideIn 0.3s ease;
                max-width:320px; line-height:1.5;
            `;
            popup.innerHTML = `
                🔴 <b>СРОЧНЫЙ ЗАПРОС!</b><br>
                🚪 Номер ${msg.room}<br>
                💬 ${msg.message}
                <br><br>
                <small style="opacity:0.8">Нажмите чтобы закрыть</small>
            `;
            popup.onclick = () => popup.remove();
            document.body.appendChild(popup);
            setTimeout(() => popup.remove(), 8000);
        }

        function goToEdit() {
            const slug = window.location.pathname.split('/')[2] || '';
            if (slug) window.location.href = '/hotel/' + slug + '/edit';
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return CHAT_HTML

from fastapi import Request, Response as FastAPIResponse
from fastapi.responses import RedirectResponse

@app.get("/register", response_class=HTMLResponse)
def register_page():
    return REGISTER_HTML

@app.post("/api/register")
def api_register(data: dict):
    slug = data.get("slug", "").strip()
    name = data.get("name", "").strip()
    password = data.get("password", "").strip()
    info = data.get("info", "").strip()

    if not all([slug, name, password, info]):
        return {"ok": False, "error": "Tüm alanlar gerekli"}

    if get_hotel(slug):
        return {"ok": False, "error": "Bu isim zaten kullanılıyor"}

    create_hotel(slug, name, password, info)
    return {"ok": True, "slug": slug}

@app.get("/hotel/{slug}", response_class=HTMLResponse)
def hotel_chat(slug: str):
    hotel = get_hotel(slug)
    if not hotel:
        return HTMLResponse("<h1 style='color:white;background:#0a0a0a;padding:40px;font-family:sans-serif'>❌ Otel bulunamadı</h1>", status_code=404)
    return CHAT_HTML.replace("SmartStay AI", hotel["name"]).replace("SmartStay Resort 5*", hotel["name"])

@app.get("/hotel/{slug}/dashboard", response_class=HTMLResponse)
def hotel_dashboard(slug: str, request: Request):
    hotel = get_hotel(slug)
    if not hotel:
        return HTMLResponse("<h1 style='color:white;background:#0a0a0a;padding:40px;font-family:sans-serif'>❌ Otel bulunamadı</h1>", status_code=404)
    if request.cookies.get(f"auth_{slug}") != "yes":
        return RedirectResponse(f"/hotel/{slug}/login")
    return DASHBOARD_HTML.replace("SmartStay — Панель менеджера", hotel["name"] + " — Панель менеджера")

@app.get("/hotel/{slug}/login", response_class=HTMLResponse)
def hotel_login_page(slug: str):
    hotel = get_hotel(slug)
    if not hotel:
        return HTMLResponse("❌ Otel bulunamadı", status_code=404)
    return LOGIN_HTML.replace("SmartStay", hotel["name"])

@app.post("/api/hotel-login")
def api_hotel_login(data: dict, response: FastAPIResponse):
    slug = data.get("slug", "")
    password = data.get("password", "")
    hotel = get_hotel(slug)
    if hotel and hotel["password"] == password:
        response.set_cookie(f"auth_{slug}", "yes", max_age=86400)
        return {"ok": True}
    return {"ok": False}

@app.get("/api/hotel/{slug}/messages")
def hotel_messages(slug: str, request: Request):
    rows = get_hotel_messages(slug)
    return [{"room": r[0], "role": r[1], "message": r[2], "created_at": r[3], "priority": r[4], "is_read": r[5]} for r in rows]

@app.post("/api/hotel/{slug}/mark-read")
def hotel_mark_read(slug: str):
    mark_hotel_read(slug)
    return {"status": "ok"}

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
        hotel = get_hotel(slug)
        import asyncio
        asyncio.create_task(send_telegram(
            f"🔴 <b>СРОЧНО!</b>\n"
            f"🏨 Отель: {hotel['name']}\n"
            f"🚪 Номер: {room}\n"
            f"💬 Сообщение: {message}\n"
            f"⏰ Время: {datetime.now().strftime('%H:%M')}"
        ))
    history.append({"role": "user", "content": message})

    system = hotel["info"] + f"\n\nОтель: {hotel['name']}\nГость в номере: {room}. Не спрашивай номер снова.\nОтвечай на языке гостя."

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
    cards = ""
    for room in rooms:
        cards += f"""
        <div class="card">
            <img src="/hotel/{slug}/qr/{room}" alt="QR {room}">
            <div class="room">🚪 {room}</div>
            <div class="hint">Skaniruy dlya pomoshchi</div>
        </div>"""
    return f"""<!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>QR — {hotel['name']}</title>
    <style>
        * {{margin:0;padding:0;box-sizing:border-box;}}
        body {{background:#0a0a0a;color:white;font-family:sans-serif;padding:40px;}}
        h1 {{color:#C9A84C;font-size:28px;margin-bottom:8px;}}
        p {{color:#666;margin-bottom:32px;font-size:14px;}}
        .grid {{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:20px;}}
        .card {{background:#1a1a1a;border-radius:12px;padding:24px;text-align:center;border:1px solid #333;}}
        .card img {{width:140px;height:140px;border-radius:8px;}}
        .room {{font-size:16px;font-weight:700;color:#C9A84C;margin-top:12px;}}
        .hint {{font-size:12px;color:#666;margin-top:4px;}}
        .btn {{background:#C9A84C;color:#000;border:none;padding:12px 32px;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;margin-bottom:32px;}}
    </style></head>
    <body>
        <h1>🏨 {hotel['name']} — QR Kodlar</h1>
        <p>Распечатай и повесь в каждый номер.</p>
        <button class="btn" onclick="window.print()">🖨️ Распечатать</button>
        <div class="grid">{cards}</div>
    </body></html>"""


@app.get("/login", response_class=HTMLResponse)
def login_page():
    return LOGIN_HTML

@app.post("/api/login")
def api_login(data: dict, response: FastAPIResponse):
    if data.get("password") == MANAGER_PASSWORD:
        response.set_cookie("manager_auth", "yes", max_age=86400)
        return {"ok": True}
    return {"ok": False}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if request.cookies.get("manager_auth") != "yes":
        return RedirectResponse("/login")
    return DASHBOARD_HTML

@app.get("/api/logout")
def logout(response: FastAPIResponse):
    response.delete_cookie("manager_auth")
    return RedirectResponse("/login")

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


def update_hotel(slug, name, info, password=None):
    conn = sqlite3.connect("smartstay.db")
    if password:
        conn.execute(
            "UPDATE hotels SET name=?, info=?, password=? WHERE slug=?",
            (name, info, password, slug)
        )
    else:
        conn.execute(
            "UPDATE hotels SET name=?, info=? WHERE slug=?",
            (name, info, slug)
        )
    conn.commit()
    conn.close()

@app.get("/hotel/{slug}/edit", response_class=HTMLResponse)
def hotel_edit(slug: str, request: Request):
    hotel = get_hotel(slug)
    if not hotel:
        return HTMLResponse("❌ Otel bulunamadı", status_code=404)
    if request.cookies.get(f"auth_{slug}") != "yes":
        return RedirectResponse(f"/hotel/{slug}/login")
    return EDIT_HTML

@app.get("/api/hotel/{slug}/info")
def hotel_info(slug: str, request: Request):
    hotel = get_hotel(slug)
    if not hotel:
        return {"error": "Not found"}
    return {"name": hotel["name"], "info": hotel["info"]}

@app.post("/api/hotel/{slug}/update")
def hotel_update(slug: str, data: dict, request: Request):
    if request.cookies.get(f"auth_{slug}") != "yes":
        return {"ok": False, "error": "Unauthorized"}
    name = data.get("name", "").strip()
    info = data.get("info", "").strip()
    password = data.get("password", "").strip()
    if not name or not info:
        return {"ok": False, "error": "Ad ve bilgiler gerekli"}
    update_hotel(slug, name, info, password if password else None)
    return {"ok": True}




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