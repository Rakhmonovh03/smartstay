def get_chat_html(hotel_name="SmartStay AI"):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{hotel_name}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: sans-serif; background:#0a0a0a; color:white; height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
        .chat-box {{ width:380px; background:#1a1a1a; border-radius:16px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,0.5); }}
        .chat-header {{ background:#C9A84C; padding:20px; text-align:center; }}
        .chat-header h2 {{ font-size:18px; color:#000; }}
        .chat-header p {{ font-size:12px; color:#333; margin-top:4px; }}
        .room-bar {{ background:#111; padding:10px 20px; font-size:13px; color:#C9A84C; text-align:center; }}
        .messages {{ height:380px; overflow-y:auto; padding:20px; display:flex; flex-direction:column; gap:12px; }}
        .msg {{ padding:12px 16px; border-radius:12px; max-width:85%; font-size:14px; line-height:1.5; }}
        .bot {{ background:#2a2a2a; align-self:flex-start; }}
        .user {{ background:#C9A84C; color:#000; align-self:flex-end; }}
        .input-area {{ padding:16px; display:flex; gap:8px; border-top:1px solid #333; }}
        input {{ flex:1; background:#2a2a2a; border:none; border-radius:8px; padding:12px; color:white; font-size:14px; outline:none; }}
        button {{ background:#C9A84C; border:none; border-radius:8px; padding:12px 16px; cursor:pointer; font-size:18px; }}
        .theme-btn {{ position:absolute; top:16px; right:16px; background:rgba(0,0,0,0.2); border:none; border-radius:20px; padding:6px 12px; cursor:pointer; font-size:12px; color:#000; }}
        body.light {{ background:#f5f5f5; }}
        body.light .chat-box {{ background:#fff; box-shadow:0 20px 60px rgba(0,0,0,0.15); }}
        body.light .messages {{ background:#fff; }}
        body.light .bot {{ background:#f0f0f0; color:#000; }}
        body.light .room-bar {{ background:#f9f9f9; }}
        body.light .input-area {{ border-top:1px solid #eee; background:#fff; }}
        body.light input {{ background:#f0f0f0; color:#000; }}
        body.light input::placeholder {{ color:#999; }}
    </style>
</head>
<body>
    <div class="chat-box">
        <div class="chat-header" style="position:relative">
            <h2>🏨 {hotel_name}</h2>
            <p>Консьерж • Concierge • Konsiyerj</p>
            <button class="theme-btn" onclick="toggleTheme()" id="themeBtn">☀️ Light</button>
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

        async function send() {{
            const input = document.getElementById('input');
            const text = input.value.trim();
            if (!text) return;

            addMessage(text, 'user');
            messages.push({{role: 'user', content: text}});
            input.value = '';
            input.disabled = true;

            const botDiv = document.createElement('div');
            botDiv.className = 'msg bot';
            botDiv.textContent = '...';
            document.getElementById('messages').appendChild(botDiv);

            const slug = window.location.pathname.split('/')[2] || '';
            const chatUrl = slug ? '/hotel/' + slug + '/chat' : '/chat';
            const res = await fetch(chatUrl, {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{message: text, history: messages.slice(0,-1), room: room, slug: slug}})
            }});

            const reader = res.body.getReader();
            const decoder = new TextDecoder();
            let fullText = '';

            while (true) {{
                const {{done, value}} = await reader.read();
                if (done) break;
                const lines = decoder.decode(value).split('\\n');
                for (const line of lines) {{
                    if (line.startsWith('data: ') && line !== 'data: [DONE]') {{
                        try {{
                            const data = JSON.parse(line.slice(6));
                            fullText += data.text;
                            botDiv.textContent = fullText;
                            document.getElementById('messages').scrollTop = 99999;
                        }} catch(e) {{}}
                    }}
                }}
            }}
            messages.push({{role: 'assistant', content: fullText}});
            input.disabled = false;
            input.focus();
        }}

        function toggleTheme() {{
            document.body.classList.toggle('light');
            const btn = document.getElementById('themeBtn');
            if (document.body.classList.contains('light')) {{
                btn.textContent = '🌙 Dark';
                localStorage.setItem('theme', 'light');
            }} else {{
                btn.textContent = '☀️ Light';
                localStorage.setItem('theme', 'dark');
            }}
        }}

        // Load saved theme
        if (localStorage.getItem('theme') === 'light') {{
            document.body.classList.add('light');
            document.getElementById('themeBtn').textContent = '🌙 Dark';
        }}

        function addMessage(text, type) {{
            const div = document.createElement('div');
            div.className = 'msg ' + (type === 'user' ? 'user' : 'bot');
            div.textContent = text;
            document.getElementById('messages').appendChild(div);
            document.getElementById('messages').scrollTop = 99999;
        }}
    </script>
</body>
</html>
"""