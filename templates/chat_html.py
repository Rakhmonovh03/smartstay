def get_chat_html(hotel_name="SmartStay AI", hotel_slug="", default_lang="en"):
    import html as _html
    hotel_name = _html.escape(hotel_name or "SmartStay AI")  # hotel-controlled → escape
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{hotel_name}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <meta name="theme-color" content="#C9A84C">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="{hotel_name}">
    {"<link rel='manifest' href='/hotel/" + hotel_slug + "/manifest.json'>" if hotel_slug else ""}
    {"<link rel='apple-touch-icon' href='/hotel/" + hotel_slug + "/icon.svg'>" if hotel_slug else ""}
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1410 100%);
            color:white; height:100dvh; display:flex;
            align-items:center; justify-content:center; padding:16px;
        }}
        .chat-box {{
            width:100%; max-width:420px; height:92dvh; max-height:720px;
            background:#141414; border-radius:24px; overflow:hidden;
            display:flex; flex-direction:column;
            box-shadow:0 30px 80px rgba(0,0,0,0.6);
            border:1px solid rgba(201,168,76,0.12);
        }}
        /* PWA standalone + small screens */
        @media (display-mode: standalone) {{
            body {{ padding:0; align-items:stretch; }}
            .chat-box {{ height:100dvh; max-height:none; border-radius:0;
                         padding-top:env(safe-area-inset-top);
                         padding-bottom:env(safe-area-inset-bottom); }}
        }}
        @media (max-width:480px) {{
            body {{ padding:0; align-items:stretch; }}
            .chat-box {{ height:100dvh; max-height:none; border-radius:0; }}
            .input-area {{ padding-bottom:calc(12px + env(safe-area-inset-bottom)); }}
        }}
        /* Install bar */
        #install-bar {{
            display:none; background:#1a1810;
            border-bottom:1px solid rgba(201,168,76,0.2);
            padding:8px 14px; align-items:center;
            gap:8px; justify-content:space-between;
        }}
        #install-bar span {{ font-size:12px; color:#aaa; flex:1; }}
        .install-btn {{
            padding:5px 14px; background:#C9A84C; color:#000;
            border:none; border-radius:20px; font-weight:700;
            font-size:12px; cursor:pointer; font-family:inherit; white-space:nowrap;
        }}
        .install-dismiss {{
            padding:4px 8px; background:transparent; border:none;
            color:#555; cursor:pointer; font-size:18px; line-height:1;
        }}
        .chat-header {{
            background:linear-gradient(135deg, #C9A84C 0%, #E8C96A 100%);
            padding:20px 20px 16px; text-align:center; position:relative;
        }}
        .header-avatar {{
            width:52px; height:52px; border-radius:50%;
            background:rgba(0,0,0,0.15); display:flex;
            align-items:center; justify-content:center;
            font-size:26px; margin:0 auto 8px;
        }}
        .chat-header h2 {{ font-size:17px; font-weight:700; color:#1a1a1a; }}
        .chat-header p {{ font-size:11px; color:rgba(0,0,0,0.55); margin-top:3px; letter-spacing:0.5px; }}
        .status-dot {{
            display:inline-block; width:7px; height:7px; border-radius:50%;
            background:#2ecc71; margin-right:5px; vertical-align:middle;
            animation:pulse 2s infinite;
        }}
        @keyframes pulse {{
            0% {{ box-shadow:0 0 0 0 rgba(46,204,113,0.5); }}
            70% {{ box-shadow:0 0 0 6px rgba(46,204,113,0); }}
            100% {{ box-shadow:0 0 0 0 rgba(46,204,113,0); }}
        }}
        .theme-btn {{
            position:absolute; top:14px; right:14px;
            background:rgba(0,0,0,0.2); border:none; border-radius:20px;
            padding:5px 11px; cursor:pointer; font-size:11px;
            color:#1a1a1a; font-weight:600; font-family:inherit;
        }}
        .room-bar {{
            background:rgba(201,168,76,0.08); padding:8px 20px;
            font-size:12px; color:#C9A84C; text-align:center; font-weight:500;
            border-bottom:1px solid rgba(201,168,76,0.1);
        }}

        /* SERVICE MENU */
        .service-menu {{
            display:flex; gap:8px; padding:10px 14px;
            overflow-x:auto; border-bottom:1px solid rgba(255,255,255,0.05);
            scrollbar-width:none;
        }}
        .service-menu::-webkit-scrollbar {{ display:none; }}
        .service-btn {{
            flex-shrink:0; background:#1e1e1e; border:1px solid #2a2a2a;
            border-radius:20px; padding:6px 14px; font-size:12px; color:#aaa;
            cursor:pointer; font-family:inherit; transition:all 0.2s; white-space:nowrap;
        }}
        .service-btn:hover {{ border-color:#C9A84C; color:#C9A84C; background:#1a1810; }}
        .service-btn.active {{ border-color:#C9A84C; color:#C9A84C; background:#1a1810; }}

        /* SERVICES OVERLAY */
        .services-overlay {{
            position:absolute; inset:0; background:rgba(0,0,0,0.65);
            z-index:100; display:none; align-items:flex-end;
            backdrop-filter:blur(4px); border-radius:24px;
        }}
        .services-overlay.open {{ display:flex; }}
        .services-panel {{
            width:100%; background:#1a1a1a; border-radius:20px 20px 0 0;
            padding:20px 16px 28px; max-height:72%;
            overflow-y:auto; animation:slidePanel 0.25s ease;
        }}
        @keyframes slidePanel {{
            from {{ transform:translateY(30px); opacity:0; }}
            to   {{ transform:translateY(0);    opacity:1; }}
        }}
        .services-panel-title {{
            font-size:13px; font-weight:700; color:#C9A84C;
            text-align:center; margin-bottom:16px; letter-spacing:1px;
            text-transform:uppercase;
        }}
        .svc-close {{
            position:absolute; top:14px; right:18px;
            background:none; border:none; color:#555;
            font-size:20px; cursor:pointer; line-height:1;
        }}
        .svc-cat-label {{
            font-size:10px; letter-spacing:2px; text-transform:uppercase;
            color:#555; margin:14px 0 8px; padding-bottom:6px;
            border-bottom:1px solid #2a2a2a;
        }}
        .svc-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; }}
        .svc-card {{
            background:#222; border:1px solid #2a2a2a; border-radius:14px;
            padding:14px 12px; cursor:pointer; transition:all 0.2s; text-align:left;
        }}
        .svc-card:hover {{ border-color:#C9A84C; background:#1e1c14; }}
        .svc-card:active {{ transform:scale(0.96); }}
        .svc-icon {{ font-size:22px; margin-bottom:6px; display:block; }}
        .svc-name {{ font-size:13px; font-weight:600; color:#eee; line-height:1.3; }}
        .svc-desc {{ font-size:11px; color:#666; margin-top:3px; line-height:1.4; }}
        .svc-price {{ font-size:12px; color:#C9A84C; font-weight:700; margin-top:6px; }}
        .svc-free {{ font-size:12px; color:#4CAF50; font-weight:600; margin-top:6px; }}
        .svc-empty {{ text-align:center; color:#555; font-size:13px; padding:20px 0; }}

        .messages {{
            flex:1; overflow-y:auto; padding:16px 14px;
            display:flex; flex-direction:column; gap:12px;
        }}
        .messages::-webkit-scrollbar {{ width:4px; }}
        .messages::-webkit-scrollbar-thumb {{ background:rgba(201,168,76,0.2); border-radius:10px; }}
        .row {{ display:flex; gap:8px; align-items:flex-end; animation:slideUp 0.3s ease; }}
        .row.user {{ flex-direction:row-reverse; }}
        @keyframes slideUp {{
            from {{ opacity:0; transform:translateY(8px); }}
            to {{ opacity:1; transform:translateY(0); }}
        }}
        .avatar {{
            width:28px; height:28px; border-radius:50%; flex-shrink:0;
            display:flex; align-items:center; justify-content:center;
            font-size:14px; background:rgba(201,168,76,0.12);
        }}
        .row.user .avatar {{ display:none; }}
        .msg-wrap {{ display:flex; flex-direction:column; gap:4px; max-width:80%; }}
        .row.user .msg-wrap {{ align-items:flex-end; }}
        .msg {{
            padding:11px 15px; border-radius:18px;
            font-size:14px; line-height:1.55; word-wrap:break-word;
        }}
        .bot .msg {{
            background:#222; color:#f0f0f0; border-bottom-left-radius:5px;
        }}
        .user .msg {{
            background:linear-gradient(135deg, #C9A84C 0%, #E8C96A 100%);
            color:#1a1a1a; border-bottom-right-radius:5px; font-weight:500;
        }}
        .staff .msg {{
            background:linear-gradient(135deg, #1a3a1a 0%, #1f4a1f 100%);
            color:#6fd46f; border:1px solid #2a4a2a; border-bottom-left-radius:5px;
        }}
        .staff-label {{
            font-size:10px; color:#4CAF50; letter-spacing:0.5px; margin-left:4px;
        }}

        /* RATING */
        .rating-wrap {{
            display:flex; flex-direction:column; gap:4px; padding:4px 4px 2px;
        }}
        .star {{
            font-size:22px; cursor:pointer; opacity:0.3;
            transition:opacity 0.15s, transform 0.15s; color:#C9A84C;
        }}
        .star:hover, .star.active {{ opacity:1; transform:scale(1.15); }}
        .rating-done {{ font-size:11px; color:#4CAF50; padding:2px 4px; }}
        .review-response {{
            font-size:13px; line-height:1.6; padding:4px 0;
        }}
        .review-response.low {{ color:#E05555; }}
        .review-response.high {{ color:#4CAF50; }}
        .booking-btn {{
            display:inline-block; margin-top:10px;
            background:linear-gradient(135deg,#C9A84C,#E8C96A);
            color:#000; font-weight:700; font-size:13px;
            padding:9px 18px; border-radius:10px;
            text-decoration:none; transition:opacity 0.2s;
        }}
        .booking-btn:hover {{ opacity:0.85; }}

        /* PROACTIVE REVIEW CARD */
        .review-card {{
            background:linear-gradient(135deg,rgba(201,168,76,0.08),rgba(201,168,76,0.04));
            border:1px solid rgba(201,168,76,0.2); border-radius:16px;
            padding:18px; margin:12px 0;
            animation:slideUp 0.4s ease;
        }}
        @keyframes slideUp {{ from{{opacity:0;transform:translateY(12px)}} to{{opacity:1;transform:translateY(0)}} }}
        .review-card-title {{ font-size:15px; font-weight:700; color:#C9A84C; margin-bottom:6px; }}
        .review-card-sub {{ font-size:13px; color:#888; margin-bottom:14px; line-height:1.5; }}

        .typing {{ display:flex; gap:4px; padding:4px 0; }}
        .typing span {{
            width:7px; height:7px; border-radius:50%; background:#C9A84C;
            animation:bounce 1.2s infinite;
        }}
        .typing span:nth-child(2) {{ animation-delay:0.2s; }}
        .typing span:nth-child(3) {{ animation-delay:0.4s; }}
        @keyframes bounce {{
            0%,60%,100% {{ transform:translateY(0); opacity:0.4; }}
            30% {{ transform:translateY(-6px); opacity:1; }}
        }}
        .input-area {{
            padding:12px 14px; display:flex; gap:10px;
            border-top:1px solid rgba(255,255,255,0.06); background:#141414;
        }}
        input {{
            flex:1; background:#222; border:1px solid transparent;
            border-radius:24px; padding:12px 18px; color:white;
            font-size:14px; outline:none; font-family:inherit;
            transition:border-color 0.2s;
        }}
        input:focus {{ border-color:rgba(201,168,76,0.4); }}
        input::placeholder {{ color:#666; }}
        .send-btn {{
            width:44px; height:44px; flex-shrink:0;
            background:linear-gradient(135deg, #C9A84C 0%, #E8C96A 100%);
            border:none; border-radius:50%; cursor:pointer; font-size:17px;
            color:#1a1a1a; display:flex; align-items:center; justify-content:center;
            transition:transform 0.15s;
        }}
        .send-btn:hover {{ transform:scale(1.08); }}
        .send-btn:active {{ transform:scale(0.95); }}

        /* LIGHT THEME */
        body.light {{ background:linear-gradient(135deg, #f0f0f0 0%, #faf6ec 100%); }}
        body.light .chat-box {{ background:#fff; box-shadow:0 30px 80px rgba(0,0,0,0.12); border-color:rgba(201,168,76,0.2); }}
        body.light .bot .msg {{ background:#f2f2f2; color:#1a1a1a; }}
        body.light .room-bar {{ background:rgba(201,168,76,0.06); }}
        body.light .service-menu {{ border-bottom-color:rgba(0,0,0,0.08); }}
        body.light .service-btn {{ background:#f5f5f5; border-color:#e0e0e0; color:#666; }}
        body.light .input-area {{ border-top:1px solid #eee; background:#fff; }}
        body.light input {{ background:#f2f2f2; color:#1a1a1a; }}
        body.light input::placeholder {{ color:#999; }}
        body.light .messages {{ background:#fff; }}
        body.light .services-panel {{ background:#f5f5f5; }}
        body.light .svc-card {{ background:#fff; border-color:#e0e0e0; }}
        body.light .svc-name {{ color:#111; }}
        body.light .svc-cat-label {{ color:#999; border-bottom-color:#e0e0e0; }}
    </style>
</head>
<body>
    <div class="chat-box">
        <!-- PWA install bar -->
        <div id="install-bar">
            <span id="installBarText">📲 Install as app</span>
            <button class="install-btn" id="installBtnText" onclick="installPWA()">Install</button>
            <button class="install-dismiss" onclick="document.getElementById('install-bar').style.display='none'">✕</button>
        </div>
        <div class="chat-header">
            <button class="theme-btn" onclick="toggleTheme()" id="themeBtn">☀️ Light</button>
            <select id="langSel" onchange="setLang(this.value)"
                style="position:absolute;top:14px;left:14px;background:rgba(0,0,0,0.25);color:#fff;border:1px solid rgba(255,255,255,0.25);border-radius:8px;padding:4px 6px;font-size:12px;outline:none;cursor:pointer">
                <option value="en">🇬🇧 EN</option>
                <option value="ru">🇷🇺 RU</option>
                <option value="tr">🇹🇷 TR</option>
                <option value="uz">🇺🇿 UZ</option>
            </select>
            <div class="header-avatar">🏨</div>
            <h2>{hotel_name}</h2>
            <p><span class="status-dot"></span><span id="chatStatusLine">Concierge • AI Assistant</span></p>
        </div>
        <div class="room-bar">🚪 <span id="roomBarLabel">Room</span>: <span id="roomNum">101</span></div>

        <div class="service-menu" id="serviceMenu">
            <button class="service-btn" id="menuToggleBtn" onclick="toggleServicePanel()">🛎️ Menu</button>
            <button class="service-btn" id="quickWifi" onclick="quickAction(_L().quickWifiMsg)">📶 WiFi</button>
            <button class="service-btn" id="quickPool" onclick="quickAction(_L().quickPoolMsg)">🏊 Pool</button>
            <button class="service-btn" id="quickRestaurant" onclick="quickAction(_L().quickRestMsg)">🍽️ Restaurant</button>
            <button class="service-btn" id="quickTaxi" onclick="quickAction(_L().quickTaxiMsg)">🚖 Taxi</button>
        </div>

        <div class="messages" id="messages"></div>
        <div class="input-area">
            <input type="text" id="input" placeholder="Type a message..." onkeypress="if(event.key==='Enter') send()">
            <button class="send-btn" onclick="send()">➤</button>
        </div>

        <!-- SERVICES OVERLAY -->
        <div class="services-overlay" id="servicesOverlay" onclick="handleOverlayClick(event)">
            <div class="services-panel" id="servicesPanel">
                <button class="svc-close" onclick="toggleServicePanel()">✕</button>
                <div class="services-panel-title" id="svcPanelTitle">🛎️ Hotel Services</div>
                <div id="servicesList"><div class="svc-empty" id="svcsLoading">Loading...</div></div>
            </div>
        </div>
    </div>
    <script>
        const HOTEL_LANG = '{default_lang}';

        const CHAT_I18N = {{
            en: {{
                installBar: '📲 Install as app',
                installBtn: 'Install',
                statusLine: 'Concierge • AI Assistant',
                roomBarLabel: 'Room',
                menuBtn: '🛎️ Menu',
                quickWifi: '📶 WiFi', quickPool: '🏊 Pool',
                quickRestaurant: '🍽️ Restaurant', quickTaxi: '🚖 Taxi',
                quickWifiMsg: 'What is the WiFi password?',
                quickPoolMsg: 'What are the pool hours?',
                quickRestMsg: 'What are the restaurant hours?',
                quickTaxiMsg: 'Can you call a taxi for me?',
                placeholder: 'Type a message...',
                servicesPanelTitle: '🛎️ Hotel Services',
                servicesLoading: 'Loading...',
                servicesEmpty: 'No services configured yet',
                staffLabel: '👨‍💼 Staff',
                freeLabel: 'Free',
                orderSuffix: ' — I would like to order this',
                ratingLow: "😔 We're sorry! Our manager will contact you shortly.",
                ratingHigh: "🌟 Great! Would you like to share your experience?",
                ratingHighBooking: "📝 Leave a Review on Booking.com",
                ratingThanks: "✅ Thank you! Your feedback is valuable to us.",
                connError: "⚠️ Connection error. Please try again.",
                notifTitle: "👨‍💼 Staff",
                reviewTitle: "⭐ How Was Your Stay?",
                reviewHi: "Hello!",
                reviewSub1: "You've been our guest for 1 day. Would you rate your experience?",
                reviewSubN: "You've been our guest for {{n}} days. Would you rate your experience?",
                welcome: 'Welcome! 👋 How can I help you?',
                welcomeDemo: 'Welcome! 👋 How can I help you?',
                catLabels: {{
                    food: '🍽️ Food & Drink', housekeeping: '🧹 Housekeeping',
                    spa: '💆 Spa', transport: '🚖 Transport',
                    maintenance: '🔧 Maintenance', general: '🛎️ Other'
                }},
            }},
            ru: {{
                installBar: '📲 Установить как приложение',
                installBtn: 'Установить',
                statusLine: 'Консьерж • ИИ-ассистент',
                roomBarLabel: 'Номер',
                menuBtn: '🛎️ Меню',
                quickWifi: '📶 WiFi', quickPool: '🏊 Бассейн',
                quickRestaurant: '🍽️ Ресторан', quickTaxi: '🚖 Такси',
                quickWifiMsg: 'Какой пароль от WiFi?',
                quickPoolMsg: 'Какое расписание бассейна?',
                quickRestMsg: 'Какое расписание ресторана?',
                quickTaxiMsg: 'Можно вызвать такси?',
                placeholder: 'Напишите сообщение...',
                servicesPanelTitle: '🛎️ Услуги отеля',
                servicesLoading: 'Загрузка...',
                servicesEmpty: 'Меню услуг пока не настроено',
                staffLabel: '👨‍💼 Персонал',
                freeLabel: 'Бесплатно',
                orderSuffix: ' — хочу заказать',
                ratingLow: '😔 Сожалеем! Наш менеджер свяжется с вами в ближайшее время.',
                ratingHigh: '🌟 Отлично! Поделитесь своими впечатлениями?',
                ratingHighBooking: '📝 Оставить отзыв на Booking.com',
                ratingThanks: '✅ Спасибо! Ваш отзыв очень важен для нас.',
                connError: '⚠️ Ошибка соединения. Пожалуйста, попробуйте ещё раз.',
                notifTitle: '👨‍💼 Персонал',
                reviewTitle: '⭐ Как вам проживание?',
                reviewHi: 'Добро пожаловать!',
                reviewSub1: 'Вы уже 1 день у нас. Оцените своё пребывание?',
                reviewSubN: 'Вы уже {{n}} дней у нас. Оцените своё пребывание?',
                welcome: 'Добро пожаловать! 👋 Чем могу помочь?',
                welcomeDemo: 'Добро пожаловать! 👋 Чем могу помочь?',
                catLabels: {{
                    food: '🍽️ Питание', housekeeping: '🧹 Горничная',
                    spa: '💆 Спа', transport: '🚖 Транспорт',
                    maintenance: '🔧 Технический', general: '🛎️ Прочее'
                }},
            }},
            tr: {{
                installBar: '📲 Uygulama olarak yükle',
                installBtn: 'Yükle',
                statusLine: 'Konsiyerj • AI Asistan',
                roomBarLabel: 'Oda',
                menuBtn: '🛎️ Menü',
                quickWifi: '📶 WiFi', quickPool: '🏊 Havuz',
                quickRestaurant: '🍽️ Restoran', quickTaxi: '🚖 Taksi',
                quickWifiMsg: 'WiFi şifresi nedir?',
                quickPoolMsg: 'Havuz saatleri nedir?',
                quickRestMsg: 'Restoran saatleri nedir?',
                quickTaxiMsg: 'Taksi çağırabilir misiniz?',
                placeholder: 'Mesajınızı yazın...',
                servicesPanelTitle: '🛎️ Otel Hizmetleri',
                servicesLoading: 'Yükleniyor...',
                servicesEmpty: 'Henüz hizmet menüsü eklenmemiş',
                staffLabel: '👨‍💼 Personel',
                freeLabel: 'Ücretsiz',
                orderSuffix: ' — sipariş etmek istiyorum',
                ratingLow: '😔 Üzgünüz! Yöneticimiz hemen sizinle ilgilenecek.',
                ratingHigh: '🌟 Harika! Deneyiminizi paylaşır mısınız?',
                ratingHighBooking: "📝 Booking.com'da Yorum Yaz",
                ratingThanks: '✅ Teşekkürler! Geri bildiriminiz bizim için değerli.',
                connError: '⚠️ Bağlantı hatası. Lütfen tekrar deneyin.',
                notifTitle: '👨‍💼 Personel',
                reviewTitle: '⭐ Konaklamanızı Nasıl Buldunuz?',
                reviewHi: 'Merhaba!',
                reviewSub1: '1 gündür misafirimizsiniz. Deneyiminizi değerlendirir misiniz?',
                reviewSubN: '{{n}} gündür misafirimizsiniz. Deneyiminizi değerlendirir misiniz?',
                welcome: 'Hoş geldiniz! 👋 Size nasıl yardımcı olabilirim?',
                welcomeDemo: 'Hoş geldiniz! 👋 Size nasıl yardımcı olabilirim?',
                catLabels: {{
                    food: '🍽️ Yiyecek & İçecek', housekeeping: '🧹 Temizlik',
                    spa: '💆 Spa', transport: '🚖 Ulaşım',
                    maintenance: '🔧 Teknik', general: '🛎️ Diğer'
                }},
            }},
            uz: {{
                installBar: "📲 Ilova sifatida o'rnatish",
                installBtn: "O'rnatish",
                statusLine: "Konsiyerj • AI Yordamchi",
                roomBarLabel: "Xona",
                menuBtn: "🛎️ Menyu",
                quickWifi: "📶 WiFi", quickPool: "🏊 Hovuz",
                quickRestaurant: "🍽️ Restoran", quickTaxi: "🚖 Taksi",
                quickWifiMsg: "WiFi paroli nima?",
                quickPoolMsg: "Hovuz ish vaqti qanday?",
                quickRestMsg: "Restoran ish vaqti qanday?",
                quickTaxiMsg: "Taksi chaqira olasizmi?",
                placeholder: "Xabar yozing...",
                servicesPanelTitle: "🛎️ Mehmonxona xizmatlari",
                servicesLoading: "Yuklanmoqda...",
                servicesEmpty: "Xizmatlar hali qo'shilmagan",
                staffLabel: "👨‍💼 Xodim",
                freeLabel: "Bepul",
                orderSuffix: " — buyurtma bermoqchiman",
                ratingLow: "😔 Uzr! Menejerimiz tez orada siz bilan bog'lanadi.",
                ratingHigh: "🌟 Ajoyib! Tajribangizni ulashing?",
                ratingHighBooking: "📝 Booking.com'da sharh qoldiring",
                ratingThanks: "✅ Rahmat! Fikringiz biz uchun muhim.",
                connError: "⚠️ Ulanish xatosi. Iltimos qayta urinib ko'ring.",
                notifTitle: "👨‍💼 Xodim",
                reviewTitle: "⭐ Qolishingiz qanday bo'ldi?",
                reviewHi: "Xush kelibsiz!",
                reviewSub1: "Siz 1 kun bizning mehmonimiz siz. Tajribangizni baholaysizmi?",
                reviewSubN: "Siz {{n}} kun bizning mehmonimiz siz. Tajribangizni baholaysizmi?",
                welcome: "Xush kelibsiz! 👋 Qanday yordam bera olaman?",
                welcomeDemo: "Xush kelibsiz! 👋 Qanday yordam bera olaman?",
                catLabels: {{
                    food: "🍽️ Ovqat va ichimlik", housekeeping: "🧹 Xonadon",
                    spa: "💆 Spa", transport: "🚖 Transport",
                    maintenance: "🔧 Texnik", general: "🛎️ Boshqa"
                }},
            }},
        }};

        // Pick the UI language: saved guest choice → hotel's setting (if we have a
        // dictionary for it) → guest's browser language → English. This keeps the
        // interface in the guest's language instead of defaulting to English when
        // the hotel is set to "auto" or to a language we don't have UI strings for.
        function _pickLang() {{
            const saved = localStorage.getItem('ss_chat_lang');
            if (saved && CHAT_I18N[saved]) return saved;
            if (CHAT_I18N[HOTEL_LANG]) return HOTEL_LANG;
            const nav = (navigator.language || 'en').slice(0, 2);
            if (CHAT_I18N[nav]) return nav;
            return 'en';
        }}
        let CUR_LANG = _pickLang();
        function _L() {{ return CHAT_I18N[CUR_LANG] || CHAT_I18N.en; }}

        function setLang(code) {{
            if (!CHAT_I18N[code]) return;
            CUR_LANG = code;
            try {{ localStorage.setItem('ss_chat_lang', code); }} catch(e) {{}}
            applyChatLang();
        }}

        function applyChatLang() {{
            const sel = document.getElementById('langSel');
            if (sel) sel.value = CUR_LANG;
            const L = _L();
            const set = (id, val) => {{ const e = document.getElementById(id); if (e) e.textContent = val; }};
            set('installBarText', L.installBar);
            set('installBtnText', L.installBtn);
            set('chatStatusLine', L.statusLine);
            set('roomBarLabel', L.roomBarLabel);
            set('menuToggleBtn', L.menuBtn);
            set('quickWifi', L.quickWifi);
            set('quickPool', L.quickPool);
            set('quickRestaurant', L.quickRestaurant);
            set('quickTaxi', L.quickTaxi);
            set('svcPanelTitle', L.servicesPanelTitle);
            set('svcsLoading', L.servicesLoading);
            const inp = document.getElementById('input');
            if (inp) inp.placeholder = L.placeholder;
        }}
        applyChatLang();

        const slug = window.location.pathname.split('/')[2] || '';
        const room = new URLSearchParams(window.location.search).get('room') || '101';
        const STORAGE_KEY = 'smartstay_' + (slug || 'demo') + '_' + room;
        document.getElementById('roomNum').textContent = room;

        let messages = [];
        let lastMsgId = 0;
        let isStreaming = false;

        // ===== LOCALSTORAGE =====
        function saveHistory() {{
            try {{
                localStorage.setItem(STORAGE_KEY, JSON.stringify({{ messages, lastMsgId }}));
            }} catch(e) {{}}
        }}

        function loadHistory() {{
            try {{
                const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
                if (stored && stored.messages && stored.messages.length > 0) {{
                    messages = stored.messages;
                    lastMsgId = stored.lastMsgId || 0;
                    stored.messages.forEach(m => {{
                        addMessageToDOM(m.content, m.role, false, m.isStaff);
                    }});
                    return true;
                }}
            }} catch(e) {{}}
            return false;
        }}

        async function loadHistoryFromServer() {{
            if (!slug) return false;
            try {{
                const res = await fetch('/api/hotel/' + slug + '/room/' + encodeURIComponent(room) + '/history');
                if (!res.ok) return false;
                const msgs = await res.json();
                if (!msgs || !msgs.length) return false;
                messages = msgs.map(m => ({{
                    role: m.role === 'user' ? 'user' : 'bot',
                    content: m.message,
                    isStaff: m.role === 'staff'
                }}));
                lastMsgId = msgs[msgs.length - 1].id;
                msgs.forEach(m => {{
                    const role = m.role === 'user' ? 'user' : 'bot';
                    addMessageToDOM(m.message, role, false, m.role === 'staff');
                }});
                saveHistory();
                return true;
            }} catch(e) {{}}
            return false;
        }}

        // ===== DOM =====
        function addMessageToDOM(text, type, withRating=false, isStaff=false) {{
            const row = document.createElement('div');
            const displayType = isStaff ? 'staff' : type;
            row.className = 'row ' + displayType;

            const wrap = document.createElement('div');
            wrap.className = 'msg-wrap';

            if (isStaff) {{
                const lbl = document.createElement('span');
                lbl.className = 'staff-label';
                lbl.textContent = _L().staffLabel;
                wrap.appendChild(lbl);
            }}

            const msgDiv = document.createElement('div');
            msgDiv.className = 'msg';
            msgDiv.textContent = text;
            wrap.appendChild(msgDiv);

            if (withRating && type === 'bot') {{
                wrap.appendChild(makeRating());
            }}

            const avatar = type !== 'user' ? '<div class="avatar">' + (isStaff ? '👨‍💼' : '🤖') + '</div>' : '';
            row.innerHTML = avatar;
            row.appendChild(wrap);
            document.getElementById('messages').appendChild(row);
            scrollBottom();
            return msgDiv;
        }}

        function scrollBottom() {{
            const el = document.getElementById('messages');
            el.scrollTop = el.scrollHeight;
        }}

        // ===== RATING =====
        function makeRating(label) {{
            const wrap = document.createElement('div');
            wrap.className = 'rating-wrap';
            if (label) {{
                const lbl = document.createElement('div');
                lbl.style.cssText = 'font-size:13px;color:#888;margin-bottom:8px';
                lbl.textContent = label;
                wrap.appendChild(lbl);
            }}
            const stars = document.createElement('div');
            for (let i = 1; i <= 5; i++) {{
                const star = document.createElement('span');
                star.className = 'star';
                star.textContent = '★';
                star.dataset.val = i;
                star.onclick = function() {{
                    const val = parseInt(this.dataset.val);
                    stars.innerHTML = '<span style="color:#C9A84C;font-size:22px">' + '★'.repeat(val) + '</span>';
                    sendRating(val, wrap);
                }};
                stars.appendChild(star);
            }}
            wrap.appendChild(stars);
            return wrap;
        }}

        async function sendRating(val, wrapEl) {{
            if (!slug) return;
            try {{
                const res = await fetch('/hotel/' + slug + '/rate', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{room, rating: val}})
                }});
                const data = await res.json();
                const L = _L();
                if (wrapEl) {{
                    if (data.low) {{
                        wrapEl.innerHTML = '<div class="review-response low">' + L.ratingLow + '</div>';
                    }} else if (data.booking_url) {{
                        wrapEl.innerHTML = '<div class="review-response high">' + L.ratingHigh +
                            '<br><a href="' + data.booking_url + '" target="_blank" class="booking-btn">' + L.ratingHighBooking + '</a></div>';
                    }} else {{
                        wrapEl.innerHTML = '<div class="review-response high">' + L.ratingThanks + '</div>';
                    }}
                }}
            }} catch(e) {{}}
        }}

        // ===== SEND =====
        async function send() {{
            if (isStreaming) return;
            const input = document.getElementById('input');
            const text = input.value.trim();
            if (!text) return;

            addMessageToDOM(text, 'user');
            messages.push({{role: 'user', content: text}});
            saveHistory();
            input.value = '';
            input.disabled = true;
            isStreaming = true;

            const row = document.createElement('div');
            row.className = 'row bot';
            row.innerHTML = '<div class="avatar">🤖</div>';
            const wrap = document.createElement('div');
            wrap.className = 'msg-wrap';
            const botMsg = document.createElement('div');
            botMsg.className = 'msg';
            botMsg.innerHTML = '<div class="typing"><span></span><span></span><span></span></div>';
            wrap.appendChild(botMsg);
            row.appendChild(wrap);
            document.getElementById('messages').appendChild(row);
            scrollBottom();

            const chatUrl = slug ? '/hotel/' + slug + '/chat' : '/chat';
            try {{
                const res = await fetch(chatUrl, {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        message: text,
                        history: messages.slice(0, -1),
                        room: room
                    }})
                }});

                const reader = res.body.getReader();
                const decoder = new TextDecoder();
                let fullText = '';
                let first = true;
                let buffer = '';   // holds a partial line across chunk boundaries

                while (true) {{
                    const {{done, value}} = await reader.read();
                    if (done) break;
                    buffer += decoder.decode(value, {{stream: true}});
                    const lines = buffer.split('\\n');
                    buffer = lines.pop();   // keep the last (possibly incomplete) line
                    for (const line of lines) {{
                        if (!line.startsWith('data: ')) continue;
                        const payload = line.slice(6);
                        if (payload === '[DONE]') continue;
                        try {{
                            const data = JSON.parse(payload);
                            if (data.text) {{
                                if (first) {{ botMsg.textContent = ''; first = false; }}
                                fullText += data.text;
                                botMsg.textContent = fullText;
                                scrollBottom();
                            }}
                            if (data.error) {{
                                botMsg.textContent = '⚠️ ' + data.error;
                                botMsg.style.color = '#E05555';
                                scrollBottom();
                            }}
                        }} catch(e) {{}}
                    }}
                }}

                // Only record a real reply — don't push an empty assistant turn
                // (which would be sent back to the model on the next message).
                if (fullText) {{
                    messages.push({{role: 'assistant', content: fullText}});
                    wrap.appendChild(makeRating());
                    saveHistory();
                }}
            }} catch(e) {{
                botMsg.textContent = _L().connError;
            }}

            isStreaming = false;
            input.disabled = false;
            input.focus();
        }}

        function quickAction(text) {{
            document.getElementById('input').value = text;
            send();
        }}

        // ===== SERVICES MENU =====
        let _servicesLoaded = false;

        async function loadServices() {{
            if (!slug || _servicesLoaded) return;
            _servicesLoaded = true;
            const L = _L();
            try {{
                const res = await fetch('/api/hotel/' + slug + '/services?active_only=true');
                if (!res.ok) return;
                const svcs = await res.json();
                if (!svcs || !svcs.length) {{
                    document.getElementById('servicesList').innerHTML =
                        '<div class="svc-empty">' + L.servicesEmpty + '</div>';
                    return;
                }}

                // Group by category
                const grouped = {{}};
                svcs.forEach(s => {{
                    const cat = s.category || 'general';
                    if (!grouped[cat]) grouped[cat] = [];
                    grouped[cat].push(s);
                }});

                let html = '';
                for (const [cat, items] of Object.entries(grouped)) {{
                    html += '<div class="svc-cat-label">' + (L.catLabels[cat] || cat) + '</div>';
                    html += '<div class="svc-grid">';
                    items.forEach(s => {{
                        const price = s.price > 0
                            ? '<div class="svc-price">' + s.price.toFixed(0) + ' ' + s.currency + '</div>'
                            : '<div class="svc-free">' + L.freeLabel + '</div>';
                        const desc = s.description
                            ? '<div class="svc-desc">' + s.description + '</div>' : '';
                        html += `<div class="svc-card" onclick="orderService(${{JSON.stringify(s.name)}}, ${{JSON.stringify(s.icon)}})">
                            <span class="svc-icon">${{s.icon}}</span>
                            <div class="svc-name">${{s.name}}</div>
                            ${{desc}}${{price}}
                        </div>`;
                    }});
                    html += '</div>';
                }}
                document.getElementById('servicesList').innerHTML = html;

                // Rebuild quick chips from first 4 services
                const menu = document.getElementById('serviceMenu');
                const toggleBtn = menu.querySelector('#menuToggleBtn');
                [...menu.children].forEach(c => {{ if (c !== toggleBtn) c.remove(); }});
                svcs.slice(0, 4).forEach(s => {{
                    const btn = document.createElement('button');
                    btn.className = 'service-btn';
                    btn.textContent = s.icon + ' ' + s.name;
                    btn.onclick = () => orderService(s.name, s.icon);
                    menu.appendChild(btn);
                }});
            }} catch(e) {{ console.error('loadServices:', e); }}
        }}

        function toggleServicePanel() {{
            const overlay = document.getElementById('servicesOverlay');
            const btn = document.getElementById('menuToggleBtn');
            const isOpen = overlay.classList.toggle('open');
            btn.classList.toggle('active', isOpen);
            if (isOpen) loadServices();
        }}

        function handleOverlayClick(e) {{
            if (e.target === document.getElementById('servicesOverlay')) toggleServicePanel();
        }}

        function orderService(name, icon) {{
            document.getElementById('input').value = (icon || '🛎️') + ' ' + name + _L().orderSuffix;
            toggleServicePanel();
            document.getElementById('input').focus();
        }}

        // ===== STAFF MESSAGE POLLING =====
        async function pollStaffMessages() {{
            if (!slug) return;  // poll even when lastMsgId is 0 (since_id=0 → fetch from start)
            try {{
                const res = await fetch('/api/hotel/' + slug + '/room/' + room + '/new-messages?since_id=' + lastMsgId);
                const msgs = await res.json();
                msgs.forEach(m => {{
                    if (m.role === 'staff') {{
                        addMessageToDOM(m.message, 'bot', false, true);
                        messages.push({{role: 'assistant', content: m.message, isStaff: true}});
                        lastMsgId = Math.max(lastMsgId, m.id);
                        saveHistory();
                        notifyStaffMessage(m.message);
                    }} else if (m.role === 'bot' && m.id > lastMsgId) {{
                        lastMsgId = Math.max(lastMsgId, m.id);
                    }}
                }});
            }} catch(e) {{}}
        }}

        function notifyStaffMessage(text) {{
            if ('Notification' in window && Notification.permission === 'granted') {{
                new Notification(_L().notifTitle, {{
                    body: text,
                    icon: '/favicon.ico'
                }});
            }}
        }}

        // ===== THEME =====
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

        // ===== PROACTIVE REVIEW =====
        async function checkReviewNeeded() {{
            if (!slug || !room) return;
            try {{
                const res = await fetch('/api/hotel/' + slug + '/room/' + room + '/review-needed');
                const data = await res.json();
                if (!data.show) return;
                const L = _L();
                const container = document.getElementById('messages');
                const card = document.createElement('div');
                card.className = 'review-card';
                const escName = (data.name || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
                const hiName = escName ? escName + ', ' + L.reviewHi : L.reviewHi;
                const daySub = data.days === 1 ? L.reviewSub1 : L.reviewSubN.replace('{{n}}', data.days);
                card.innerHTML = '<div class="review-card-title">' + L.reviewTitle + '</div>' +
                    '<div class="review-card-sub">' + hiName + ' ' + daySub + '</div>';
                const ratingWrap = makeRating();
                card.appendChild(ratingWrap);
                container.insertBefore(card, container.firstChild);
                scrollBottom();
            }} catch(e) {{}}
        }}

        // ===== INIT =====
        if (localStorage.getItem('theme') === 'light') {{
            document.body.classList.add('light');
            document.getElementById('themeBtn').textContent = '🌙 Dark';
        }}

        const hasLocalHistory = loadHistory();

        (async () => {{
            if (hasLocalHistory) return;

            if (slug) {{
                const serverHistory = await loadHistoryFromServer();
                if (serverHistory) return;

                try {{
                    const res = await fetch('/api/hotel/' + slug + '/room/' + encodeURIComponent(room) + '/welcome', {{
                        method: 'POST', credentials: 'same-origin'
                    }});
                    const data = await res.json();
                    if (data.message) {{
                        addMessageToDOM(data.message, 'bot');
                        return;
                    }}
                }} catch(e) {{}}
                addMessageToDOM(_L().welcome, 'bot');
            }} else {{
                addMessageToDOM(_L().welcomeDemo, 'bot');
            }}
        }})();

        if (slug) {{
            setInterval(pollStaffMessages, 5000);
            checkReviewNeeded();
        }}

        // ===== PWA =====
        {"(function() { if ('serviceWorker' in navigator) { navigator.serviceWorker.register('/hotel/" + hotel_slug + "/sw.js').catch(()=>{}); } })();" if hotel_slug else ""}

        let _deferredInstall = null;
        window.addEventListener('beforeinstallprompt', e => {{
            e.preventDefault();
            _deferredInstall = e;
            const bar = document.getElementById('install-bar');
            if (bar) bar.style.display = 'flex';
        }});
        function installPWA() {{
            if (!_deferredInstall) return;
            _deferredInstall.prompt();
            _deferredInstall.userChoice.then(() => {{
                _deferredInstall = null;
                const bar = document.getElementById('install-bar');
                if (bar) bar.style.display = 'none';
            }});
        }}
        window.addEventListener('appinstalled', () => {{
            const bar = document.getElementById('install-bar');
            if (bar) bar.style.display = 'none';
        }});
    </script>
</body>
</html>
"""
