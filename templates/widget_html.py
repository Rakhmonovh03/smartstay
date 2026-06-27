def get_widget_html(hotel_name="SmartStay", hotel_slug="", ai_name="AI Asistan"):
    import html as _html
    hotel_name = _html.escape(hotel_name or "SmartStay")   # hotel-controlled → escape
    ai_name = _html.escape(ai_name or "AI Asistan")
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{hotel_name}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: #141414; color: #f0f0f0;
    height: 100vh; display: flex; flex-direction: column;
    overflow: hidden;
  }}
  /* HEADER */
  .wh {{
    background: linear-gradient(135deg, #C9A84C, #E8C96A);
    padding: 12px 16px; display: flex; align-items: center; gap: 10px;
    flex-shrink: 0;
  }}
  .wh-icon {{
    width: 34px; height: 34px; border-radius: 50%;
    background: rgba(0,0,0,0.15); display: flex;
    align-items: center; justify-content: center; font-size: 18px;
  }}
  .wh-text h3 {{ font-size: 14px; font-weight: 700; color: #1a1a1a; line-height: 1.2; }}
  .wh-text p {{ font-size: 11px; color: rgba(0,0,0,0.5); }}
  .wh-dot {{
    width: 7px; height: 7px; border-radius: 50%; background: #2ecc71;
    margin-right: 4px; display: inline-block;
    animation: pulse 2s infinite;
  }}
  @keyframes pulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(46,204,113,0.5); }}
    70% {{ box-shadow: 0 0 0 5px rgba(46,204,113,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(46,204,113,0); }}
  }}
  /* MESSAGES */
  .msgs {{
    flex: 1; overflow-y: auto; padding: 12px;
    display: flex; flex-direction: column; gap: 10px;
  }}
  .msgs::-webkit-scrollbar {{ width: 3px; }}
  .msgs::-webkit-scrollbar-thumb {{ background: rgba(201,168,76,0.2); border-radius: 10px; }}
  .row {{ display: flex; gap: 6px; align-items: flex-end; }}
  .row.user {{ flex-direction: row-reverse; }}
  .av {{
    width: 24px; height: 24px; border-radius: 50%; flex-shrink: 0;
    background: rgba(201,168,76,0.1); display: flex;
    align-items: center; justify-content: center; font-size: 12px;
  }}
  .row.user .av {{ display: none; }}
  .bubble {{
    max-width: 78%; padding: 9px 13px; border-radius: 16px;
    font-size: 13px; line-height: 1.5; word-wrap: break-word;
  }}
  .bot .bubble {{ background: #222; color: #eee; border-bottom-left-radius: 4px; }}
  .user .bubble {{
    background: linear-gradient(135deg, #C9A84C, #E8C96A);
    color: #1a1a1a; font-weight: 500; border-bottom-right-radius: 4px;
  }}
  .staff .bubble {{
    background: rgba(76,175,80,0.1); color: #6fd46f;
    border: 1px solid rgba(76,175,80,0.2); border-bottom-left-radius: 4px;
  }}
  .typing {{ display: flex; gap: 4px; padding: 2px 0; }}
  .typing span {{
    width: 6px; height: 6px; border-radius: 50%; background: #C9A84C;
    animation: bounce 1.2s infinite;
  }}
  .typing span:nth-child(2) {{ animation-delay: 0.2s; }}
  .typing span:nth-child(3) {{ animation-delay: 0.4s; }}
  @keyframes bounce {{
    0%,60%,100% {{ transform: translateY(0); opacity: 0.4; }}
    30% {{ transform: translateY(-5px); opacity: 1; }}
  }}
  /* INPUT */
  .inp-area {{
    padding: 10px 12px; display: flex; gap: 8px;
    border-top: 1px solid rgba(255,255,255,0.06); flex-shrink: 0;
    background: #141414;
  }}
  .inp-area input {{
    flex: 1; background: #1f1f1f; border: 1px solid transparent;
    border-radius: 20px; padding: 10px 14px; color: #fff;
    font-size: 13px; outline: none; font-family: inherit;
    transition: border-color 0.2s;
  }}
  .inp-area input:focus {{ border-color: rgba(201,168,76,0.4); }}
  .inp-area input::placeholder {{ color: #555; }}
  .send {{
    width: 38px; height: 38px; flex-shrink: 0;
    background: linear-gradient(135deg, #C9A84C, #E8C96A);
    border: none; border-radius: 50%; cursor: pointer;
    font-size: 15px; color: #1a1a1a;
    display: flex; align-items: center; justify-content: center;
    transition: transform 0.15s;
  }}
  .send:hover {{ transform: scale(1.08); }}
  /* Powered by */
  .powered {{
    text-align: center; font-size: 10px; color: #333;
    padding: 4px 0 6px; flex-shrink: 0;
  }}
  .powered a {{ color: #C9A84C; text-decoration: none; }}
</style>
</head>
<body>
<div class="wh">
  <div class="wh-icon">🤖</div>
  <div class="wh-text">
    <h3>{ai_name}</h3>
    <p><span class="wh-dot"></span>Онлайн • Online</p>
  </div>
</div>

<div class="msgs" id="msgs"></div>

<div class="inp-area">
  <input type="text" id="inp" placeholder="Напишите сообщение..."
         onkeypress="if(event.key==='Enter') send()">
  <button class="send" onclick="send()">➤</button>
</div>
<div class="powered">Powered by <a href="https://smartstay.ai" target="_blank">SmartStay AI</a></div>

<script>
  const slug = '{hotel_slug}';
  const params = new URLSearchParams(window.location.search);
  const room = params.get('room') || ('w-' + Math.random().toString(36).slice(2,8));
  let history = [];
  let streaming = false;
  let lastId = 0;

  function addMsg(text, role, isStaff) {{
    const row = document.createElement('div');
    const cls = isStaff ? 'staff' : role;
    row.className = 'row ' + cls;
    const av = role !== 'user'
      ? '<div class="av">' + (isStaff ? '👨‍💼' : '🤖') + '</div>' : '';
    const bub = document.createElement('div');
    bub.className = 'bubble';
    bub.textContent = text;
    row.innerHTML = av;
    row.appendChild(bub);
    document.getElementById('msgs').appendChild(row);
    scroll();
    return bub;
  }}

  function scroll() {{
    const el = document.getElementById('msgs');
    el.scrollTop = el.scrollHeight;
  }}

  async function send() {{
    if (streaming) return;
    const inp = document.getElementById('inp');
    const text = inp.value.trim();
    if (!text) return;
    inp.value = '';
    inp.disabled = true;
    streaming = true;
    addMsg(text, 'user');
    history.push({{role:'user', content:text}});

    const row = document.createElement('div');
    row.className = 'row bot';
    row.innerHTML = '<div class="av">🤖</div>';
    const bub = document.createElement('div');
    bub.className = 'bubble';
    bub.innerHTML = '<div class="typing"><span></span><span></span><span></span></div>';
    row.appendChild(bub);
    document.getElementById('msgs').appendChild(row);
    scroll();

    const url = slug ? '/hotel/' + slug + '/chat' : '/chat';
    try {{
      const res = await fetch(url, {{
        method:'POST',
        headers:{{'Content-Type':'application/json'}},
        body: JSON.stringify({{message:text, history:history.slice(0,-1), room}})
      }});
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let full = ''; let first = true;
      let buf = '';   // holds a partial line across chunk boundaries
      while (true) {{
        const {{done, value}} = await reader.read();
        if (done) break;
        buf += dec.decode(value, {{stream: true}});
        const lines = buf.split('\\n');
        buf = lines.pop();   // keep the last (possibly incomplete) line
        for (const line of lines) {{
          if (!line.startsWith('data: ')) continue;
          try {{
            const d = JSON.parse(line.slice(6));
            if (d.text) {{ if(first){{bub.textContent='';first=false;}} full+=d.text; bub.textContent=full; scroll(); }}
            if (d.error) {{ bub.textContent='⚠️ '+d.error; bub.style.color='#E05555'; }}
          }} catch(e) {{}}
        }}
      }}
      if (full) history.push({{role:'assistant', content:full}});
    }} catch(e) {{ bub.textContent='⚠️ Ошибка соединения'; }}
    streaming = false;
    inp.disabled = false;
    inp.focus();
  }}

  // Poll for staff replies
  async function poll() {{
    if (!slug) return;  // poll even when lastId is 0 (since_id=0 → fetch from start)
    try {{
      const r = await fetch('/api/hotel/'+slug+'/room/'+room+'/new-messages?since_id='+lastId);
      const msgs = await r.json();
      msgs.forEach(m => {{
        if (m.role === 'staff') {{
          addMsg(m.message, 'bot', true);
          lastId = Math.max(lastId, m.id);
        }}
      }});
    }} catch(e) {{}}
  }}

  // Init: welcome message
  (async () => {{
    if (!slug) {{
      addMsg('Добро пожаловать! 👋 Чем могу помочь?', 'bot');
      return;
    }}
    try {{
      const r = await fetch('/api/hotel/'+slug+'/room/'+encodeURIComponent(room)+'/welcome', {{method:'POST'}});
      const d = await r.json();
      if (d.message) {{ addMsg(d.message, 'bot'); return; }}
    }} catch(e) {{}}
    addMsg('Здравствуйте! 👋 Чем могу помочь?\\nHello! How can I help?', 'bot');
  }})();

  if (slug) setInterval(poll, 5000);
</script>
</body>
</html>"""
