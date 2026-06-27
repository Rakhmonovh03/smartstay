LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>SmartStay — AI Hotel Management</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
        :root {
            --gold:#C9A84C; --gold2:#E8C96A; --bg:#0a0a0a; --bg2:#111;
            --bg3:#1a1a1a; --border:rgba(201,168,76,.12); --text:#fff;
            --text2:#aaa; --text3:#666;
        }
        html { scroll-behavior:smooth; }
        body { font-family:'Inter',sans-serif; background:var(--bg); color:var(--text); line-height:1.6; }

        /* NAV */
        nav {
            position:fixed; top:0; left:0; right:0; z-index:200;
            background:rgba(10,10,10,.9); backdrop-filter:blur(12px);
            border-bottom:1px solid var(--border);
            display:flex; align-items:center; justify-content:space-between;
            padding:0 40px; height:64px;
        }
        .nav-logo { display:flex; align-items:center; gap:10px; font-size:18px; font-weight:800; color:var(--text); text-decoration:none; }
        .nav-logo-icon { width:34px; height:34px; border-radius:9px; background:linear-gradient(135deg,var(--gold),var(--gold2)); display:flex; align-items:center; justify-content:center; font-size:18px; }
        .nav-actions { display:flex; align-items:center; gap:8px; }

        /* Language picker dropdown */
        .lang-picker { position:relative; }
        .lang-trigger {
            display:flex; align-items:center; gap:6px;
            padding:7px 12px; border-radius:10px;
            border:1px solid var(--border); background:transparent;
            color:var(--text2); font-size:13px; font-weight:600;
            cursor:pointer; font-family:inherit; transition:.15s;
            user-select:none;
        }
        .lang-trigger:hover { border-color:var(--gold); color:var(--gold); }
        .lang-menu {
            display:none; position:absolute; top:calc(100% + 8px); right:0;
            background:#1a1a1a; border:1px solid var(--border);
            border-radius:12px; overflow:hidden; min-width:160px;
            box-shadow:0 16px 40px rgba(0,0,0,.6); z-index:300;
        }
        .lang-menu.open { display:block; }
        .lang-menu button {
            display:flex; align-items:center; gap:8px; width:100%;
            padding:11px 16px; background:transparent; border:none;
            color:var(--text2); font-size:14px; font-weight:500;
            cursor:pointer; font-family:inherit; text-align:left; transition:.1s;
        }
        .lang-menu button:hover { background:rgba(201,168,76,.08); color:var(--gold); }
        .lang-menu button.active { color:var(--gold); font-weight:700; }

        .btn-ghost { padding:8px 18px; border-radius:10px; border:1px solid var(--border); background:transparent; color:var(--text); font-size:14px; font-weight:600; cursor:pointer; font-family:inherit; text-decoration:none; display:inline-flex; align-items:center; transition:.15s; }
        .btn-ghost:hover { border-color:var(--gold); color:var(--gold); }
        .btn-gold-sm { padding:8px 18px; border-radius:10px; border:none; background:linear-gradient(135deg,var(--gold),var(--gold2)); color:#1a1a1a; font-size:14px; font-weight:700; cursor:pointer; font-family:inherit; text-decoration:none; display:inline-flex; align-items:center; transition:.2s; }
        .btn-gold-sm:hover { transform:translateY(-1px); box-shadow:0 6px 24px rgba(201,168,76,.3); }

        /* HERO */
        .hero { min-height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:100px 20px 60px; position:relative; overflow:hidden; }
        .hero::before { content:''; position:absolute; top:-200px; left:50%; transform:translateX(-50%); width:800px; height:800px; background:radial-gradient(circle, rgba(201,168,76,.08) 0%, transparent 70%); pointer-events:none; }
        .hero-badge { display:inline-flex; align-items:center; gap:8px; background:rgba(201,168,76,.1); border:1px solid rgba(201,168,76,.2); border-radius:50px; padding:6px 16px; font-size:13px; color:var(--gold); margin-bottom:28px; }
        .hero h1 { font-size:clamp(36px,6vw,80px); font-weight:900; line-height:1.05; margin-bottom:20px; }
        .hero h1 span { background:linear-gradient(135deg,var(--gold),var(--gold2)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
        .hero p { font-size:clamp(16px,2vw,20px); color:var(--text2); max-width:560px; margin:0 auto 40px; }
        .hero-cta { display:flex; gap:14px; justify-content:center; flex-wrap:wrap; }
        .btn-hero { padding:15px 34px; border-radius:14px; font-size:16px; font-weight:700; cursor:pointer; font-family:inherit; text-decoration:none; transition:.2s; display:inline-flex; align-items:center; gap:8px; }
        .btn-hero-primary { background:linear-gradient(135deg,var(--gold),var(--gold2)); color:#1a1a1a; border:none; }
        .btn-hero-primary:hover { transform:translateY(-2px); box-shadow:0 12px 40px rgba(201,168,76,.35); }
        .btn-hero-secondary { background:transparent; color:var(--text); border:1px solid rgba(255,255,255,.15); }
        .btn-hero-secondary:hover { border-color:var(--gold); color:var(--gold); }
        /* Watch-video button */
        .btn-hero-video { background:rgba(255,255,255,.06); color:var(--text); border:1px solid rgba(201,168,76,.35); }
        .btn-hero-video:hover { background:rgba(201,168,76,.12); border-color:var(--gold); color:var(--gold); transform:translateY(-2px); }
        .play-ring { display:inline-flex; align-items:center; justify-content:center; width:24px; height:24px; border-radius:50%; background:var(--gold); color:#1a1a1a; font-size:11px; }
        /* Promo video modal */
        .pv-overlay { position:fixed; inset:0; background:rgba(0,0,0,.85); display:none; align-items:center; justify-content:center; z-index:1000; padding:20px; }
        .pv-overlay.open { display:flex; }
        .pv-box { width:100%; max-width:900px; position:relative; }
        .pv-frame { width:100%; aspect-ratio:16/9; border:none; border-radius:14px; background:#000; box-shadow:0 20px 80px rgba(0,0,0,.6); }
        .pv-close { position:absolute; top:-44px; right:0; background:rgba(255,255,255,.1); color:#fff; border:1px solid rgba(255,255,255,.2); width:36px; height:36px; border-radius:50%; font-size:18px; cursor:pointer; }
        .pv-close:hover { background:rgba(255,255,255,.2); }
        /* Soft hero glow for a more premium/marketing feel */
        .hero::before { content:''; position:absolute; top:-10%; left:50%; transform:translateX(-50%); width:680px; height:680px; max-width:90vw; background:radial-gradient(circle, rgba(201,168,76,.16) 0%, rgba(201,168,76,0) 70%); pointer-events:none; z-index:0; }
        .hero > * { position:relative; z-index:1; }
        .hero-stats { display:flex; gap:48px; margin-top:60px; justify-content:center; flex-wrap:wrap; }
        .hero-stat { text-align:center; }
        .hero-stat-num { font-size:32px; font-weight:800; color:var(--gold); }
        .hero-stat-label { font-size:13px; color:var(--text3); margin-top:2px; }

        /* SECTIONS */
        section { padding:100px 20px; }
        .container { max-width:1100px; margin:0 auto; }
        .section-label { font-size:12px; letter-spacing:3px; text-transform:uppercase; color:var(--gold); margin-bottom:12px; font-weight:600; }
        .section-title { font-size:clamp(28px,4vw,44px); font-weight:800; margin-bottom:16px; }
        .section-sub { font-size:16px; color:var(--text2); max-width:500px; }

        /* FEATURES */
        .features-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:20px; margin-top:56px; }
        .feature-card { background:var(--bg2); border:1px solid var(--border); border-radius:20px; padding:28px; transition:.2s; }
        .feature-card:hover { border-color:rgba(201,168,76,.3); transform:translateY(-3px); }
        .feature-icon { width:48px; height:48px; border-radius:12px; background:linear-gradient(135deg,rgba(201,168,76,.15),rgba(201,168,76,.05)); border:1px solid var(--border); display:flex; align-items:center; justify-content:center; font-size:24px; margin-bottom:16px; }
        .feature-title { font-size:16px; font-weight:700; margin-bottom:8px; }
        .feature-desc { font-size:14px; color:var(--text2); line-height:1.65; }

        /* PRICING */
        .pricing { background:var(--bg2); }
        .pricing-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:20px; margin-top:56px; max-width:960px; }
        .price-card { background:var(--bg); border:1px solid var(--border); border-radius:24px; padding:32px; position:relative; transition:.2s; }
        .price-card:hover { border-color:rgba(201,168,76,.25); }
        .price-card.popular { border-color:var(--gold); background:linear-gradient(180deg,rgba(201,168,76,.06) 0%,var(--bg) 100%); }
        .popular-badge { position:absolute; top:-12px; left:50%; transform:translateX(-50%); background:linear-gradient(135deg,var(--gold),var(--gold2)); color:#1a1a1a; font-size:11px; font-weight:800; padding:4px 16px; border-radius:20px; white-space:nowrap; }
        .trial-badge { display:inline-block; background:rgba(76,175,80,.15); border:1px solid rgba(76,175,80,.3); color:#4caf50; font-size:11px; font-weight:700; padding:3px 10px; border-radius:20px; margin-bottom:16px; }
        .price-name { font-size:14px; font-weight:600; color:var(--text2); margin-bottom:10px; }
        .price-amount { font-size:48px; font-weight:900; line-height:1; margin-bottom:4px; }
        .price-amount sup { font-size:22px; font-weight:700; vertical-align:super; color:var(--gold); }
        .price-period { font-size:13px; color:var(--text3); margin-bottom:24px; }
        .price-features { list-style:none; margin-bottom:28px; display:flex; flex-direction:column; gap:10px; }
        .price-features li { font-size:14px; color:var(--text2); display:flex; align-items:center; gap:8px; }
        .price-features li::before { content:'✓'; color:var(--gold); font-weight:700; flex-shrink:0; }
        .btn-plan { width:100%; padding:13px; border-radius:12px; font-size:14px; font-weight:700; cursor:pointer; font-family:inherit; transition:.15s; text-align:center; text-decoration:none; display:block; }
        .btn-plan-outline { background:transparent; border:1px solid var(--border); color:var(--text); }
        .btn-plan-outline:hover { border-color:var(--gold); color:var(--gold); }
        .btn-plan-gold { background:linear-gradient(135deg,var(--gold),var(--gold2)); color:#1a1a1a; border:none; }
        .btn-plan-gold:hover { transform:translateY(-2px); box-shadow:0 8px 28px rgba(201,168,76,.3); }

        /* FOOTER */
        footer { background:var(--bg); border-top:1px solid var(--border); padding:48px 20px 32px; }
        .footer-inner { max-width:1100px; margin:0 auto; }
        .footer-top { display:flex; justify-content:space-between; align-items:flex-start; gap:32px; flex-wrap:wrap; margin-bottom:40px; }
        .footer-brand p { font-size:14px; color:var(--text3); margin-top:10px; max-width:280px; }
        .footer-links h4 { font-size:12px; letter-spacing:2px; text-transform:uppercase; color:var(--text3); margin-bottom:14px; }
        .footer-links a { display:block; font-size:14px; color:var(--text2); text-decoration:none; margin-bottom:8px; transition:.15s; }
        .footer-links a:hover { color:var(--gold); }
        .footer-bottom { border-top:1px solid var(--border); padding-top:24px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }
        .footer-bottom p { font-size:13px; color:var(--text3); }

        /* RESPONSIVE */
        @media(max-width:640px) {
            nav { padding:0 16px; }
            .hero { padding:90px 16px 48px; }
            .hero-stats { gap:28px; }
            section { padding:64px 16px; }
            .footer-top { flex-direction:column; }
        }
    </style>
</head>
<body>

<!-- NAV -->
<nav>
    <a class="nav-logo" href="/">
        <div class="nav-logo-icon">🏨</div>
        SmartStay
    </a>
    <div class="nav-actions">
        <div class="lang-picker" id="langPicker">
            <button class="lang-trigger" id="langTrigger" onclick="toggleLangMenu(event)">
                🌐 <span id="currentLangLabel">EN</span> ▾
            </button>
            <div class="lang-menu" id="langMenu">
                <button onclick="setLang('en')" id="lmEn">🇺🇸 English</button>
                <button onclick="setLang('ru')" id="lmRu">🇷🇺 Русский</button>
                <button onclick="setLang('tr')" id="lmTr">🇹🇷 Türkçe</button>
                <button onclick="setLang('uz')" id="lmUz">🇺🇿 O'zbek</button>
            </div>
        </div>
        <a class="btn-ghost" href="/login" id="navLoginBtn">Login</a>
        <a class="btn-gold-sm" href="/register" id="navRegisterBtn">Register</a>
    </div>
</nav>

<!-- HERO -->
<section class="hero">
    <div class="hero-badge">✨ <span id="heroBadge">AI-Powered Hotel Management</span></div>
    <h1>
        <span id="heroTitle1">Smart Hotel</span><br>
        <span id="heroTitle2">on Autopilot</span>
    </h1>
    <p id="heroSub">24/7 AI assistant for your guests, staff management, analytics and more — all in one dashboard.</p>
    <div class="hero-cta">
        <a class="btn-hero btn-hero-primary" href="/register">
            🚀 <span id="heroCta1">Get Started Free</span>
        </a>
        <button class="btn-hero btn-hero-video" id="heroVideoBtn" onclick="openPromoVideo()" style="display:none">
            <span class="play-ring">▶</span> <span id="heroCtaVideo">Watch video</span>
        </button>
        <a class="btn-hero btn-hero-secondary" href="/login">
            <span id="heroCta2">Sign In</span> →
        </a>
    </div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-num">24/7</div>
            <div class="hero-stat-label" id="statAi">AI Assistant</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">27</div>
            <div class="hero-stat-label" id="statLang">Languages</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">30</div>
            <div class="hero-stat-label" id="statFree">Days Free Trial</div>
        </div>
    </div>
</section>

<!-- FEATURES -->
<section id="features">
    <div class="container">
        <div class="section-label" id="featLabel">Features</div>
        <div class="section-title" id="featTitle">Everything your hotel needs</div>
        <div class="section-sub" id="featSub">From guest AI chat to staff management — one platform, zero complexity.</div>

        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title" id="f1Title">AI Guest Assistant</div>
                <div class="feature-desc" id="f1Desc">Answers guest questions 24/7, knows your hotel inside out, speaks the guest's language automatically.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📋</div>
                <div class="feature-title" id="f2Title">Request Tracker</div>
                <div class="feature-desc" id="f2Desc">Guests submit requests via chat. Staff see them in a Kanban board — pending, in progress, done.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">👥</div>
                <div class="feature-title" id="f3Title">Staff Management</div>
                <div class="feature-desc" id="f3Desc">Add receptionists, housekeeping, maintenance — each with their own login and role-based access.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title" id="f4Title">Analytics Dashboard</div>
                <div class="feature-desc" id="f4Desc">Message volume, guest ratings, room occupancy — visual charts updated in real time.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <div class="feature-title" id="f5Title">Staff Chat</div>
                <div class="feature-desc" id="f5Desc">Internal team chat with department channels — General, Reception, Housekeeping, Maintenance.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <div class="feature-title" id="f6Title">Telegram & Mobile</div>
                <div class="feature-desc" id="f6Desc">Get notified on Telegram for every new message. Full mobile dashboard — works on any device.</div>
            </div>
        </div>
    </div>
</section>

<!-- PRICING -->
<section class="pricing" id="pricing">
    <div class="container">
        <div class="section-label" id="priceLabel">Pricing</div>
        <div class="section-title" id="priceTitle">Simple, transparent pricing</div>
        <div class="section-sub" id="priceSub">All plans include a 30-day free trial. No credit card required.</div>

        <div class="pricing-grid">
            <!-- Başlangıç -->
            <div class="price-card">
                <div class="trial-badge" id="trialBadge1">30 Days Free</div>
                <div class="price-name" id="plan1Name">Starter</div>
                <div class="price-amount"><sup>$</sup>299</div>
                <div class="price-period" id="planMo1">per month</div>
                <ul class="price-features">
                    <li id="p1f1">500 messages / month</li>
                    <li id="p1f2">1 property</li>
                    <li id="p1f3">AI guest chat</li>
                    <li id="p1f4">Telegram & Email alerts</li>
                    <li id="p1f5">Request management</li>
                </ul>
                <a class="btn-plan btn-plan-outline" href="/register" id="p1Cta">Start Free Trial</a>
            </div>

            <!-- Pro (popular) -->
            <div class="price-card popular">
                <div class="popular-badge" id="popularBadge">MOST POPULAR</div>
                <div class="trial-badge" id="trialBadge2">30 Days Free</div>
                <div class="price-name" id="plan2Name">Pro</div>
                <div class="price-amount"><sup>$</sup>599</div>
                <div class="price-period" id="planMo2">per month</div>
                <ul class="price-features">
                    <li id="p2f1">2,000 messages / month</li>
                    <li id="p2f2">All Starter features</li>
                    <li id="p2f3">Multi-staff roles</li>
                    <li id="p2f4">Analytics & charts</li>
                    <li id="p2f5">Staff internal chat</li>
                </ul>
                <a class="btn-plan btn-plan-gold" href="/register" id="p2Cta">Start Free Trial</a>
            </div>

            <!-- Kurumsal -->
            <div class="price-card">
                <div class="trial-badge" id="trialBadge3">30 Days Free</div>
                <div class="price-name" id="plan3Name">Premium</div>
                <div class="price-amount"><sup>$</sup>999</div>
                <div class="price-period" id="planMo3">per month</div>
                <ul class="price-features">
                    <li id="p3f1">Unlimited messages</li>
                    <li id="p3f2">Multiple properties</li>
                    <li id="p3f3">Priority support</li>
                    <li id="p3f4">Custom AI training</li>
                    <li id="p3f5">SLA guarantee</li>
                </ul>
                <a class="btn-plan btn-plan-outline" href="/register" id="p3Cta">Start Free Trial</a>
            </div>
        </div>
    </div>
</section>

<!-- FOOTER -->
<footer>
    <div class="footer-inner">
        <div class="footer-top">
            <div class="footer-brand">
                <a class="nav-logo" href="/" style="text-decoration:none">
                    <div class="nav-logo-icon">🏨</div> SmartStay
                </a>
                <p id="footerTagline">AI-powered hotel management platform for modern hospitality.</p>
            </div>
            <div class="footer-links">
                <h4 id="footerProduct">Product</h4>
                <a href="#features" id="footerFeatures">Features</a>
                <a href="#pricing" id="footerPricing">Pricing</a>
                <a href="/register" id="footerRegister">Register</a>
                <a href="/login" id="footerLogin">Login</a>
            </div>
            <div class="footer-links">
                <h4 id="footerContact">Contact</h4>
                <a href="mailto:support@smartstay.ai">support@smartstay.ai</a>
                <a href="https://t.me/smartstay_support" target="_blank">Telegram Support</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2025 SmartStay. <span id="footerRights">All rights reserved.</span></p>
        </div>
    </div>
</footer>

<script>
// ===== i18n =====
const I18N = {
    en: {
        navLogin:'Login', navRegister:'Register',
        heroBadge:'AI-Powered Hotel Management',
        heroTitle1:'Smart Hotel', heroTitle2:'on Autopilot',
        heroSub:'24/7 AI assistant for your guests, staff management, analytics and more — all in one dashboard.',
        heroCta1:'Get Started Free', heroCta2:'Sign In', heroCtaVideo:'Watch video',
        statAi:'AI Assistant', statLang:'Languages', statFree:'Days Free Trial',
        featLabel:'Features', featTitle:'Everything your hotel needs',
        featSub:'From guest AI chat to staff management — one platform, zero complexity.',
        f1Title:'AI Guest Assistant', f1Desc:"Answers guest questions 24/7, knows your hotel inside out, speaks the guest's language automatically.",
        f2Title:'Request Tracker', f2Desc:'Guests submit requests via chat. Staff see them in a Kanban board — pending, in progress, done.',
        f3Title:'Staff Management', f3Desc:'Add receptionists, housekeeping, maintenance — each with their own login and role-based access.',
        f4Title:'Analytics Dashboard', f4Desc:'Message volume, guest ratings, room occupancy — visual charts updated in real time.',
        f5Title:'Staff Chat', f5Desc:'Internal team chat with department channels — General, Reception, Housekeeping, Maintenance.',
        f6Title:'Telegram & Mobile', f6Desc:'Get notified on Telegram for every new message. Full mobile dashboard — works on any device.',
        priceLabel:'Pricing', priceTitle:'Simple, transparent pricing',
        priceSub:'All plans include a 30-day free trial. No credit card required.',
        trialBadge:'30 Days Free', popularBadge:'MOST POPULAR', planMo:'per month',
        plan1Name:'Starter', p1f1:'500 messages / month', p1f2:'1 property', p1f3:'AI guest chat', p1f4:'Telegram & Email alerts', p1f5:'Request management',
        plan2Name:'Pro', p2f1:'2,000 messages / month', p2f2:'All Starter features', p2f3:'Multi-staff roles', p2f4:'Analytics & charts', p2f5:'Staff internal chat',
        plan3Name:'Premium', p3f1:'Unlimited messages', p3f2:'Multiple properties', p3f3:'Priority support', p3f4:'Custom AI training', p3f5:'SLA guarantee',
        planCta:'Start Free Trial',
        footerTagline:'AI-powered hotel management platform for modern hospitality.',
        footerProduct:'Product', footerFeatures:'Features', footerPricing:'Pricing', footerRegister:'Register', footerLogin:'Login', footerContact:'Contact',
        footerRights:'All rights reserved.',
        lmEn:'🇺🇸 English', lmRu:'🇷🇺 Русский', lmTr:'🇹🇷 Türkçe', lmUz:"🇺🇿 O'zbek", currentLang:'EN'
    },
    ru: {
        navLogin:'Войти', navRegister:'Регистрация',
        heroBadge:'AI-управление отелем',
        heroTitle1:'Умный отель', heroTitle2:'на автопилоте',
        heroSub:'AI-ассистент для гостей 24/7, управление персоналом, аналитика и многое другое — в одном дашборде.',
        heroCta1:'Начать бесплатно', heroCta2:'Войти', heroCtaVideo:'Смотреть видео',
        statAi:'AI-ассистент', statLang:'Языка', statFree:'Дней бесплатно',
        featLabel:'Возможности', featTitle:'Всё для вашего отеля',
        featSub:'От AI-чата до управления персоналом — одна платформа, без сложностей.',
        f1Title:'AI-ассистент', f1Desc:'Отвечает на вопросы гостей 24/7, знает всё о вашем отеле, автоматически говорит на языке гостя.',
        f2Title:'Трекер запросов', f2Desc:'Гости отправляют запросы через чат. Персонал видит их в Kanban-доске — ожидает, в работе, готово.',
        f3Title:'Управление персоналом', f3Desc:'Добавьте рецепционистов, горничных, техников — каждый со своим логином и доступом по роли.',
        f4Title:'Аналитика', f4Desc:'Объём сообщений, рейтинги гостей, загрузка номеров — графики обновляются в реальном времени.',
        f5Title:'Чат персонала', f5Desc:'Внутренний чат с каналами по отделам — Общий, Рецепция, Горничные, Техника.',
        f6Title:'Telegram и мобайл', f6Desc:'Получайте уведомления в Telegram на каждое новое сообщение. Полный мобильный дашборд.',
        priceLabel:'Тарифы', priceTitle:'Простые и прозрачные цены',
        priceSub:'Все тарифы включают 30-дневный бесплатный пробный период. Без банковской карты.',
        trialBadge:'30 дней бесплатно', popularBadge:'ПОПУЛЯРНЫЙ', planMo:'в месяц',
        plan1Name:'Стартовый', p1f1:'500 сообщений / месяц', p1f2:'1 объект', p1f3:'AI-чат для гостей', p1f4:'Telegram и Email уведомления', p1f5:'Управление запросами',
        plan2Name:'Про', p2f1:'2 000 сообщений / месяц', p2f2:'Всё из Стартового', p2f3:'Роли для персонала', p2f4:'Аналитика и графики', p2f5:'Чат персонала',
        plan3Name:'Премиум', p3f1:'Безлимитные сообщения', p3f2:'Несколько объектов', p3f3:'Приоритетная поддержка', p3f4:'Настройка AI', p3f5:'Гарантия SLA',
        planCta:'Начать бесплатно',
        footerTagline:'AI-платформа управления отелем для современного гостиничного бизнеса.',
        footerProduct:'Продукт', footerFeatures:'Возможности', footerPricing:'Тарифы', footerRegister:'Регистрация', footerLogin:'Войти', footerContact:'Контакты',
        footerRights:'Все права защищены.',
        lmEn:'🇺🇸 English', lmRu:'🇷🇺 Русский', lmTr:'🇹🇷 Türkçe', lmUz:"🇺🇿 O'zbek", currentLang:'RU'
    },
    tr: {
        navLogin:'Giriş', navRegister:'Kayıt Ol',
        heroBadge:'AI Destekli Otel Yönetimi',
        heroTitle1:'Akıllı Otel', heroTitle2:'Otomatik Pilot',
        heroSub:'Misafirleriniz için 7/24 AI asistanı, personel yönetimi, analitik ve daha fazlası — hepsi tek panelde.',
        heroCta1:'Ücretsiz Başla', heroCta2:'Giriş Yap', heroCtaVideo:'Videoyu izle',
        statAi:'AI Asistanı', statLang:'Dil', statFree:'Gün Ücretsiz Deneme',
        featLabel:'Özellikler', featTitle:'Otelinizin ihtiyacı olan her şey',
        featSub:'Misafir AI sohbetinden personel yönetimine — tek platform, sıfır karmaşıklık.',
        f1Title:'AI Misafir Asistanı', f1Desc:'Misafir sorularını 7/24 yanıtlar, otelinizi içten dışa tanır, misafirin diliyle otomatik konuşur.',
        f2Title:'Talep Takipçisi', f2Desc:'Misafirler sohbet yoluyla talepte bulunur. Personel bunları Kanban panosunda görür.',
        f3Title:'Personel Yönetimi', f3Desc:'Resepsiyonist, temizlik, teknik ekip — her biri kendi girişi ve rol tabanlı erişimiyle.',
        f4Title:'Analitik Paneli', f4Desc:'Mesaj hacmi, misafir derecelendirmeleri, oda doluluk oranı — gerçek zamanlı grafikler.',
        f5Title:'Personel Sohbeti', f5Desc:'Departman kanallarıyla dahili ekip sohbeti — Genel, Resepsiyon, Temizlik, Teknik.',
        f6Title:'Telegram ve Mobil', f6Desc:'Her yeni mesaj için Telegram bildirimi alın. Tam mobil panel — her cihazda çalışır.',
        priceLabel:'Fiyatlandırma', priceTitle:'Basit, şeffaf fiyatlandırma',
        priceSub:'Tüm planlar 30 günlük ücretsiz deneme içerir. Kredi kartı gerekmez.',
        trialBadge:'30 Gün Ücretsiz', popularBadge:'EN POPÜLER', planMo:'aylık',
        plan1Name:'Başlangıç', p1f1:'500 mesaj / ay', p1f2:'1 mülk', p1f3:'AI misafir sohbeti', p1f4:'Telegram ve Email bildirimleri', p1f5:'Talep yönetimi',
        plan2Name:'Pro', p2f1:'2.000 mesaj / ay', p2f2:'Tüm Başlangıç özellikleri', p2f3:'Çoklu personel rolleri', p2f4:'Analitik ve grafikler', p2f5:'Personel sohbeti',
        plan3Name:'Premium', p3f1:'Sınırsız mesaj', p3f2:'Birden fazla mülk', p3f3:'Öncelikli destek', p3f4:'Özel AI eğitimi', p3f5:'SLA garantisi',
        planCta:'Ücretsiz Denemeyi Başlat',
        footerTagline:'Modern konaklama için AI destekli otel yönetim platformu.',
        footerProduct:'Ürün', footerFeatures:'Özellikler', footerPricing:'Fiyatlar', footerRegister:'Kayıt Ol', footerLogin:'Giriş', footerContact:'İletişim',
        footerRights:'Tüm hakları saklıdır.',
        lmEn:'🇺🇸 English', lmRu:'🇷🇺 Русский', lmTr:'🇹🇷 Türkçe', lmUz:"🇺🇿 O'zbek", currentLang:'TR'
    },
    uz: {
        navLogin:'Kirish', navRegister:"Ro'yxatdan o'tish",
        heroBadge:"AI-Asosida Mehmonxona Boshqaruvi",
        heroTitle1:'Aqlli Mehmonxona', heroTitle2:'Avtopilatda',
        heroSub:"Mehmonlaringiz uchun 24/7 AI yordamchi, xodimlarni boshqarish, analitika va boshqalar — bitta panelda.",
        heroCta1:'Bepul Boshlash', heroCta2:'Kirish', heroCtaVideo:'Videoni ko‘rish',
        statAi:'AI Yordamchi', statLang:'Tillar', statFree:'Kun Bepul Sinov',
        featLabel:'Imkoniyatlar', featTitle:"Mehmonxonangizga kerak bo'lgan hamma narsa",
        featSub:"Mehmon AI chatidan xodimlarni boshqarishga qadar — bitta platforma, hech qanday murakkablik yo'q.",
        f1Title:'AI Mehmon Yordamchisi', f1Desc:"Mehmon savollariga 24/7 javob beradi, mehmonxonangizni ichidan biladi, mehmon tilida avtomatik gapiradi.",
        f2Title:"So'rovlar Kuzatuvchisi", f2Desc:"Mehmonlar chat orqali so'rov yuboradi. Xodimlar ularni Kanban taxtasida ko'radi.",
        f3Title:"Xodimlarni Boshqarish", f3Desc:"Resepsionistlar, tozalovchilar, texniklar — har biri o'z login va rol asosidagi kirish bilan.",
        f4Title:'Analitika Paneli', f4Desc:"Xabarlar hajmi, mehmon reytinglari, xona bandligi — real vaqtda yangilanadigan grafiklar.",
        f5Title:'Xodimlar Chati', f5Desc:"Bo'limlar bo'yicha kanallar bilan ichki jamoa chati — Umumiy, Retseptsiya, Tozalovchilar, Texnika.",
        f6Title:'Telegram va Mobil', f6Desc:"Har yangi xabar uchun Telegram bildirishnomalarini oling. To'liq mobil panel.",
        priceLabel:'Narxlar', priceTitle:'Oddiy, shaffof narxlar',
        priceSub:"Barcha rejalar 30 kunlik bepul sinovni o'z ichiga oladi. Kredit karta shart emas.",
        trialBadge:'30 Kun Bepul', popularBadge:'ENG MASHHUR', planMo:'oyiga',
        plan1Name:"Boshlang'ich", p1f1:'500 xabar / oy', p1f2:'1 obyekt', p1f3:'AI mehmon chati', p1f4:'Telegram va Email bildirishnomalar', p1f5:"So'rovlarni boshqarish",
        plan2Name:'Pro', p2f1:'2 000 xabar / oy', p2f2:"Barcha Boshlang'ich imkoniyatlar", p2f3:"Ko'p xodim rollari", p2f4:'Analitika va grafiklar', p2f5:'Xodimlar chati',
        plan3Name:'Premium', p3f1:'Cheksiz xabarlar', p3f2:'Bir nechta obyekt', p3f3:"Ustuvor qo'llab-quvvatlash", p3f4:"Maxsus AI o'qitish", p3f5:'SLA kafolati',
        planCta:'Bepul Sinovni Boshlash',
        footerTagline:'Zamonaviy mehmonxona uchun AI asosidagi boshqaruv platformasi.',
        footerProduct:'Mahsulot', footerFeatures:'Imkoniyatlar', footerPricing:'Narxlar', footerRegister:"Ro'yxatdan o'tish", footerLogin:'Kirish', footerContact:'Aloqa',
        footerRights:'Barcha huquqlar himoyalangan.',
        lmEn:'🇺🇸 English', lmRu:'🇷🇺 Русский', lmTr:'🇹🇷 Türkçe', lmUz:"🇺🇿 O'zbek", currentLang:'UZ'
    }
};

let currentLang = localStorage.getItem('ss_lang') || navigator.language.slice(0,2) || 'en';
if (!I18N[currentLang]) currentLang = 'en';

// IDs to translate (id → i18n key, same name)
const TRANS_IDS = [
    'navLoginBtn','navRegisterBtn','heroBadge','heroTitle1','heroTitle2','heroSub',
    'heroCta1','heroCta2','heroCtaVideo','statAi','statLang','statFree',
    'featLabel','featTitle','featSub',
    'f1Title','f1Desc','f2Title','f2Desc','f3Title','f3Desc',
    'f4Title','f4Desc','f5Title','f5Desc','f6Title','f6Desc',
    'priceLabel','priceTitle','priceSub','popularBadge',
    'plan1Name','p1f1','p1f2','p1f3','p1f4','p1f5',
    'plan2Name','p2f1','p2f2','p2f3','p2f4','p2f5',
    'plan3Name','p3f1','p3f2','p3f3','p3f4','p3f5',
    'footerTagline','footerProduct','footerFeatures','footerPricing',
    'footerRegister','footerLogin','footerContact','footerRights',
    'lmEn','lmRu','lmTr','lmUz','currentLangLabel'
];

// Per-element key mapping where id != key
const KEY_MAP = {
    navLoginBtn: 'navLogin', navRegisterBtn: 'navRegister',
    currentLangLabel: 'currentLang'
};
// Trial badges & plan CTAs
const REPEAT_MAP = {
    trialBadge1:'trialBadge', trialBadge2:'trialBadge', trialBadge3:'trialBadge',
    planMo1:'planMo', planMo2:'planMo', planMo3:'planMo',
    p1Cta:'planCta', p2Cta:'planCta', p3Cta:'planCta'
};

function applyLang() {
    const L = I18N[currentLang] || I18N.en;
    TRANS_IDS.forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;
        const key = KEY_MAP[id] || id;
        if (L[key] !== undefined) el.textContent = L[key];
    });
    Object.entries(REPEAT_MAP).forEach(([id, key]) => {
        const el = document.getElementById(id);
        if (el && L[key] !== undefined) el.textContent = L[key];
    });
    // Update active state in dropdown
    ['en','ru','tr','uz'].forEach(l => {
        const btn = document.getElementById('lm' + l.charAt(0).toUpperCase() + l.slice(1));
        if (btn) btn.classList.toggle('active', l === currentLang);
    });
}

function setLang(lang) {
    if (!I18N[lang]) return;
    currentLang = lang;
    localStorage.setItem('ss_lang', lang);
    applyLang();
    closeLangMenu();
}

function toggleLangMenu(e) {
    e.stopPropagation();
    document.getElementById('langMenu').classList.toggle('open');
}
function closeLangMenu() {
    document.getElementById('langMenu').classList.remove('open');
}

document.addEventListener('click', function(e) {
    if (!document.getElementById('langPicker').contains(e.target)) {
        closeLangMenu();
    }
});

applyLang();

// ===== PROMO VIDEO =====
let _promoUrl = '';
function _toEmbed(url) {
    // YouTube watch / youtu.be / shorts → embed URL; else return null (use <video>)
    let m = url.match(/(?:youtube\.com\/(?:watch\?v=|shorts\/)|youtu\.be\/)([A-Za-z0-9_-]{6,})/);
    if (m) return 'https://www.youtube.com/embed/' + m[1] + '?autoplay=1&rel=0';
    if (url.includes('vimeo.com/')) {
        const id = url.split('vimeo.com/')[1].split(/[?#/]/)[0];
        if (id) return 'https://player.vimeo.com/video/' + id + '?autoplay=1';
    }
    return null;
}
function openPromoVideo() {
    if (!_promoUrl) return;
    const box = document.getElementById('pvBox');
    const embed = _toEmbed(_promoUrl);
    if (embed) {
        box.innerHTML = '<iframe class="pv-frame" src="' + embed + '" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>';
    } else {
        box.innerHTML = '<video class="pv-frame" src="' + _promoUrl + '" controls autoplay playsinline></video>';
    }
    box.insertAdjacentHTML('beforeend', '<button class="pv-close" onclick="closePromoVideo()">✕</button>');
    document.getElementById('pvOverlay').classList.add('open');
}
function closePromoVideo() {
    document.getElementById('pvOverlay').classList.remove('open');
    document.getElementById('pvBox').innerHTML = '';  // stop playback
}
fetch('/api/landing-config').then(r => r.json()).then(d => {
    if (d && d.promo_video) {
        _promoUrl = d.promo_video;
        const btn = document.getElementById('heroVideoBtn');
        if (btn) btn.style.display = 'inline-flex';
    }
}).catch(() => {});
</script>

<!-- PROMO VIDEO MODAL -->
<div class="pv-overlay" id="pvOverlay" onclick="if(event.target===this)closePromoVideo()">
    <div class="pv-box" id="pvBox"></div>
</div>
</body>
</html>
"""

def get_landing_html():
    return LANDING_HTML
