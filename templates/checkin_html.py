def get_checkin_html(hotel_name="SmartStay", default_lang="en"):
    import html as _html
    hotel_name = _html.escape(hotel_name or "SmartStay")  # hotel-controlled → escape
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>{hotel_name} — Check-in</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <meta name="theme-color" content="#C9A84C">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{
            font-family:'Inter',sans-serif;
            background:linear-gradient(135deg,#0a0a0a 0%,#1a1410 100%);
            color:white; min-height:100dvh;
            display:flex; align-items:center; justify-content:center;
            padding:max(24px, env(safe-area-inset-top)) 24px max(24px, env(safe-area-inset-bottom));
        }}
        .card {{
            background:#141414; border-radius:24px; padding:40px;
            width:100%; max-width:480px;
            border:1px solid rgba(201,168,76,0.12);
            box-shadow:0 30px 80px rgba(0,0,0,0.5);
            animation:fadeIn 0.5s ease;
        }}
        @keyframes fadeIn {{ from{{opacity:0;transform:translateY(20px)}} to{{opacity:1;transform:translateY(0)}} }}

        /* HEADER */
        .header {{ text-align:center; margin-bottom:32px; }}
        .hotel-icon {{ font-size:40px; margin-bottom:12px; }}
        .hotel-name {{ font-size:20px; font-weight:700; color:#fff; }}
        .page-sub {{ font-size:13px; color:#555; margin-top:4px; }}

        /* STEP INDICATOR */
        .steps {{ display:flex; align-items:center; justify-content:center; gap:0; margin-bottom:32px; }}
        .step {{ display:flex; align-items:center; gap:8px; }}
        .step-dot {{
            width:28px; height:28px; border-radius:50%;
            display:flex; align-items:center; justify-content:center;
            font-size:12px; font-weight:700;
            background:#1f1f1f; color:#555; border:2px solid #2a2a2a;
            transition:all 0.3s;
        }}
        .step-dot.active {{ background:linear-gradient(135deg,#C9A84C,#E8C96A); color:#000; border-color:transparent; }}
        .step-dot.done {{ background:rgba(76,175,80,0.15); color:#4CAF50; border-color:#4CAF50; }}
        .step-label {{ font-size:12px; color:#555; transition:color 0.3s; }}
        .step-label.active {{ color:#C9A84C; font-weight:600; }}
        .step-line {{ width:40px; height:2px; background:#1f1f1f; margin:0 4px; }}

        /* FORM */
        .section-label {{
            font-size:11px; letter-spacing:2px; text-transform:uppercase;
            color:#C9A84C; margin-bottom:20px;
            padding-bottom:10px; border-bottom:1px solid rgba(201,168,76,0.1);
        }}
        .field {{ margin-bottom:16px; }}
        label {{ display:block; font-size:12px; color:#666; margin-bottom:7px; font-weight:500; letter-spacing:0.5px; text-transform:uppercase; }}
        input, select {{
            width:100%; background:#1a1a1a; border:1px solid #252525;
            border-radius:12px; padding:13px 15px; color:white;
            font-size:14px; outline:none; font-family:inherit;
            transition:border-color 0.2s;
        }}
        input:focus, select:focus {{ border-color:#C9A84C; background:#1d1d1d; }}
        select option {{ background:#1a1a1a; }}
        .grid-2 {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}

        /* BUTTONS */
        .btn-row {{ display:flex; gap:10px; margin-top:24px; }}
        .btn {{
            flex:1; padding:14px; border:none; border-radius:12px;
            font-size:14px; font-weight:700; cursor:pointer;
            font-family:inherit; transition:transform 0.15s;
        }}
        .btn:hover {{ transform:translateY(-2px); }}
        .btn-gold {{ background:linear-gradient(135deg,#C9A84C,#E8C96A); color:#000; }}
        .btn-dark {{ background:#1f1f1f; color:#888; border:1px solid #2a2a2a; flex:0 0 auto; width:100px; }}

        /* STATES */
        .validating {{
            display:none; text-align:center; padding:32px 0;
        }}
        .spinner {{
            width:44px; height:44px; border-radius:50%;
            border:3px solid #1f1f1f; border-top-color:#C9A84C;
            margin:0 auto 16px; animation:spin 0.8s linear infinite;
        }}
        @keyframes spin {{ to{{transform:rotate(360deg)}} }}
        .validating p {{ color:#666; font-size:14px; }}

        .success {{ display:none; text-align:center; padding:20px 0; }}
        .success-icon {{
            width:72px; height:72px; border-radius:50%;
            background:rgba(76,175,80,0.12); border:2px solid rgba(76,175,80,0.3);
            display:flex; align-items:center; justify-content:center;
            font-size:36px; margin:0 auto 20px;
            animation:pop 0.4s cubic-bezier(0.34,1.56,0.64,1);
        }}
        @keyframes pop {{ from{{transform:scale(0)}} to{{transform:scale(1)}} }}
        .success h2 {{ font-size:22px; font-weight:700; margin-bottom:8px; }}
        .success p {{ color:#666; font-size:14px; line-height:1.6; }}
        .room-badge {{
            display:inline-block; margin-top:16px;
            background:rgba(201,168,76,0.1); border:1px solid rgba(201,168,76,0.3);
            border-radius:12px; padding:12px 24px;
            font-size:28px; font-weight:800; color:#C9A84C;
            letter-spacing:2px;
        }}
        .room-label {{ font-size:11px; color:#555; letter-spacing:2px; text-transform:uppercase; margin-bottom:6px; }}

        .error-msg {{ color:#E05555; font-size:13px; margin-top:12px; display:none; text-align:center; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="hotel-icon">🏨</div>
            <div class="hotel-name">{hotel_name}</div>
            <div class="page-sub" id="ciSub">Digital Check-in</div>
        </div>

        <!-- STEP INDICATOR -->
        <div class="steps">
            <div class="step">
                <div class="step-dot active" id="dot1">1</div>
                <div class="step-label active" id="lbl1">Personal Info</div>
            </div>
            <div class="step-line"></div>
            <div class="step">
                <div class="step-dot" id="dot2">2</div>
                <div class="step-label" id="lbl2">Stay Details</div>
            </div>
        </div>

        <!-- STEP 1 -->
        <div id="step1">
            <div class="section-label" id="ciSecLabel1">Identity</div>
            <div class="grid-2">
                <div class="field">
                    <label id="ciLblFirst">First Name</label>
                    <input type="text" id="first_name" placeholder="Ivan / John" autocomplete="given-name">
                </div>
                <div class="field">
                    <label id="ciLblLast">Last Name</label>
                    <input type="text" id="last_name" placeholder="Ivanov / Smith" autocomplete="family-name">
                </div>
            </div>
            <div class="field">
                <label id="ciLblPassport">Passport / ID No</label>
                <input type="text" id="passport" placeholder="AB1234567" autocomplete="off">
            </div>
            <div class="field">
                <label id="ciLblNat">Nationality</label>
                <select id="nationality">
                    <option value="" id="ciOptPlaceholder">Select...</option>
                    <option value="Russia">🇷🇺 Russia</option>
                    <option value="Ukraine">🇺🇦 Ukraine</option>
                    <option value="Belarus">🇧🇾 Belarus</option>
                    <option value="Kazakhstan">🇰🇿 Kazakhstan</option>
                    <option value="Uzbekistan">🇺🇿 Uzbekistan</option>
                    <option value="Germany">🇩🇪 Germany</option>
                    <option value="Turkey">🇹🇷 Turkey</option>
                    <option value="UK">🇬🇧 UK</option>
                    <option value="France">🇫🇷 France</option>
                    <option value="USA">🇺🇸 USA</option>
                    <option value="Other">🌍 Other</option>
                </select>
            </div>
            <div class="btn-row">
                <button class="btn btn-gold" id="ciBtn1" onclick="goStep2()">Continue →</button>
            </div>
            <div class="error-msg" id="err1"></div>
        </div>

        <!-- STEP 2 -->
        <div id="step2" style="display:none">
            <div class="section-label" id="ciSecLabel2">Stay Details</div>
            <div class="field">
                <label id="ciLblRoom">Room Number</label>
                <input type="text" id="room" placeholder="101">
            </div>
            <div class="grid-2">
                <div class="field">
                    <label id="ciLblCI">Check-in Date</label>
                    <input type="date" id="check_in">
                </div>
                <div class="field">
                    <label id="ciLblCO">Check-out Date</label>
                    <input type="date" id="check_out">
                </div>
            </div>
            <div class="btn-row">
                <button class="btn btn-dark" id="ciBack" onclick="goStep1()">← Back</button>
                <button class="btn btn-gold" id="ciSubmit" onclick="submitCheckin()">Check-in ✓</button>
            </div>
            <div class="error-msg" id="err2"></div>
        </div>

        <!-- VALIDATING -->
        <div class="validating" id="validating">
            <div class="spinner"></div>
            <p id="ciValidatingTxt">Verifying your information...</p>
        </div>

        <!-- SUCCESS -->
        <div class="success" id="success">
            <div class="success-icon">✅</div>
            <h2 id="ciSuccessH2">Check-in Complete!</h2>
            <p id="ciSuccessMsg">Welcome! Your stay has been registered.</p>
            <div class="room-label" id="ciRoomLabel">YOUR ROOM</div>
            <div class="room-badge" id="successRoom">—</div>
            <p id="ciSuccessHint" style="margin-top:20px;font-size:12px;color:#444">
                Scan the QR code in your room for any requests.
            </p>
        </div>
    </div>

    <script>
        const HOTEL_LANG = '{default_lang}';
        const CHECKIN_I18N = {{
          en: {{
            ciSub:'Digital Check-in', lbl1:'Personal Info', lbl2:'Stay Details',
            ciSecLabel1:'Identity', ciLblFirst:'First Name', ciLblLast:'Last Name',
            ciLblPassport:'Passport / ID No', ciLblNat:'Nationality',
            ciOptPlaceholder:'Select...', ciBtn1:'Continue →',
            ciSecLabel2:'Stay Details', ciLblRoom:'Room Number',
            ciLblCI:'Check-in Date', ciLblCO:'Check-out Date',
            ciBack:'← Back', ciSubmit:'Check-in ✓',
            ciValidatingTxt:'Verifying your information...',
            ciSuccessH2:'Check-in Complete!',
            ciSuccessMsg:'Welcome! Your stay has been registered.',
            ciRoomLabel:'YOUR ROOM',
            ciSuccessHint:'Scan the QR code in your room for any requests.',
            errName:'First and last name are required',
            errPassport:'Passport number is required',
            errRoom:'Enter room number', errDate:'Select dates',
            errDateRange:'Check-out must be after check-in',
            errServer:'An error occurred', errNet:'Connection error, please try again',
          }},
          ru: {{
            ciSub:'Цифровая регистрация', lbl1:'Личные данные', lbl2:'Проживание',
            ciSecLabel1:'Личные данные', ciLblFirst:'Имя', ciLblLast:'Фамилия',
            ciLblPassport:'Паспорт / Номер документа', ciLblNat:'Гражданство',
            ciOptPlaceholder:'Выберите...', ciBtn1:'Продолжить →',
            ciSecLabel2:'Детали проживания', ciLblRoom:'Номер комнаты',
            ciLblCI:'Дата заезда', ciLblCO:'Дата выезда',
            ciBack:'← Назад', ciSubmit:'Заселиться ✓',
            ciValidatingTxt:'Проверяем ваши данные...',
            ciSuccessH2:'Регистрация завершена!',
            ciSuccessMsg:'Добро пожаловать! Ваше проживание зарегистрировано.',
            ciRoomLabel:'ВАШ НОМЕР',
            ciSuccessHint:'Отсканируйте QR-код в номере для любых запросов.',
            errName:'Имя и фамилия обязательны',
            errPassport:'Номер паспорта обязателен',
            errRoom:'Введите номер комнаты', errDate:'Выберите даты',
            errDateRange:'Дата выезда должна быть позже заезда',
            errServer:'Произошла ошибка', errNet:'Ошибка соединения, попробуйте снова',
          }},
          tr: {{
            ciSub:'Dijital Check-in', lbl1:'Kişisel Bilgiler', lbl2:'Konaklama',
            ciSecLabel1:'Kimlik Bilgileri', ciLblFirst:'Ad', ciLblLast:'Soyad',
            ciLblPassport:'Pasaport / Kimlik No', ciLblNat:'Uyruk',
            ciOptPlaceholder:'Seçiniz...', ciBtn1:'Devam Et →',
            ciSecLabel2:'Konaklama Detayları', ciLblRoom:'Oda Numarası',
            ciLblCI:'Giriş Tarihi', ciLblCO:'Çıkış Tarihi',
            ciBack:'← Geri', ciSubmit:'Check-in Yap ✓',
            ciValidatingTxt:'Bilgileriniz doğrulanıyor...',
            ciSuccessH2:'Check-in Tamamlandı!',
            ciSuccessMsg:'Hoş geldiniz! Konaklamanız kaydedildi.',
            ciRoomLabel:'ODANIZ',
            ciSuccessHint:'Herhangi bir isteğiniz için oda içindeki QR kodu tarayabilirsiniz.',
            errName:'Ad ve soyad zorunludur',
            errPassport:'Pasaport numarası zorunludur',
            errRoom:'Oda numarasını girin', errDate:'Tarih seçin',
            errDateRange:'Çıkış tarihi girişten sonra olmalı',
            errServer:'Bir hata oluştu', errNet:'Bağlantı hatası, tekrar deneyin',
          }},
          uz: {{
            ciSub:"Raqamli Ro'yxatdan O'tish", lbl1:"Shaxsiy ma'lumot", lbl2:"Turar joy",
            ciSecLabel1:"Shaxsiy ma'lumot", ciLblFirst:"Ism", ciLblLast:"Familiya",
            ciLblPassport:"Pasport / ID raqami", ciLblNat:"Fuqarolik",
            ciOptPlaceholder:"Tanlang...", ciBtn1:"Davom etish →",
            ciSecLabel2:"Turar joy tafsilotlari", ciLblRoom:"Xona raqami",
            ciLblCI:"Kirish sanasi", ciLblCO:"Chiqish sanasi",
            ciBack:"← Orqaga", ciSubmit:"Ro'yxatdan o'tish ✓",
            ciValidatingTxt:"Ma'lumotlaringiz tekshirilmoqda...",
            ciSuccessH2:"Ro'yxatdan o'tish yakunlandi!",
            ciSuccessMsg:"Xush kelibsiz! Qolishingiz ro'yxatga olindi.",
            ciRoomLabel:"XONANGIZ",
            ciSuccessHint:"Har qanday talab uchun xonadagi QR kodni skanerlang.",
            errName:"Ism va familiya majburiy",
            errPassport:"Pasport raqami majburiy",
            errRoom:"Xona raqamini kiriting", errDate:"Sanalarni tanlang",
            errDateRange:"Chiqish sanasi kirishdan keyin bo'lishi kerak",
            errServer:"Xato yuz berdi", errNet:"Ulanish xatosi, qayta urining",
          }},
        }};
        // UI language: saved guest choice → hotel setting → browser language → English.
        function _pickLang() {{
          let saved = null;
          try {{ saved = localStorage.getItem('ss_lang'); }} catch(e) {{}}
          if (saved && CHECKIN_I18N[saved]) return saved;
          if (CHECKIN_I18N[HOTEL_LANG]) return HOTEL_LANG;
          const nav = (navigator.language || 'en').slice(0, 2);
          if (CHECKIN_I18N[nav]) return nav;
          return 'en';
        }}
        const CUR_LANG = _pickLang();
        function _L() {{ return CHECKIN_I18N[CUR_LANG] || CHECKIN_I18N.en; }}
        function applyCheckinLang() {{
          const L = _L();
          ['ciSub','lbl1','lbl2','ciSecLabel1','ciLblFirst','ciLblLast',
           'ciLblPassport','ciLblNat','ciOptPlaceholder','ciBtn1','ciSecLabel2',
           'ciLblRoom','ciLblCI','ciLblCO','ciBack','ciSubmit','ciValidatingTxt',
           'ciSuccessH2','ciSuccessMsg','ciRoomLabel','ciSuccessHint'
          ].forEach(id => {{ const el = document.getElementById(id); if (el && L[id]) el.textContent = L[id]; }});
        }}
        applyCheckinLang();

        const slug = window.location.pathname.split('/')[2] || '';

        // Set today as default check-in
        const today = new Date().toISOString().split('T')[0];
        const tomorrow = new Date(Date.now() + 86400000).toISOString().split('T')[0];
        document.getElementById('check_in').value = today;
        document.getElementById('check_out').value = tomorrow;
        document.getElementById('check_in').min = today;

        function showErr(id, msg) {{
            const el = document.getElementById(id);
            el.textContent = '❌ ' + msg;
            el.style.display = 'block';
            setTimeout(() => el.style.display = 'none', 4000);
        }}

        function goStep2() {{
            const first = document.getElementById('first_name').value.trim();
            const last = document.getElementById('last_name').value.trim();
            const passport = document.getElementById('passport').value.trim();
            if (!first || !last) {{ showErr('err1', _L().errName); return; }}
            if (!passport) {{ showErr('err1', _L().errPassport); return; }}
            document.getElementById('step1').style.display = 'none';
            document.getElementById('step2').style.display = 'block';
            // Update step indicators
            document.getElementById('dot1').className = 'step-dot done';
            document.getElementById('dot1').textContent = '✓';
            document.getElementById('lbl1').className = 'step-label';
            document.getElementById('dot2').className = 'step-dot active';
            document.getElementById('lbl2').className = 'step-label active';
        }}

        function goStep1() {{
            document.getElementById('step2').style.display = 'none';
            document.getElementById('step1').style.display = 'block';
            document.getElementById('dot1').className = 'step-dot active';
            document.getElementById('dot1').textContent = '1';
            document.getElementById('lbl1').className = 'step-label active';
            document.getElementById('dot2').className = 'step-dot';
            document.getElementById('lbl2').className = 'step-label';
        }}

        async function submitCheckin() {{
            const room = document.getElementById('room').value.trim();
            const check_in = document.getElementById('check_in').value;
            const check_out = document.getElementById('check_out').value;

            if (!room) {{ showErr('err2', _L().errRoom); return; }}
            if (!check_in || !check_out) {{ showErr('err2', _L().errDate); return; }}
            if (check_out <= check_in) {{ showErr('err2', _L().errDateRange); return; }}

            document.getElementById('step2').style.display = 'none';
            document.getElementById('validating').style.display = 'block';

            const body = {{
                first_name: document.getElementById('first_name').value.trim(),
                last_name: document.getElementById('last_name').value.trim(),
                passport: document.getElementById('passport').value.trim(),
                nationality: document.getElementById('nationality').value,
                room, check_in, check_out
            }};

            try {{
                const res = await fetch('/api/hotel/' + slug + '/checkin', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(body)
                }});
                const data = await res.json();
                document.getElementById('validating').style.display = 'none';
                if (data.ok) {{
                    document.getElementById('successRoom').textContent = '🚪 ' + data.room;
                    document.getElementById('success').style.display = 'block';
                }} else {{
                    document.getElementById('step2').style.display = 'block';
                    showErr('err2', data.error || _L().errServer);
                }}
            }} catch(e) {{
                document.getElementById('validating').style.display = 'none';
                document.getElementById('step2').style.display = 'block';
                showErr('err2', _L().errNet);
            }}
        }}
    </script>
</body>
</html>"""
