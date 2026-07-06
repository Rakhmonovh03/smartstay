LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>SmartStay — Login</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:'Inter',sans-serif; background:linear-gradient(135deg,#0a0a0a 0%,#1a1410 100%); color:white; min-height:100vh; display:flex; align-items:center; justify-content:center; padding:20px; }
        .box { background:#141414; border-radius:24px; padding:48px 40px; width:100%; max-width:400px; text-align:center; border:1px solid rgba(201,168,76,0.12); box-shadow:0 30px 80px rgba(0,0,0,0.5); animation:fadeIn 0.5s ease; }
        @keyframes fadeIn { from{opacity:0;transform:translateY(20px);} to{opacity:1;transform:translateY(0);} }
        .icon { width:64px; height:64px; border-radius:50%; background:linear-gradient(135deg,#C9A84C,#E8C96A); display:flex; align-items:center; justify-content:center; font-size:30px; margin:0 auto 20px; }
        .logo { color:#fff; font-size:22px; font-weight:700; margin-bottom:6px; }
        .sub { color:#666; font-size:14px; margin-bottom:32px; }
        .field-label { text-align:left; font-size:12px; color:#888; letter-spacing:1px; text-transform:uppercase; margin-bottom:7px; font-weight:600; }
        input { width:100%; background:#1f1f1f; border:1px solid #2a2a2a; border-radius:14px; padding:14px 18px; color:white; font-size:15px; outline:none; margin-bottom:16px; font-family:inherit; transition:border-color 0.2s; }
        input:focus { border-color:#C9A84C; }
        button.btn-main { width:100%; background:linear-gradient(135deg,#C9A84C,#E8C96A); color:#1a1a1a; border:none; border-radius:14px; padding:15px; font-size:15px; font-weight:700; cursor:pointer; font-family:inherit; transition:transform 0.15s; margin-top:4px; }
        button.btn-main:hover { transform:translateY(-2px); }
        button.btn-main:active { transform:translateY(0); }
        .error { color:#E05555; font-size:13px; margin-top:14px; display:none; }
        .footer-link { margin-top:24px; font-size:13px; color:#666; }
        .footer-link a { color:#C9A84C; text-decoration:none; }
        .footer-link a:hover { text-decoration:underline; }
        .lang-switcher { display:flex; justify-content:center; gap:6px; margin-bottom:28px; }
        .lang-btn { padding:4px 12px; border-radius:8px; border:1px solid rgba(201,168,76,0.2); background:transparent; color:#888; font-size:12px; font-weight:600; cursor:pointer; font-family:inherit; transition:.15s; }
        .lang-btn:hover, .lang-btn.active { border-color:#C9A84C; color:#C9A84C; background:rgba(201,168,76,0.08); }
        /* Pre-filled slug mode: hide slug field */
        .slug-hidden { display:none !important; }
    </style>
</head>
<body>
    <div class="box">
        <div class="icon">🏨</div>
        <div class="logo">SmartStay</div>
        <div class="sub" id="loginSub">Manager Dashboard</div>

        <div class="lang-switcher">
            <button class="lang-btn" onclick="setLang('en')">EN</button>
            <button class="lang-btn" onclick="setLang('ru')">RU</button>
            <button class="lang-btn" onclick="setLang('tr')">TR</button>
            <button class="lang-btn" onclick="setLang('uz')">UZ</button>
        </div>

        <div id="slugWrap">
            <div class="field-label" id="labelSlug">Hotel ID (slug)</div>
            <input type="text" id="slug" placeholder="your-hotel-name" onkeypress="if(event.key==='Enter')document.getElementById('pwd').focus()">
        </div>
        <div class="field-label" id="labelPwd">Password</div>
        <input type="password" id="pwd" placeholder="••••••••" onkeypress="if(event.key==='Enter') login()">
        <button class="btn-main" id="loginBtn" onclick="login()">Login →</button>
        <div class="error" id="err">❌ Wrong credentials</div>

        <div class="footer-link">
            <span id="noAccText">Don't have an account?</span>
            <a href="/register" id="regLink">Register</a>
        </div>
    </div>

    <script>
        // Pre-filled slug from /hotel/{slug}/login route
        const pathSlug = (function() {
            const parts = window.location.pathname.split('/');
            // /hotel/{slug}/login → parts[2]
            if (parts[1] === 'hotel' && parts[3] === 'login') return parts[2];
            return '';
        })();
        if (pathSlug) {
            document.getElementById('slug').value = pathSlug;
            document.getElementById('slugWrap').classList.add('slug-hidden');
        }

        // i18n
        const I18N = {
            en: { sub:'Manager Dashboard', labelSlug:'Hotel ID (slug)', labelPwd:'Password', btn:'Login →', err:'❌ Wrong credentials', noAcc:"Don't have an account?", reg:'Register' },
            ru: { sub:'Панель управления', labelSlug:'ID отеля (slug)', labelPwd:'Пароль', btn:'Войти →', err:'❌ Неверные данные', noAcc:'Нет аккаунта?', reg:'Зарегистрироваться' },
            tr: { sub:'Yönetici Paneli', labelSlug:'Otel Kimliği (slug)', labelPwd:'Şifre', btn:'Giriş Yap →', err:'❌ Yanlış kimlik bilgileri', noAcc:'Hesabınız yok mu?', reg:'Kayıt Ol' },
            uz: { sub:'Boshqaruv Paneli', labelSlug:'Mehmonxona ID (slug)', labelPwd:'Parol', btn:'Kirish →', err:"❌ Noto'g'ri ma'lumotlar", noAcc:"Hisobingiz yo'qmi?", reg:"Ro'yxatdan o'tish" }
        };
        let lang = localStorage.getItem('ss_lang') || 'en';
        if (!I18N[lang]) lang = 'en';

        function applyLang() {
            const L = I18N[lang];
            document.getElementById('loginSub').textContent = L.sub;
            document.getElementById('labelSlug').textContent = L.labelSlug;
            document.getElementById('labelPwd').textContent = L.labelPwd;
            document.getElementById('loginBtn').textContent = L.btn;
            document.getElementById('err').textContent = L.err;
            document.getElementById('noAccText').textContent = L.noAcc + ' ';
            document.getElementById('regLink').textContent = L.reg;
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.textContent === lang.toUpperCase()));
        }
        function setLang(l) { lang = l; localStorage.setItem('ss_lang', l); applyLang(); }
        applyLang();

        async function login() {
            const pwd = document.getElementById('pwd').value.trim();
            const slug = pathSlug || document.getElementById('slug').value.trim();
            const errEl = document.getElementById('err');
            errEl.style.display = 'none';
            if (!slug || !pwd) { errEl.style.display = 'block'; return; }
            const res = await fetch('/api/hotel-login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                credentials: 'include',
                body: JSON.stringify({slug, password: pwd})
            });
            const data = await res.json();
            if (data.ok) {
                window.location.href = '/hotel/' + slug + '/dashboard';
            } else {
                errEl.style.display = 'block';
            }
        }
    </script>
</body>
</html>
"""

REGISTER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>SmartStay — Register</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:'Inter',sans-serif; background:linear-gradient(135deg,#0a0a0a 0%,#1a1410 100%); color:white; min-height:100vh; display:flex; align-items:center; justify-content:center; padding:40px 20px; }
        .box { background:#141414; border-radius:24px; padding:48px; width:100%; max-width:600px; border:1px solid rgba(201,168,76,0.12); box-shadow:0 30px 80px rgba(0,0,0,0.5); animation:fadeIn 0.5s ease; }
        @keyframes fadeIn { from{opacity:0;transform:translateY(20px);} to{opacity:1;transform:translateY(0);} }
        .top-bar { display:flex; justify-content:space-between; align-items:center; margin-bottom:28px; }
        .head { display:flex; align-items:center; gap:14px; }
        .icon { width:52px; height:52px; border-radius:14px; background:linear-gradient(135deg,#C9A84C,#E8C96A); display:flex; align-items:center; justify-content:center; font-size:26px; }
        .logo { color:#fff; font-size:22px; font-weight:700; }
        .lang-switcher { display:flex; gap:4px; }
        .lang-btn { padding:4px 10px; border-radius:8px; border:1px solid rgba(201,168,76,0.2); background:transparent; color:#888; font-size:12px; font-weight:600; cursor:pointer; font-family:inherit; transition:.15s; }
        .lang-btn:hover, .lang-btn.active { border-color:#C9A84C; color:#C9A84C; background:rgba(201,168,76,.08); }
        .sub { color:#666; font-size:14px; margin-bottom:32px; }
        .section-title { font-size:11px; letter-spacing:2px; text-transform:uppercase; color:#C9A84C; margin-bottom:18px; margin-top:32px; padding-bottom:10px; border-bottom:1px solid rgba(201,168,76,0.12); }
        .field { margin-bottom:18px; }
        label { display:block; font-size:13px; color:#888; margin-bottom:8px; font-weight:500; }
        input, textarea { width:100%; background:#1f1f1f; border:1px solid #2a2a2a; border-radius:14px; padding:14px 16px; color:white; font-size:14px; outline:none; font-family:inherit; transition:border-color 0.2s; }
        input:focus, textarea:focus { border-color:#C9A84C; }
        textarea { height:200px; resize:vertical; }
        .hint { font-size:12px; color:#555; margin-top:6px; }
        .tg-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
        .btn { width:100%; background:linear-gradient(135deg,#C9A84C,#E8C96A); color:#1a1a1a; border:none; border-radius:14px; padding:16px; font-size:15px; font-weight:700; cursor:pointer; margin-top:8px; font-family:inherit; transition:transform 0.15s; }
        .btn:hover { transform:translateY(-2px); }
        .error { color:#E05555; font-size:13px; margin-top:12px; display:none; }
        .success { display:none; text-align:center; padding:20px 0; }
        .success-icon { width:72px; height:72px; border-radius:50%; background:rgba(76,175,80,0.15); display:flex; align-items:center; justify-content:center; font-size:36px; margin:0 auto 20px; }
        .success h2 { color:#fff; font-size:22px; margin-bottom:10px; }
        .success p { color:#666; font-size:14px; margin-bottom:20px; line-height:1.7; }
        .link-box { background:#1f1f1f; border:1px solid rgba(201,168,76,0.25); padding:14px; border-radius:12px; color:#C9A84C; font-size:13px; word-break:break-all; margin-bottom:12px; text-align:left; }
        .link-label { font-size:11px; color:#666; margin-bottom:6px; letter-spacing:1px; text-transform:uppercase; text-align:left; }
        .login-link { margin-top:20px; font-size:13px; color:#666; text-align:center; }
        .login-link a { color:#C9A84C; text-decoration:none; }
        .login-link a:hover { text-decoration:underline; }
    </style>
</head>
<body>
    <div class="box">
        <div id="form-view">
            <div class="top-bar">
                <div class="head">
                    <div class="icon">🏨</div>
                    <div class="logo">SmartStay</div>
                </div>
                <div class="lang-switcher">
                    <button class="lang-btn" onclick="setLang('en')">EN</button>
                    <button class="lang-btn" onclick="setLang('ru')">RU</button>
                    <button class="lang-btn" onclick="setLang('tr')">TR</button>
                    <button class="lang-btn" onclick="setLang('uz')">UZ</button>
                </div>
            </div>
            <div class="sub" id="sub">Register your hotel — ready in 3 minutes</div>

            <div class="section-title" id="secHotel">Hotel Info</div>
            <div class="field">
                <label id="lblName">HOTEL NAME</label>
                <input type="text" id="name" placeholder="e.g. Grand Palace Hotel">
            </div>
            <div class="field">
                <label id="lblSlug">URL ID (SLUG)</label>
                <input type="text" id="slug" placeholder="e.g. grand-palace">
                <div class="hint" id="hintSlug">Lowercase letters and hyphens only</div>
            </div>
            <div class="field">
                <label id="lblPwd">MANAGER PASSWORD</label>
                <input type="password" id="password" placeholder="Choose a secure password">
            </div>
            <div class="field">
                <label id="lblInfo">HOTEL INFORMATION</label>
                <textarea id="info" placeholder="Pool hours, restaurant times, spa, phone numbers..."></textarea>
                <div class="hint" id="hintInfo">The more detail you provide, the better the AI responds</div>
            </div>

            <!-- Room configuration moved out of the form: sensible defaults, editable later in settings -->
            <input type="hidden" id="room_count" value="30">
            <input type="hidden" id="room_start" value="101">
            <input type="hidden" id="rooms_per_floor" value="0">

            <div class="section-title" id="secTg">Telegram Notifications (Optional)</div>
            <div class="tg-grid">
                <div class="field">
                    <label id="lblTgToken">BOT TOKEN</label>
                    <input type="text" id="tg_token" placeholder="7xxx:AAF...">
                    <div class="hint" id="hintTgToken">Get from @BotFather</div>
                </div>
                <div class="field">
                    <label id="lblTgChat">CHAT ID</label>
                    <input type="text" id="tg_chat" placeholder="123456789">
                    <div class="hint" id="hintTgChat">Get from @userinfobot</div>
                </div>
            </div>

            <div id="invite-section" style="display:none">
                <div class="section-title" id="secInvite">Invite Code</div>
                <div class="field">
                    <label id="lblInvite">INVITE CODE</label>
                    <input type="text" id="invite_code" placeholder="••••••••">
                    <div class="hint" id="hintInvite">Code provided by SmartStay team</div>
                </div>
            </div>

            <button class="btn" id="registerBtn" onclick="register()">Register Hotel →</button>
            <div class="error" id="err"></div>
            <div class="login-link"><span id="haveAccount">Already have an account?</span> <a href="/login" id="loginLink">Login</a></div>
        </div>

        <div class="success" id="success-view">
            <div class="success-icon">✅</div>
            <h2 id="successTitle">Hotel Registered!</h2>
            <p id="successSub">Your system is ready! Save these links:</p>
            <div class="link-label" id="llGuest">👤 Guest Link</div>
            <div class="link-box" id="guest-link"></div>
            <div class="link-label" id="llDash">📊 Manager Dashboard</div>
            <div class="link-box" id="manager-link"></div>
            <br>
            <button class="btn" id="dashBtn">Go to Dashboard →</button>
        </div>
    </div>

    <script>
        const I18N = {
            en: {
                sub:'Register your hotel — ready in 3 minutes',
                secHotel:'Hotel Info', lblName:'HOTEL NAME', lblSlug:'URL ID (SLUG)', hintSlug:'Lowercase letters and hyphens only',
                lblPwd:'MANAGER PASSWORD', lblInfo:'HOTEL INFORMATION', hintInfo:'The more detail you provide, the better the AI responds',
                phName:'e.g. Grand Palace Hotel', phSlug:'e.g. grand-palace', phPwd:'Choose a secure password', phInfoReg:'Pool hours, restaurant times, spa, phone numbers...',
                secTg:'Telegram Notifications (Optional)', lblTgToken:'BOT TOKEN', lblTgChat:'CHAT ID', hintTgToken:'Get from @BotFather', hintTgChat:'Get from @userinfobot',
                secInvite:'Invite Code', lblInvite:'INVITE CODE', hintInvite:'Code provided by SmartStay team',
                registerBtn:'Register Hotel →', errRequired:'❌ Please fill in all required fields',
                haveAccount:'Already have an account?', loginLink:'Login',
                successTitle:'Hotel Registered!', successSub:'Your system is ready! Save these links:',
                llGuest:'👤 Guest Link', llDash:'📊 Manager Dashboard', dashBtn:'Go to Dashboard →'
            },
            ru: {
                sub:'Зарегистрируйте ваш отель — готово за 3 минуты',
                secHotel:'Данные отеля', lblName:'НАЗВАНИЕ ОТЕЛЯ', lblSlug:'URL (SLUG)', hintSlug:'Только строчные буквы и дефисы',
                lblPwd:'ПАРОЛЬ МЕНЕДЖЕРА', lblInfo:'ИНФОРМАЦИЯ ОБ ОТЕЛЕ', hintInfo:'Чем подробнее, тем лучше AI отвечает',
                phName:'Напр. Grand Palace Hotel', phSlug:'напр. grand-palace', phPwd:'Придумайте надёжный пароль', phInfoReg:'Часы работы бассейна, ресторана, спа, номера телефонов...',
                secTg:'Уведомления Telegram (необязательно)', lblTgToken:'ТОКЕН БОТА', lblTgChat:'ID ЧАТА', hintTgToken:'Получить у @BotFather', hintTgChat:'Получить у @userinfobot',
                secInvite:'Инвайт-код', lblInvite:'ИНВАЙТ-КОД', hintInvite:'Код от команды SmartStay',
                registerBtn:'Зарегистрировать отель →', errRequired:'❌ Пожалуйста, заполните все обязательные поля',
                haveAccount:'Уже есть аккаунт?', loginLink:'Войти',
                successTitle:'Отель зарегистрирован!', successSub:'Система готова! Сохраните ссылки:',
                llGuest:'👤 Ссылка для гостей', llDash:'📊 Панель управления', dashBtn:'Перейти в дашборд →'
            },
            tr: {
                sub:'Otelinizi kaydedin — 3 dakikada hazır',
                secHotel:'Otel Bilgileri', lblName:'OTELİN ADI', lblSlug:'URL KISALTMASI (SLUG)', hintSlug:'Sadece küçük harf ve tire kullanın',
                lblPwd:'YÖNETİCİ ŞİFRESİ', lblInfo:'OTEL BİLGİLERİ', hintInfo:'Ne kadar detaylı olursa AI o kadar iyi yanıt verir',
                phName:'Örn: Grand Palace Hotel', phSlug:'örn: grand-palace', phPwd:'Güvenli bir şifre belirleyin', phInfoReg:'Havuz saatleri, restoran saatleri, spa, telefon numaraları...',
                secTg:'Telegram Bildirimleri (İsteğe Bağlı)', lblTgToken:'BOT TOKEN', lblTgChat:'SOHBET ID', hintTgToken:"@BotFather'dan alın", hintTgChat:"@userinfobot'tan alın",
                secInvite:'Davet Kodu', lblInvite:'DAVET KODU', hintInvite:'SmartStay ekibinden aldığınız kod',
                registerBtn:'Oteli Kaydet →', errRequired:'❌ Lütfen zorunlu alanları doldurun',
                haveAccount:'Hesabınız var mı?', loginLink:'Giriş Yap',
                successTitle:'Otel Kaydedildi!', successSub:'Sisteminiz hazır! Linkleri kaydedin:',
                llGuest:'👤 Misafir Linki', llDash:'📊 Yönetici Paneli', dashBtn:'Panele Git →'
            },
            uz: {
                sub:"Mehmonxonangizni ro'yxatdan o'tkazing — 3 daqiqada tayyor",
                secHotel:"Mehmonxona ma'lumotlari", lblName:'MEHMONXONA NOMI', lblSlug:'URL ID (SLUG)', hintSlug:"Faqat kichik harflar va defislar",
                lblPwd:'MENEJER PAROLI', lblInfo:"MEHMONXONA HAQIDA MA'LUMOT", hintInfo:"Qancha batafsil bo'lsa, AI shuncha yaxshi javob beradi",
                phName:'Masalan: Grand Palace Hotel', phSlug:'masalan: grand-palace', phPwd:'Xavfsiz parol tanlang', phInfoReg:'Basseyn ish vaqti, restoran vaqtlari, spa, telefon raqamlari...',
                secTg:"Telegram bildirishnomalar (ixtiyoriy)", lblTgToken:'BOT TOKENI', lblTgChat:'CHAT ID', hintTgToken:"@BotFather dan oling", hintTgChat:"@userinfobot dan oling",
                secInvite:'Taklif kodi', lblInvite:'TAKLIF KODI', hintInvite:'SmartStay jamoasidan olingan kod',
                registerBtn:"Mehmonxonani ro'yxatdan o'tkazish →", errRequired:"❌ Iltimos, barcha majburiy maydonlarni to'ldiring",
                haveAccount:"Hisobingiz bormi?", loginLink:'Kirish',
                successTitle:"Mehmonxona ro'yxatdan o'tkazildi!", successSub:'Tizimingiz tayyor! Havolalarni saqlang:',
                llGuest:'👤 Mehmon havolasi', llDash:'📊 Boshqaruv paneli', dashBtn:"Panelga o'tish →"
            }
        };

        // Language: saved choice -> browser language -> English
        let lang = localStorage.getItem('ss_lang') || (navigator.language || 'en').slice(0, 2).toLowerCase();
        if (!I18N[lang]) lang = 'en';

        function applyLang() {
            const L = I18N[lang];
            const ids = ['sub','secHotel','lblName','lblSlug','hintSlug','lblPwd','lblInfo','hintInfo',
                         'secTg','lblTgToken','lblTgChat','hintTgToken','hintTgChat',
                         'secInvite','lblInvite','hintInvite','registerBtn','haveAccount','loginLink',
                         'successTitle','successSub','llGuest','llDash','dashBtn'];
            ids.forEach(id => {
                const el = document.getElementById(id);
                if (el && L[id] !== undefined) el.textContent = L[id];
            });
            const phMap = {name:'phName', slug:'phSlug', password:'phPwd', info:'phInfoReg'};
            Object.entries(phMap).forEach(([id, key]) => {
                const el = document.getElementById(id);
                if (el && L[key]) el.placeholder = L[key];
            });
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.textContent === lang.toUpperCase()));
        }
        function setLang(l) { lang = l; localStorage.setItem('ss_lang', l); applyLang(); }
        applyLang();

        let registeredSlug = '';
        let registeredPassword = '';

        fetch('/api/register-config').then(r => r.json()).then(d => {
            if (d.invite_required) document.getElementById('invite-section').style.display = 'block';
        }).catch(() => {});

        document.getElementById('name').addEventListener('input', function() {
            const slug = this.value.toLowerCase()
                .replace(/[^a-z0-9\\s-]/g, '')
                .replace(/\\s+/g, '-')
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
            const invite_code = document.getElementById('invite_code')?.value.trim() || '';
            const room_count = parseInt(document.getElementById('room_count').value) || 30;
            const room_start = parseInt(document.getElementById('room_start').value) || 101;
            const rooms_per_floor = parseInt(document.getElementById('rooms_per_floor').value) || 0;
            const err = document.getElementById('err');

            if (!name || !slug || !password || !info) {
                err.textContent = I18N[lang].errRequired;
                err.style.display = 'block';
                return;
            }

            const res = await fetch('/api/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name, slug, password, info, tg_token, tg_chat,
                                      invite_code, room_count, room_start, rooms_per_floor})
            });

            const data = await res.json();
            if (data.ok) {
                registeredSlug = slug;
                registeredPassword = password;
                const base = window.location.origin;
                document.getElementById('guest-link').textContent = base + '/hotel/' + slug;
                document.getElementById('manager-link').textContent = base + '/hotel/' + slug + '/dashboard';
                document.getElementById('form-view').style.display = 'none';
                const sv = document.getElementById('success-view');
                sv.style.display = 'block';
                applyLang();
                document.getElementById('dashBtn').onclick = async function() {
                    const loginRes = await fetch('/api/hotel-login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        credentials: 'include',
                        body: JSON.stringify({slug: registeredSlug, password: registeredPassword})
                    });
                    if ((await loginRes.json()).ok) window.location.href = '/hotel/' + registeredSlug + '/dashboard';
                };
            } else {
                err.textContent = '❌ ' + (data.error || 'Error');
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:'Inter',sans-serif; background:linear-gradient(135deg,#0a0a0a 0%,#1a1410 100%); color:white; min-height:100vh; display:flex; align-items:center; justify-content:center; padding:40px 20px; }
        .box { background:#141414; border-radius:24px; padding:48px; width:100%; max-width:600px; border:1px solid rgba(201,168,76,0.12); box-shadow:0 30px 80px rgba(0,0,0,0.5); animation:fadeIn 0.5s ease; }
        @keyframes fadeIn { from{opacity:0;transform:translateY(20px);} to{opacity:1;transform:translateY(0);} }
        .head { display:flex; align-items:center; gap:14px; margin-bottom:8px; }
        .icon { width:52px; height:52px; border-radius:14px; background:linear-gradient(135deg,#C9A84C,#E8C96A); display:flex; align-items:center; justify-content:center; font-size:26px; }
        .logo { color:#fff; font-size:22px; font-weight:700; }
        .sub { color:#666; font-size:14px; margin-bottom:24px; }
        .section-title { font-size:11px; letter-spacing:2px; text-transform:uppercase; color:#C9A84C; margin-bottom:18px; margin-top:32px; padding-bottom:10px; border-bottom:1px solid rgba(201,168,76,0.12); }
        .field { margin-bottom:18px; }
        label { display:block; font-size:13px; color:#888; margin-bottom:8px; font-weight:500; }
        input, textarea { width:100%; background:#1f1f1f; border:1px solid #2a2a2a; border-radius:14px; padding:14px 16px; color:white; font-size:14px; outline:none; font-family:inherit; transition:border-color 0.2s; }
        input:focus, textarea:focus { border-color:#C9A84C; }
        textarea { height:280px; resize:vertical; }
        .hint { font-size:12px; color:#555; margin-top:6px; }
        .tg-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
        .btns { display:flex; gap:12px; margin-top:8px; }
        .btn { flex:1; padding:15px; border:none; border-radius:14px; font-size:14px; font-weight:700; cursor:pointer; font-family:inherit; transition:transform 0.15s; }
        .btn:hover { transform:translateY(-2px); }
        .btn-gold { background:linear-gradient(135deg,#C9A84C,#E8C96A); color:#1a1a1a; }
        .btn-dark { background:#1f1f1f; color:#fff; border:1px solid #2a2a2a; }
        .success { color:#4CAF50; font-size:13px; margin-top:12px; display:none; }
        .error { color:#E05555; font-size:13px; margin-top:12px; display:none; }
        .back { color:#C9A84C; font-size:13px; text-decoration:none; display:inline-flex; align-items:center; gap:6px; margin-bottom:24px; }
        .back:hover { text-decoration:underline; }
    </style>
</head>
<body>
    <div class="box">
        <a class="back" id="editBack" href="javascript:history.back()">← Panele Dön</a>
        <div class="head">
            <div class="icon">🏨</div>
            <div class="logo">SmartStay AI</div>
        </div>
        <div class="sub" id="editSub">Otel ayarlarını düzenle</div>

        <div class="section-title" id="editSecHotel">Otel Bilgileri</div>
        <div class="field">
            <label id="editLblName">OTELİN ADI</label>
            <input type="text" id="name" placeholder="Otel adı">
        </div>
        <div class="field">
            <label id="editLblInfo">OTEL BİLGİLERİ</label>
            <textarea id="info" data-i18n-ph="phInfo" placeholder="Otel bilgileri..."></textarea>
        </div>
        <div class="field">
            <label id="editLblPwd">YENİ ŞİFRE (değiştirmek istemiyorsanız boş bırakın)</label>
            <input type="password" id="password" data-i18n-ph="phNewPassword" placeholder="Yeni şifre">
        </div>

        <div class="section-title" id="editSecTg">Telegram Bildirimleri</div>
        <div class="tg-grid">
            <div class="field">
                <label>BOT TOKEN</label>
                <input type="text" id="tg_token" placeholder="7xxx:AAF...">
                <div class="hint" data-i18n="hintTgToken">@BotFather'dan alın</div>
            </div>
            <div class="field">
                <label>CHAT ID</label>
                <input type="text" id="tg_chat" placeholder="123456789">
                <div class="hint" data-i18n="hintTgChat">@userinfobot'tan alın</div>
            </div>
        </div>

        <div class="section-title" id="editSecTg2">Telegram 2 Yönlü Mesajlaşma</div>
        <div class="field" style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:16px 18px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap">
            <div>
                <div style="font-size:13px;color:#ccc;margin-bottom:4px;font-weight:600" id="editTgWebhookTitle">Telegram Webhook</div>
                <div style="font-size:12px;color:#555;line-height:1.6" id="editTgWebhookDesc">Bot token kayıt edildikten sonra webhook'u etkinleştirin.<br>Misafire gelen mesajlara Telegram'dan yanıt verebilirsiniz.</div>
            </div>
            <button class="btn" style="width:auto;padding:11px 20px;margin:0;font-size:13px" onclick="setupWebhook()" id="webhookBtn">🔗 Webhook Kur</button>
        </div>
        <div id="webhookResult" style="font-size:12px;margin-top:8px;display:none"></div>

        <div class="section-title" id="editSecAI">AI Asistan Ayarları</div>
        <div class="field">
            <label id="editLblAIName">AI ASISTAN ADI</label>
            <input type="text" id="ai_name" placeholder="AI Asistan" maxlength="40">
            <div class="hint" id="editHintAI">Misafirlere kendini bu isimle tanıtır (örn: "Aria", "Luna", "Max")</div>
        </div>

        <div class="section-title" id="editSecLang">🌐 Dil Ayarları</div>
        <div class="field">
            <label id="editLblDefaultLang">VARSAYILAN DİL</label>
            <select id="default_language" style="width:100%;background:#1f1f1f;border:1px solid #2a2a2a;border-radius:14px;padding:14px 16px;color:white;font-size:14px;outline:none;font-family:inherit">
                <option value="auto">🌐 Auto (detect guest language)</option>
                <option value="en">🇬🇧 English</option>
                <option value="ru">🇷🇺 Русский</option>
                <option value="tr">🇹🇷 Türkçe</option>
                <option value="uz">🇺🇿 O'zbek</option>
                <option value="ar">🇸🇦 العربية</option>
                <option value="zh">🇨🇳 中文</option>
                <option value="de">🇩🇪 Deutsch</option>
                <option value="fr">🇫🇷 Français</option>
                <option value="es">🇪🇸 Español</option>
                <option value="it">🇮🇹 Italiano</option>
                <option value="pt">🇧🇷 Português</option>
                <option value="ja">🇯🇵 日本語</option>
                <option value="ko">🇰🇷 한국어</option>
                <option value="hi">🇮🇳 हिन्दी</option>
                <option value="fa">🇮🇷 فارسی</option>
                <option value="az">🇦🇿 Azərbaycan</option>
                <option value="kk">🇰🇿 Қазақша</option>
                <option value="ky">🇰🇬 Кыргызча</option>
                <option value="tk">🇹🇲 Türkmen</option>
                <option value="uk">🇺🇦 Українська</option>
                <option value="pl">🇵🇱 Polski</option>
                <option value="nl">🇳🇱 Nederlands</option>
                <option value="id">🇮🇩 Indonesia</option>
                <option value="ms">🇲🇾 Melayu</option>
                <option value="ro">🇷🇴 Română</option>
                <option value="cs">🇨🇿 Čeština</option>
                <option value="hu">🇭🇺 Magyar</option>
            </select>
            <div class="hint" id="editHintAutoLang">Otomatik: AI misafirin yazdığı dili algılar ve o dilde yanıt verir</div>
        </div>
        <div class="field">
            <label id="editLblSupportedLangs">DESTEKLENECEĞİ DİLLER (virgülle ayırın)</label>
            <input type="text" id="supported_languages" placeholder="en,ru,tr,ar,de,fr">
        </div>

        <div class="section-title" id="editSecEmail">📧 E-posta Bildirimleri (SMTP)</div>
        <div class="field">
            <label id="editLblSmtpHost">SMTP SUNUCU</label>
            <input type="text" id="smtp_host" placeholder="smtp.gmail.com">
            <div class="hint">Gmail: smtp.gmail.com · Outlook: smtp-mail.outlook.com · SendGrid: smtp.sendgrid.net</div>
        </div>
        <div class="field" style="display:flex;gap:12px">
            <div style="flex:1">
                <label>PORT</label>
                <input type="number" id="smtp_port" placeholder="587" min="1" max="65535">
            </div>
            <div style="flex:2">
                <label id="editLblSmtpUser">KULLANICI ADI</label>
                <input type="text" id="smtp_user" placeholder="user@gmail.com">
            </div>
        </div>
        <div class="field">
            <label id="editLblSmtpPass">SMTP ŞİFRE / APP PASSWORD</label>
            <input type="password" id="smtp_pass" placeholder="••••••••••••">
        </div>
        <div class="field">
            <label id="editLblSmtpFrom">GÖNDEREN ADRESİ (FROM)</label>
            <input type="email" id="smtp_from" placeholder="hotel@gmail.com">
        </div>
        <div class="field">
            <label id="editLblNotifyEmail">BİLDİRİM E-POSTASI (ALICI)</label>
            <input type="email" id="notify_email" placeholder="manager@hotel.com">
        </div>

        <div class="section-title" id="editSecPage">🌐 Публичная страница (/hotel/…/page)</div>
        <div class="field">
            <label id="editLblPhoto">ФОТО ОТЕЛЯ (URL)</label>
            <input type="url" id="photo_url" placeholder="https://example.com/hotel.jpg">
        </div>
        <div class="field">
            <label id="editLblPageDesc">МАРКЕТИНГОВОЕ ОПИСАНИЕ</label>
            <textarea id="page_description" style="height:140px" placeholder="Описание для гостей до заезда..."></textarea>
        </div>
        <div class="field">
            <label id="editLblAmenities">УДОБСТВА (через запятую)</label>
            <input type="text" id="amenities" placeholder="🏊 Бассейн, 🌐 WiFi, 🍽️ Ресторан, 💆 Спа">
        </div>

        <div class="section-title" id="editSecBilling">💳 Abonelik &amp; Faturalandırma</div>
        <div id="billingSection" style="background:#111;border:1px solid #2a2a2a;border-radius:12px;padding:20px">
            <!-- Current plan -->
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px">
                <div>
                    <div style="font-size:12px;color:#888;margin-bottom:4px" id="bilActivePlan">AKTİF PLAN</div>
                    <div id="planNameEl" style="font-size:20px;font-weight:700;color:#C9A84C">Yükleniyor...</div>
                    <div id="stripeStatusEl" style="font-size:12px;color:#666;margin-top:2px"></div>
                </div>
                <button id="manageSubBtn" onclick="goToPortal()"
                        style="display:none;padding:8px 16px;background:#1a1a1a;border:1px solid #333;color:#aaa;
                               border-radius:8px;cursor:pointer;font-size:13px">
                    ⚙️ Aboneliği Yönet
                </button>
            </div>

            <!-- Plan cards -->
            <div id="planCards" style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">
                <!-- filled by JS -->
            </div>

            <!-- Stripe not configured notice -->
            <div id="stripeNotConfigured" style="display:none;margin-top:12px;padding:12px;
                 background:#1a1a1a;border-radius:8px;font-size:13px;color:#888;text-align:center">
                <span id="bilStripeNotice">💡 Stripe henüz yapılandırılmadı. STRIPE_SECRET_KEY ve fiyat ID'lerini .env dosyasına ekleyin.</span>
            </div>
        </div>

        <div class="section-title" id="editSecRooms">🚪 Oda Ayarları</div>
        <div class="field">
            <label id="editLblRoomsPerFloor">KATINA GÖRE ODA SAYISI</label>
            <input type="number" id="rooms_per_floor" value="0" min="0" max="100" placeholder="0">
        </div>

        <div class="section-title" id="editSecReview">Yorum Entegrasyonu</div>
        <div class="field">
            <label id="editLblBooking">BOOKING.COM YORUM LİNKİ</label>
            <input type="url" id="booking_url" placeholder="https://www.booking.com/hotel/...">
        </div>

        <div class="section-title" id="editSecInteg">🔗 Интеграция — встроить на сайт</div>
        <div class="field" style="background:#111;border:1px solid #2a2a2a;border-radius:14px;padding:20px">
            <div style="font-size:13px;color:#888;margin-bottom:14px;line-height:1.6" id="editIntegDesc">
                Вставьте одну строку кода на сайт отеля — появится кнопка-консьерж 🛎️ с всплывающим чатом.
            </div>
            <div style="background:#0a0a0a;border:1px solid #1f1f1f;border-radius:10px;padding:14px;font-family:monospace;font-size:13px;color:#C9A84C;word-break:break-all;margin-bottom:12px" id="embedCode">
                Загрузка...
            </div>
            <div style="display:flex;gap:10px;flex-wrap:wrap">
                <button onclick="copyEmbed()" class="btn btn-gold" style="flex:1;min-width:140px" id="editCopyBtn">📋 Скопировать код</button>
                <button onclick="openWidget()" class="btn btn-dark" style="flex:1;min-width:140px" id="editPreviewBtn">👁️ Превью виджета</button>
            </div>
            <div id="embedCopied" style="font-size:12px;color:#4CAF50;margin-top:8px;display:none" id="editCopied">✅ Скопировано!</div>
        </div>

        <div class="btns">
            <button class="btn btn-gold" onclick="save()" id="editSaveBtn">💾 Kaydet</button>
            <button class="btn btn-dark" id="dashBtn">📊 Panele Git</button>
        </div>
        <div class="success" id="success">✅ Kaydedildi!</div>
        <div class="error" id="error"></div>
    </div>

    <script>
        const slug = window.location.pathname.split('/')[2];
        document.getElementById('dashBtn').onclick = () => window.location.href = '/hotel/' + slug + '/dashboard';

        // Embed code
        (function() {
            const base = window.location.origin;
            const code = '<script src="' + base + '/hotel/' + slug + '/embed.js"><\\/script>';
            document.getElementById('embedCode').textContent = code;
        })();
        function copyEmbed() {
            const base = window.location.origin;
            const code = '<script src="' + base + '/hotel/' + slug + '/embed.js"><\\/script>';
            navigator.clipboard.writeText(code).then(() => {
                const el = document.getElementById('embedCopied');
                el.style.display = 'block';
                setTimeout(() => el.style.display = 'none', 2500);
            }).catch(() => {
                prompt('Скопируйте код:', code);
            });
        }
        function openWidget() {
            window.open('/hotel/' + slug + '/widget', '_blank', 'width=400,height=640');
        }

        function ET(k) {
            const lang = localStorage.getItem('ss_lang') || 'en';
            const L = EDIT_I18N[lang] || EDIT_I18N.en;
            return (L[k] !== undefined ? L[k] : (EDIT_I18N.en[k] !== undefined ? EDIT_I18N.en[k] : k));
        }

        async function setupWebhook() {
            const btn = document.getElementById('webhookBtn');
            const res = document.getElementById('webhookResult');
            btn.textContent = ET('whSetting');
            btn.disabled = true;
            try {
                const r = await fetch('/api/hotel/' + slug + '/telegram/set-webhook', {credentials:'include'});
                const data = await r.json();
                res.style.display = 'block';
                if (data.ok) {
                    res.style.color = '#4CAF50';
                    res.textContent = ET('whDone') + data.webhook_url;
                    btn.textContent = ET('whActive');
                } else {
                    res.style.color = '#E05555';
                    res.textContent = '❌ ' + (data.error || JSON.stringify(data));
                    btn.textContent = ET('webhookBtn');
                    btn.disabled = false;
                }
            } catch(e) {
                res.style.display = 'block';
                res.style.color = '#E05555';
                res.textContent = ET('whConnErr');
                btn.textContent = ET('webhookBtn');
                btn.disabled = false;
            }
        }

        // ===== BILLING =====
        function planDetails() {
            return {
                starter: { label: '🏠 ' + ET('planMiniName'),   price: '$49'  + ET('bilPerMonth'), features: ET('featStarter') },
                pro:     { label: '⭐ ' + ET('planStdName'),    price: '$129' + ET('bilPerMonth'), features: ET('featPro') },
                premium: { label: '🏝 ' + ET('planResortName'), price: '$299' + ET('bilPerMonth'), features: ET('featPremium') },
            };
        }

        async function loadBilling() {
            try {
                const d = await fetch('/api/hotel/' + slug + '/billing/info', {credentials:'include'}).then(r => r.json());
                const currentPlan = d.plan || 'trial';
                const planLabels = { trial: ET('bilTrial'), starter: ET('planMiniName'), pro: ET('planStdName'), premium: ET('planResortName') };
                document.getElementById('planNameEl').textContent = planLabels[currentPlan] || currentPlan;

                const statusEl = document.getElementById('stripeStatusEl');
                if (d.stripe_status === 'active')   { statusEl.textContent = ET('bilStActive'); statusEl.style.color = '#4caf50'; }
                else if (d.stripe_status === 'past_due') { statusEl.textContent = ET('bilStPastDue'); statusEl.style.color = '#E8A040'; }
                else if (d.stripe_status === 'canceled') { statusEl.textContent = ET('bilStCanceled'); statusEl.style.color = '#e05555'; }

                if (d.has_subscription) document.getElementById('manageSubBtn').style.display = 'block';

                if (!d.stripe_configured) {
                    document.getElementById('stripeNotConfigured').style.display = 'block';
                }

                const cards = document.getElementById('planCards');
                cards.innerHTML = Object.entries(planDetails()).map(([key, info]) => {
                    const isCurrent = currentPlan === key;
                    const priceId = d.prices[key];
                    return `<div style="background:${isCurrent ? '#1e1a0e' : '#1a1a1a'};border:1px solid ${isCurrent ? '#C9A84C' : '#2a2a2a'};
                                       border-radius:10px;padding:16px;text-align:center">
                        <div style="font-size:14px;font-weight:700;margin-bottom:4px">${info.label}</div>
                        <div style="font-size:18px;font-weight:800;color:#C9A84C;margin-bottom:10px">${info.price}</div>
                        <ul style="list-style:none;font-size:12px;color:#888;margin-bottom:14px;text-align:left;line-height:1.8">
                            ${info.features.map(f => `<li>✓ ${f}</li>`).join('')}
                        </ul>
                        ${isCurrent
                            ? '<div style="background:#C9A84C;color:#000;border-radius:6px;padding:6px;font-size:12px;font-weight:700">' + ET('bilCurrent') + '</div>'
                            : priceId
                                ? `<button onclick="upgradePlan('${priceId}')"
                                          style="width:100%;padding:8px;background:#C9A84C;color:#000;border:none;border-radius:6px;
                                                 font-weight:700;cursor:pointer;font-size:13px">
                                       ${ET('bilChoose')}
                                   </button>`
                                : '<div style="color:#555;font-size:12px">' + ET('bilNotConfigured') + '</div>'
                        }
                    </div>`;
                }).join('');
            } catch(e) {
                console.error('Billing load error:', e);
            }
        }

        async function upgradePlan(priceId) {
            try {
                const r = await fetch('/api/hotel/' + slug + '/billing/checkout', {
                    method: 'POST', credentials: 'include',
                    headers: {'Content-Type':'application/json'},
                    body: JSON.stringify({price_id: priceId})
                });
                const d = await r.json();
                if (d.checkout_url) {
                    window.location.href = d.checkout_url;
                } else {
                    alert('❌ ' + (d.error || ET('bilCheckoutFail')));
                }
            } catch(e) {
                alert(ET('whConnErr'));
            }
        }

        function goToPortal() {
            window.location.href = '/api/hotel/' + slug + '/billing/portal';
        }

        loadBilling();

        fetch('/api/hotel/' + slug + '/info')
            .then(r => r.json())
            .then(data => {
                document.getElementById('name').value = data.name || '';
                document.getElementById('info').value = data.info || '';
                document.getElementById('tg_token').value = data.telegram_token || '';
                document.getElementById('tg_chat').value = data.telegram_chat_id || '';
                document.getElementById('booking_url').value = data.booking_url || '';
                document.getElementById('ai_name').value = data.ai_name || '';
                document.getElementById('smtp_host').value = data.smtp_host || '';
                document.getElementById('smtp_port').value = data.smtp_port || 587;
                document.getElementById('smtp_user').value = data.smtp_user || '';
                document.getElementById('smtp_from').value = data.smtp_from || '';
                document.getElementById('notify_email').value = data.notify_email || '';
                document.getElementById('default_language').value = data.default_language || 'auto';
                document.getElementById('supported_languages').value = data.supported_languages || 'en,ru,tr,ar,de,fr';
                document.getElementById('photo_url').value = data.photo_url || '';
                document.getElementById('page_description').value = data.page_description || '';
                document.getElementById('amenities').value = data.amenities || '';
                document.getElementById('rooms_per_floor').value = data.rooms_per_floor || 0;
                // smtp_pass intentionally left blank for security
            });

        // ===== i18n =====
        const EDIT_I18N = {
            en: {
                editBack:'← Back to Dashboard', editSub:'Edit hotel settings',
                editSecHotel:'Hotel Information', editLblName:'HOTEL NAME',
                editLblInfo:'HOTEL INFORMATION', editLblPwd:'NEW PASSWORD (leave blank to keep current)',
                editSecTg:'Telegram Notifications', editSecTg2:'Telegram 2-Way Messaging',
                editTgWebhookTitle:'Telegram Webhook',
                editTgWebhookDesc:'Activate the webhook after saving the bot token. You can reply to guests directly from Telegram.',
                editSecAI:'AI Assistant Settings', editLblAIName:'AI ASSISTANT NAME',
                editHintAI:'Introduces itself to guests by this name (e.g. "Aria", "Luna", "Max")',
                editSecLang:'🌐 Language Settings', editLblDefaultLang:'DEFAULT LANGUAGE',
                editLblSupportedLangs:'SUPPORTED LANGUAGES (comma-separated)',
                editSecEmail:'📧 Email Notifications (SMTP)',
                editLblSmtpUser:'USERNAME', editLblSmtpPass:'SMTP PASSWORD / APP PASSWORD',
                editLblSmtpFrom:'SENDER ADDRESS (FROM)', editLblNotifyEmail:'NOTIFICATION EMAIL (RECIPIENT)',
                editSecPage:'🌐 Public Page (/hotel/…/page)', editLblPhoto:'HOTEL PHOTO (URL)',
                editLblPageDesc:'MARKETING DESCRIPTION', editLblAmenities:'AMENITIES (comma-separated)',
                editSecBilling:'💳 Subscription & Billing', editSecRooms:'🚪 Room Settings',
                editLblRoomsPerFloor:'ROOMS PER FLOOR', editSecReview:'Review Integration',
                editLblBooking:'BOOKING.COM REVIEW LINK',
                editSecInteg:'🔗 Integration — embed on website',
                editIntegDesc:'Add one line of code to your hotel website — a 🛎️ concierge button with popup chat appears.',
                editCopyBtn:'📋 Copy code', editPreviewBtn:'👁️ Widget preview',
                editSaveBtn:'💾 Save', success:'✅ Saved!',
                hintTgToken:'Get from @BotFather', hintTgChat:'Get from @userinfobot', phInfo:'Hotel information...', phNewPassword:'New password',
                webhookBtn:'🔗 Set up Webhook', whSetting:'⏳ Setting up...', whDone:'✅ Webhook set! URL: ', whActive:'✅ Active', whConnErr:'❌ Connection error',
                editHintAutoLang:'Auto: AI detects the guest language and replies in it', editLblSmtpHost:'SMTP SERVER',
                bilActivePlan:'ACTIVE PLAN', manageSubBtn:'⚙️ Manage Subscription', bilTrial:'Trial', bilCurrent:'Current Plan',
                bilChoose:'Upgrade →', bilNotConfigured:'Not configured', bilPerMonth:'/mo', bilCheckoutFail:'Checkout failed',
                bilStripeNotice:'💡 Stripe is not configured yet. Add STRIPE_SECRET_KEY and price IDs to the .env file.',
                bilStActive:'✅ Active subscription', bilStPastDue:'⚠️ Payment overdue', bilStCanceled:'❌ Canceled',
                planMiniName:'Mini', planStdName:'Standard', planResortName:'Resort',
                featStarter:['Up to 15 rooms','AI guest chat 24/7','Request tracker','Telegram notifications'],
                featPro:['Up to 40 rooms','Everything in Mini','Staff roles','Staff chat','Analytics'],
                featPremium:['Unlimited rooms','Multiple properties','Custom AI setup','Priority support'],
            },
            ru: {
                editBack:'← Назад', editSub:'Редактировать настройки отеля',
                editSecHotel:'Информация об отеле', editLblName:'НАЗВАНИЕ ОТЕЛЯ',
                editLblInfo:'ИНФОРМАЦИЯ ОБ ОТЕЛЕ', editLblPwd:'НОВЫЙ ПАРОЛЬ (оставьте пустым, чтобы не менять)',
                editSecTg:'Telegram уведомления', editSecTg2:'Telegram двухсторонний обмен',
                editTgWebhookTitle:'Telegram Webhook',
                editTgWebhookDesc:'Активируйте вебхук после сохранения токена бота. Можно отвечать гостям прямо из Telegram.',
                editSecAI:'Настройки AI ассистента', editLblAIName:'ИМЯ AI АССИСТЕНТА',
                editHintAI:'Представляется гостям этим именем (напр. "Aria", "Luna", "Max")',
                editSecLang:'🌐 Настройки языка', editLblDefaultLang:'ЯЗЫК ПО УМОЛЧАНИЮ',
                editLblSupportedLangs:'ПОДДЕРЖИВАЕМЫЕ ЯЗЫКИ (через запятую)',
                editSecEmail:'📧 Email уведомления (SMTP)',
                editLblSmtpUser:'ИМЯ ПОЛЬЗОВАТЕЛЯ', editLblSmtpPass:'ПАРОЛЬ SMTP / APP PASSWORD',
                editLblSmtpFrom:'АДРЕС ОТПРАВИТЕЛЯ (FROM)', editLblNotifyEmail:'EMAIL ДЛЯ УВЕДОМЛЕНИЙ (ПОЛУЧАТЕЛЬ)',
                editSecPage:'🌐 Публичная страница (/hotel/…/page)', editLblPhoto:'ФОТО ОТЕЛЯ (URL)',
                editLblPageDesc:'МАРКЕТИНГОВОЕ ОПИСАНИЕ', editLblAmenities:'УДОБСТВА (через запятую)',
                editSecBilling:'💳 Подписка & Оплата', editSecRooms:'🚪 Настройки номеров',
                editLblRoomsPerFloor:'НОМЕРОВ НА ЭТАЖЕ', editSecReview:'Интеграция отзывов',
                editLblBooking:'ССЫЛКА НА ОТЗЫВЫ BOOKING.COM',
                editSecInteg:'🔗 Интеграция — встроить на сайт',
                editIntegDesc:'Вставьте одну строку кода на сайт отеля — появится кнопка-консьерж 🛎️ с всплывающим чатом.',
                editCopyBtn:'📋 Скопировать код', editPreviewBtn:'👁️ Превью виджета',
                editSaveBtn:'💾 Сохранить', success:'✅ Сохранено!',
                hintTgToken:'Получить у @BotFather', hintTgChat:'Получить у @userinfobot', phInfo:'Информация об отеле...', phNewPassword:'Новый пароль',
                webhookBtn:'🔗 Подключить вебхук', whSetting:'⏳ Подключаю...', whDone:'✅ Вебхук подключён! URL: ', whActive:'✅ Активен', whConnErr:'❌ Ошибка соединения',
                editHintAutoLang:'Авто: AI определяет язык гостя и отвечает на нём', editLblSmtpHost:'SMTP СЕРВЕР',
                bilActivePlan:'АКТИВНЫЙ ПЛАН', manageSubBtn:'⚙️ Управление подпиской', bilTrial:'Пробный (Trial)', bilCurrent:'Текущий план',
                bilChoose:'Перейти →', bilNotConfigured:'Не настроено', bilPerMonth:'/мес', bilCheckoutFail:'Не удалось открыть оплату',
                bilStripeNotice:'💡 Stripe ещё не настроен. Добавьте STRIPE_SECRET_KEY и ID цен в файл .env.',
                bilStActive:'✅ Подписка активна', bilStPastDue:'⚠️ Платёж просрочен', bilStCanceled:'❌ Отменена',
                planMiniName:'Мини', planStdName:'Стандарт', planResortName:'Резорт',
                featStarter:['До 15 номеров','AI-чат для гостей 24/7','Трекер запросов','Telegram-уведомления'],
                featPro:['До 40 номеров','Всё из «Мини»','Роли персонала','Чат персонала','Аналитика'],
                featPremium:['Номера без лимита','Несколько объектов','Настройка AI под отель','Приоритетная поддержка'],
            },
            tr: {
                editBack:'← Panele Dön', editSub:'Otel ayarlarını düzenle',
                editSecHotel:'Otel Bilgileri', editLblName:'OTELİN ADI',
                editLblInfo:'OTEL BİLGİLERİ', editLblPwd:'YENİ ŞİFRE (değiştirmek istemiyorsanız boş bırakın)',
                editSecTg:'Telegram Bildirimleri', editSecTg2:'Telegram 2 Yönlü Mesajlaşma',
                editTgWebhookTitle:'Telegram Webhook',
                editTgWebhookDesc:"Bot token kayıt edildikten sonra webhook'u etkinleştirin. Misafire gelen mesajlara Telegram'dan yanıt verebilirsiniz.",
                editSecAI:'AI Asistan Ayarları', editLblAIName:'AI ASISTAN ADI',
                editHintAI:'Misafirlere kendini bu isimle tanıtır (örn: "Aria", "Luna", "Max")',
                editSecLang:'🌐 Dil Ayarları', editLblDefaultLang:'VARSAYILAN DİL',
                editLblSupportedLangs:'DESTEKLENECEĞİ DİLLER (virgülle ayırın)',
                editSecEmail:'📧 E-posta Bildirimleri (SMTP)',
                editLblSmtpUser:'KULLANICI ADI', editLblSmtpPass:'SMTP ŞİFRE / APP PASSWORD',
                editLblSmtpFrom:'GÖNDEREN ADRESİ (FROM)', editLblNotifyEmail:'BİLDİRİM E-POSTASI (ALICI)',
                editSecPage:'🌐 Genel Sayfa (/hotel/…/page)', editLblPhoto:'OTEL FOTOĞRAFI (URL)',
                editLblPageDesc:'PAZARLAMA AÇIKLAMASI', editLblAmenities:'OLANAKLAR (virgülle ayırın)',
                editSecBilling:'💳 Abonelik & Faturalandırma', editSecRooms:'🚪 Oda Ayarları',
                editLblRoomsPerFloor:'KATINA GÖRE ODA SAYISI', editSecReview:'Yorum Entegrasyonu',
                editLblBooking:'BOOKING.COM YORUM LİNKİ',
                editSecInteg:'🔗 Entegrasyon — web sitesine ekle',
                editIntegDesc:'Otel web sitenize bir satır kod ekleyin — 🛎️ konsiyerj düğmesi çıkar.',
                editCopyBtn:'📋 Kodu kopyala', editPreviewBtn:'👁️ Widget önizleme',
                editSaveBtn:'💾 Kaydet', success:'✅ Kaydedildi!',
                hintTgToken:"@BotFather'dan alın", hintTgChat:"@userinfobot'tan alın", phInfo:'Otel bilgileri...', phNewPassword:'Yeni şifre',
                webhookBtn:'🔗 Webhook Kur', whSetting:'⏳ Kuruluyor...', whDone:'✅ Webhook kuruldu! URL: ', whActive:'✅ Aktif', whConnErr:'❌ Bağlantı hatası',
                editHintAutoLang:'Otomatik: AI misafirin yazdığı dili algılar ve o dilde yanıt verir', editLblSmtpHost:'SMTP SUNUCU',
                bilActivePlan:'AKTİF PLAN', manageSubBtn:'⚙️ Aboneliği Yönet', bilTrial:'Deneme (Trial)', bilCurrent:'Mevcut Plan',
                bilChoose:'Geç →', bilNotConfigured:'Yapılandırılmadı', bilPerMonth:'/ay', bilCheckoutFail:'Checkout başarısız',
                bilStripeNotice:"💡 Stripe henüz yapılandırılmadı. STRIPE_SECRET_KEY ve fiyat ID'lerini .env dosyasına ekleyin.",
                bilStActive:'✅ Aktif abonelik', bilStPastDue:'⚠️ Ödeme gecikmiş', bilStCanceled:'❌ İptal edildi',
                planMiniName:'Mini', planStdName:'Standart', planResortName:'Resort',
                featStarter:['15 odaya kadar','7/24 AI misafir sohbeti','Talep takipçisi','Telegram bildirimleri'],
                featPro:['40 odaya kadar',"Mini'deki her şey",'Personel rolleri','Personel sohbeti','Analitik'],
                featPremium:['Sınırsız oda','Birden fazla mülk','Özel AI kurulumu','Öncelikli destek'],
            },
            uz: {
                editBack:'← Panelga qaytish', editSub:"Mehmonxona sozlamalarini tahrirlash",
                editSecHotel:'Mehmonxona haqida', editLblName:"MEHMONXONA NOMI",
                editLblInfo:"MEHMONXONA MA'LUMOTLARI", editLblPwd:"YANGI PAROL (o'zgartirmasangiz bo'sh qoldiring)",
                editSecTg:'Telegram bildirishnomalari', editSecTg2:"Telegram 2 tomonlama xabar",
                editTgWebhookTitle:'Telegram Webhook',
                editTgWebhookDesc:"Bot token saqlangandan keyin webhookni faollashtiring. Mehmonlarga Telegram orqali javob berishingiz mumkin.",
                editSecAI:'AI Assistent sozlamalari', editLblAIName:"AI ASSISTENT NOMI",
                editHintAI:`"Aria", "Luna", "Max" kabi nomlar bilan mehmonlarga o'zini tanishtiradi`,
                editSecLang:'🌐 Til sozlamalari', editLblDefaultLang:"STANDART TIL",
                editLblSupportedLangs:"QOLLAB-QUVVATLANADIGAN TILLAR (vergul bilan)",
                editSecEmail:'📧 Email bildirishnomalari (SMTP)',
                editLblSmtpUser:"FOYDALANUVCHI ADI", editLblSmtpPass:"SMTP PAROL / APP PAROL",
                editLblSmtpFrom:"JO'NATUVCHI MANZILI (FROM)", editLblNotifyEmail:"BILDIRISHNOMA EMAILI (QABUL QILUVCHI)",
                editSecPage:"🌐 Ommaviy sahifa (/hotel/…/page)", editLblPhoto:"MEHMONXONA RASMI (URL)",
                editLblPageDesc:"MARKETING TAVSIFI", editLblAmenities:"QULAYLIKLAR (vergul bilan)",
                editSecBilling:"💳 Obuna & To'lov", editSecRooms:"🚪 Xona sozlamalari",
                editLblRoomsPerFloor:"QAVATDAGI XONALAR SONI", editSecReview:"Sharh integratsiyasi",
                editLblBooking:"BOOKING.COM SHARH HAVOLASI",
                editSecInteg:"🔗 Integratsiya — veb-saytga joylashtirish",
                editIntegDesc:"Mehmonxona veb-saytiga bir qator kod qo'shing — 🛎️ konsyerj tugmasi paydo bo'ladi.",
                editCopyBtn:"📋 Kodni nusxalash", editPreviewBtn:"👁️ Vidjet oldinko'rish",
                editSaveBtn:"💾 Saqlash", success:"✅ Saqlandi!",
                hintTgToken:"@BotFather dan oling", hintTgChat:"@userinfobot dan oling", phInfo:"Mehmonxona ma'lumotlari...", phNewPassword:"Yangi parol",
                webhookBtn:"🔗 Webhook o'rnatish", whSetting:"⏳ O'rnatilmoqda...", whDone:"✅ Webhook o'rnatildi! URL: ", whActive:'✅ Faol', whConnErr:'❌ Ulanish xatosi',
                editHintAutoLang:'Avto: AI mehmon tilini aniqlab, shu tilda javob beradi', editLblSmtpHost:'SMTP SERVER',
                bilActivePlan:'FAOL TARIF', manageSubBtn:'⚙️ Obunani boshqarish', bilTrial:'Sinov (Trial)', bilCurrent:'Joriy tarif',
                bilChoose:"O'tish →", bilNotConfigured:'Sozlanmagan', bilPerMonth:'/oy', bilCheckoutFail:"To'lovni ochib bo'lmadi",
                bilStripeNotice:"💡 Stripe hali sozlanmagan. STRIPE_SECRET_KEY va narx IDlarini .env fayliga qo'shing.",
                bilStActive:'✅ Faol obuna', bilStPastDue:"⚠️ To'lov kechikkan", bilStCanceled:'❌ Bekor qilingan',
                planMiniName:'Mini', planStdName:'Standart', planResortName:'Resort',
                featStarter:['15 tagacha xona','24/7 AI mehmon chati',"So'rovlar kuzatuvchisi",'Telegram bildirishnomalari'],
                featPro:['40 tagacha xona',"Mini'dagi hammasi",'Xodim rollari','Xodimlar chati','Analitika'],
                featPremium:['Cheksiz xonalar','Bir nechta obyekt','AI maxsus sozlash',"Ustuvor qo'llab-quvvatlash"],
            },
        };
        (function applyEditLang() {
            const lang = localStorage.getItem('ss_lang') || 'en';
            const L = EDIT_I18N[lang] || EDIT_I18N.en;
            Object.keys(L).forEach(id => {
                const el = document.getElementById(id);
                if (el) el.textContent = L[id];
            });
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const k = el.getAttribute('data-i18n');
                if (L[k]) el.textContent = L[k];
            });
            document.querySelectorAll('[data-i18n-ph]').forEach(el => {
                const k = el.getAttribute('data-i18n-ph');
                if (L[k]) el.placeholder = L[k];
            });
            const dashBtn = document.getElementById('dashBtn');
            if (dashBtn) dashBtn.textContent = (lang === 'en' ? '📊 Back to Dashboard' : lang === 'ru' ? '📊 На панель' : lang === 'uz' ? '📊 Panelga' : '📊 Panele Git');
        })();

        async function save() {
            const name = document.getElementById('name').value.trim();
            const info = document.getElementById('info').value.trim();
            const password = document.getElementById('password').value.trim();
            const tg_token = document.getElementById('tg_token').value.trim();
            const tg_chat = document.getElementById('tg_chat').value.trim();
            const booking_url = document.getElementById('booking_url').value.trim();
            const ai_name = document.getElementById('ai_name').value.trim();
            const smtp_host = document.getElementById('smtp_host').value.trim();
            const smtp_port = document.getElementById('smtp_port').value.trim();
            const smtp_user = document.getElementById('smtp_user').value.trim();
            const smtp_pass = document.getElementById('smtp_pass').value;
            const smtp_from = document.getElementById('smtp_from').value.trim();
            const notify_email = document.getElementById('notify_email').value.trim();
            const default_language = document.getElementById('default_language').value;
            const supported_languages = document.getElementById('supported_languages').value.trim() || 'en,ru,tr,ar,de,fr';
            const photo_url = document.getElementById('photo_url').value.trim();
            const page_description = document.getElementById('page_description').value.trim();
            const amenities = document.getElementById('amenities').value.trim();
            const rooms_per_floor = parseInt(document.getElementById('rooms_per_floor').value) || 0;

            const res = await fetch('/api/hotel/' + slug + '/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                credentials: 'include',
                body: JSON.stringify({name, info, password, tg_token, tg_chat, booking_url, ai_name,
                                      smtp_host, smtp_port, smtp_user, smtp_pass, smtp_from, notify_email,
                                      default_language, supported_languages,
                                      photo_url, page_description, amenities, rooms_per_floor})
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
    # hotel_name kept for backward compat but unused — slug is now read from URL path by JS
    return LOGIN_HTML

def get_register_html():
    return REGISTER_HTML

def get_edit_html():
    return EDIT_HTML