LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartStay — Giriş</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:sans-serif; background:#0a0a0a; color:white; height:100vh; display:flex; align-items:center; justify-content:center; }
        .box { background:#111; border-radius:16px; padding:48px; width:360px; text-align:center; border:1px solid rgba(201,168,76,0.15); }
        .logo { color:#C9A84C; font-size:26px; font-weight:900; margin-bottom:8px; }
        .sub { color:#555; font-size:14px; margin-bottom:32px; }
        input { width:100%; background:#1a1a1a; border:1px solid #333; border-radius:8px; padding:14px; color:white; font-size:15px; outline:none; margin-bottom:16px; text-align:center; }
        input:focus { border-color:#C9A84C; }
        button { width:100%; background:#C9A84C; color:#000; border:none; border-radius:8px; padding:14px; font-size:15px; font-weight:600; cursor:pointer; }
        button:hover { background:#E8C96A; }
        .error { color:#E05555; font-size:13px; margin-top:12px; display:none; }
    </style>
</head>
<body>
    <div class="box">
        <div class="logo">🏨 HOTEL_NAME_PLACEHOLDER</div>
        <div class="sub">Yönetici Paneli</div>
        <input type="password" id="pwd" placeholder="Şifrenizi girin" onkeypress="if(event.key==='Enter') login()">
        <button onclick="login()">Giriş Yap</button>
        <div class="error" id="err">❌ Yanlış şifre</div>
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
                credentials: 'include',
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

REGISTER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartStay — Otel Kayıt</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:sans-serif; background:#0a0a0a; color:white; min-height:100vh; display:flex; align-items:center; justify-content:center; padding:40px 20px; }
        .box { background:#111; border-radius:16px; padding:48px; width:100%; max-width:600px; border:1px solid rgba(201,168,76,0.15); }
        .logo { color:#C9A84C; font-size:24px; font-weight:900; margin-bottom:4px; }
        .sub { color:#555; font-size:14px; margin-bottom:40px; }
        .section-title { font-size:11px; letter-spacing:2px; text-transform:uppercase; color:#C9A84C; margin-bottom:16px; margin-top:32px; padding-bottom:8px; border-bottom:1px solid rgba(201,168,76,0.15); }
        .field { margin-bottom:20px; }
        label { display:block; font-size:13px; color:#666; margin-bottom:8px; }
        input, textarea { width:100%; background:#1a1a1a; border:1px solid #333; border-radius:8px; padding:14px; color:white; font-size:14px; outline:none; font-family:sans-serif; transition:border-color 0.2s; }
        input:focus, textarea:focus { border-color:#C9A84C; }
        textarea { height:200px; resize:vertical; }
        .hint { font-size:12px; color:#444; margin-top:6px; }
        .tg-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
        .btn { width:100%; background:#C9A84C; color:#000; border:none; border-radius:8px; padding:16px; font-size:15px; font-weight:600; cursor:pointer; margin-top:8px; transition:background 0.2s; }
        .btn:hover { background:#E8C96A; }
        .error { color:#E05555; font-size:13px; margin-top:12px; display:none; }
        .success { display:none; text-align:center; padding:32px 0; }
        .success h2 { color:#C9A84C; font-size:24px; margin-bottom:16px; }
        .success p { color:#666; font-size:14px; margin-bottom:16px; line-height:1.7; }
        .link-box { background:#1a1a1a; border:1px solid rgba(201,168,76,0.3); padding:14px; border-radius:8px; color:#C9A84C; font-size:13px; word-break:break-all; margin-bottom:12px; text-align:left; }
        .link-label { font-size:11px; color:#555; margin-bottom:6px; letter-spacing:1px; text-transform:uppercase; }
    </style>
</head>
<body>
    <div class="box">
        <div id="form-view">
            <div class="logo">🏨 SmartStay AI</div>
            <div class="sub">Otelinizi sisteme kaydedin — 3 dakikada hazır</div>

            <div class="section-title">Otel Bilgileri</div>
            <div class="field">
                <label>OTELİN ADI</label>
                <input type="text" id="name" placeholder="Örn: Rixos Premium Belek">
            </div>
            <div class="field">
                <label>URL KISALTMASI</label>
                <input type="text" id="slug" placeholder="Örn: rixos-premium">
                <div class="hint">Sadece küçük harf ve tire kullanın</div>
            </div>
            <div class="field">
                <label>YÖNETİCİ ŞİFRESİ</label>
                <input type="password" id="password" placeholder="Güvenli bir şifre">
            </div>
            <div class="field">
                <label>OTEL BİLGİLERİ</label>
                <textarea id="info" placeholder="Havuz saatleri, restoran saatleri, spa, telefon numaraları..."></textarea>
                <div class="hint">Ne kadar detaylı olursa AI o kadar iyi yanıt verir</div>
            </div>

            <div class="section-title">Telegram Bildirimleri (İsteğe Bağlı)</div>
            <div class="tg-grid">
                <div class="field">
                    <label>BOT TOKEN</label>
                    <input type="text" id="tg_token" placeholder="7xxx:AAF...">
                    <div class="hint">@BotFather'dan alın</div>
                </div>
                <div class="field">
                    <label>CHAT ID</label>
                    <input type="text" id="tg_chat" placeholder="123456789">
                    <div class="hint">@userinfobot'tan alın</div>
                </div>
            </div>

            <button class="btn" onclick="register()">Oteli Kaydet →</button>
            <div class="error" id="err"></div>
        </div>

        <div class="success" id="success-view">
            <h2>✅ Otel Kaydedildi!</h2>
            <p>Sisteminiz hazır! Linkleri kaydedin:</p>
            <div class="link-label">👤 Misafir Linki</div>
            <div class="link-box" id="guest-link"></div>
            <div class="link-label">📊 Yönetici Paneli</div>
            <div class="link-box" id="manager-link"></div>
            <div class="link-label">📱 QR Kodlar</div>
            <div class="link-box" id="qr-link"></div>
            <br>
            <button class="btn" id="dashBtn">Panele Git →</button>
        </div>
    </div>

    <script>
        let registeredSlug = '';
        let registeredPassword = '';

        document.getElementById('name').addEventListener('input', function() {
            const slug = this.value.toLowerCase()
                .replace(/[^a-z0-9\s-]/g, '')
                .replace(/\s+/g, '-')
                .replace(/-+/g, '-')
                .slice(0, 30);
            document.getElementById('slug').value = slug;
        });

        async function register() {
            const name = document.getElementById('name').value.trim();
            const slug = document.getElementById('slug').value.trim();
            const password = document.getElementById('password').value.trim();
            const info = document.getElementById('info').value.trim();
            const tg_token = document.getElementById('tg_token').value.trim();
            const tg_chat = document.getElementById('tg_chat').value.trim();
            const err = document.getElementById('err');

            if (!name || !slug || !password || !info) {
                err.textContent = '❌ Lütfen zorunlu alanları doldurun';
                err.style.display = 'block';
                return;
            }

            const res = await fetch('/api/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name, slug, password, info, tg_token, tg_chat})
            });

            const data = await res.json();
            if (data.ok) {
                registeredSlug = slug;
                registeredPassword = password;

                const base = window.location.origin;
                document.getElementById('guest-link').textContent = base + '/hotel/' + slug;
                document.getElementById('manager-link').textContent = base + '/hotel/' + slug + '/dashboard';
                document.getElementById('qr-link').textContent = base + '/hotel/' + slug + '/qrcodes';
                document.getElementById('form-view').style.display = 'none';
                document.getElementById('success-view').style.display = 'block';

                document.getElementById('dashBtn').onclick = async function() {
                    const loginRes = await fetch('/api/hotel-login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        credentials: 'include',
                        body: JSON.stringify({slug: registeredSlug, password: registeredPassword})
                    });
                    const loginData = await loginRes.json();
                    if (loginData.ok) {
                        window.location.href = '/hotel/' + registeredSlug + '/dashboard';
                    }
                };
            } else {
                err.textContent = '❌ ' + (data.error || 'Hata oluştu');
                err.style.display = 'block';
            }
        }
    </script>
</body>
</html>
"""

EDIT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartStay — Ayarlar</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:sans-serif; background:#0a0a0a; color:white; min-height:100vh; display:flex; align-items:center; justify-content:center; padding:40px 20px; }
        .box { background:#111; border-radius:16px; padding:48px; width:100%; max-width:600px; border:1px solid rgba(201,168,76,0.15); }
        .logo { color:#C9A84C; font-size:22px; font-weight:900; margin-bottom:4px; }
        .sub { color:#555; font-size:14px; margin-bottom:32px; }
        .section-title { font-size:11px; letter-spacing:2px; text-transform:uppercase; color:#C9A84C; margin-bottom:16px; margin-top:32px; padding-bottom:8px; border-bottom:1px solid rgba(201,168,76,0.15); }
        .field { margin-bottom:20px; }
        label { display:block; font-size:13px; color:#666; margin-bottom:8px; }
        input, textarea { width:100%; background:#1a1a1a; border:1px solid #333; border-radius:8px; padding:14px; color:white; font-size:14px; outline:none; font-family:sans-serif; transition:border-color 0.2s; }
        input:focus, textarea:focus { border-color:#C9A84C; }
        textarea { height:280px; resize:vertical; }
        .hint { font-size:12px; color:#444; margin-top:6px; }
        .tg-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
        .btns { display:flex; gap:12px; margin-top:8px; }
        .btn { flex:1; padding:14px; border:none; border-radius:8px; font-size:14px; font-weight:600; cursor:pointer; transition:all 0.2s; }
        .btn-gold { background:#C9A84C; color:#000; }
        .btn-gold:hover { background:#E8C96A; }
        .btn-dark { background:#1a1a1a; color:#fff; border:1px solid #333; }
        .btn-dark:hover { background:#222; }
        .success { color:#4CAF50; font-size:13px; margin-top:12px; display:none; }
        .error { color:#E05555; font-size:13px; margin-top:12px; display:none; }
        .back { color:#C9A84C; font-size:13px; text-decoration:none; display:inline-flex; align-items:center; gap:6px; margin-bottom:24px; }
        .back:hover { text-decoration:underline; }
    </style>
</head>
<body>
    <div class="box">
        <a class="back" href="javascript:history.back()">← Panele Dön</a>
        <div class="logo">🏨 SmartStay AI</div>
        <div class="sub">Otel ayarlarını düzenle</div>

        <div class="section-title">Otel Bilgileri</div>
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

        <div class="section-title">Telegram Bildirimleri</div>
        <div class="tg-grid">
            <div class="field">
                <label>BOT TOKEN</label>
                <input type="text" id="tg_token" placeholder="7xxx:AAF...">
                <div class="hint">@BotFather'dan alın</div>
            </div>
            <div class="field">
                <label>CHAT ID</label>
                <input type="text" id="tg_chat" placeholder="123456789">
                <div class="hint">@userinfobot'tan alın</div>
            </div>
        </div>

        <div class="btns">
            <button class="btn btn-gold" onclick="save()">💾 Kaydet</button>
            <button class="btn btn-dark" id="dashBtn">📊 Panele Git</button>
        </div>
        <div class="success" id="success">✅ Kaydedildi!</div>
        <div class="error" id="error"></div>
    </div>

    <script>
        const slug = window.location.pathname.split('/')[2];
        document.getElementById('dashBtn').onclick = () => window.location.href = '/hotel/' + slug + '/dashboard';

        fetch('/api/hotel/' + slug + '/info')
            .then(r => r.json())
            .then(data => {
                document.getElementById('name').value = data.name || '';
                document.getElementById('info').value = data.info || '';
                document.getElementById('tg_token').value = data.telegram_token || '';
                document.getElementById('tg_chat').value = data.telegram_chat_id || '';
            });

        async function save() {
            const name = document.getElementById('name').value.trim();
            const info = document.getElementById('info').value.trim();
            const password = document.getElementById('password').value.trim();
            const tg_token = document.getElementById('tg_token').value.trim();
            const tg_chat = document.getElementById('tg_chat').value.trim();

            const res = await fetch('/api/hotel/' + slug + '/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                credentials: 'include',
                body: JSON.stringify({name, info, password, tg_token, tg_chat})
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

def get_login_html(hotel_name="SmartStay"):
    return LOGIN_HTML.replace("HOTEL_NAME_PLACEHOLDER", hotel_name)

def get_register_html():
    return REGISTER_HTML

def get_edit_html():
    return EDIT_HTML