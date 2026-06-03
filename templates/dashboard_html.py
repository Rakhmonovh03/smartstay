DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{hotel_name} — Панель</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: sans-serif; background:#0a0a0a; color:white; }}
        
        /* SIDEBAR */
        .sidebar {{
            position: fixed; left:0; top:0; bottom:0; width:240px;
            background:#111; border-right:1px solid rgba(201,168,76,0.15);
            padding:24px 0; z-index:100;
        }}
        .sidebar-logo {{
            padding:0 24px 24px;
            border-bottom:1px solid rgba(255,255,255,0.06);
            margin-bottom:24px;
        }}
        .sidebar-logo h2 {{
            font-size:16px; font-weight:700; color:#C9A84C;
        }}
        .sidebar-logo p {{ font-size:12px; color:#555; margin-top:2px; }}
        .nav-item {{
            display:flex; align-items:center; gap:12px;
            padding:12px 24px; font-size:14px; color:#888;
            cursor:pointer; transition:all 0.2s;
            text-decoration:none;
        }}
        .nav-item:hover {{ background:rgba(255,255,255,0.04); color:#fff; }}
        .nav-item.active {{ background:rgba(201,168,76,0.1); color:#C9A84C; border-right:2px solid #C9A84C; }}
        .nav-icon {{ font-size:16px; width:20px; text-align:center; }}

        /* MAIN */
        .main {{ margin-left:240px; padding:32px; }}
        .page-header {{
            display:flex; justify-content:space-between; align-items:center;
            margin-bottom:32px;
        }}
        .page-title {{ font-size:22px; font-weight:700; color:#C9A84C; }}
        .page-sub {{ font-size:13px; color:#555; margin-top:4px; }}
        .header-btns {{ display:flex; gap:10px; }}
        .btn {{ padding:10px 20px; border-radius:8px; font-size:13px; font-weight:500; cursor:pointer; border:none; transition:all 0.2s; }}
        .btn-gold {{ background:#C9A84C; color:#000; }}
        .btn-gold:hover {{ background:#E8C96A; }}
        .btn-dark {{ background:#1a1a1a; color:#fff; border:1px solid #333; }}
        .btn-dark:hover {{ background:#222; }}
        .btn-red {{ background:rgba(224,85,85,0.15); color:#E05555; border:1px solid rgba(224,85,85,0.3); }}

        /* STATS */
        .stats {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:32px; }}
        .stat {{
            background:#111; border-radius:12px; padding:24px;
            border:1px solid rgba(255,255,255,0.05);
            position:relative; overflow:hidden;
        }}
        .stat::before {{
            content:''; position:absolute; bottom:0; left:0; right:0; height:3px;
            background:var(--accent, #C9A84C);
        }}
        .stat.red {{ --accent: #E05555; }}
        .stat.green {{ --accent: #4CAF50; }}
        .stat.blue {{ --accent: #5B8DEF; }}
        .stat-icon {{ font-size:24px; margin-bottom:12px; }}
        .stat-num {{ font-size:36px; font-weight:900; color:#C9A84C; line-height:1; }}
        .stat.red .stat-num {{ color:#E05555; }}
        .stat.green .stat-num {{ color:#4CAF50; }}
        .stat.blue .stat-num {{ color:#5B8DEF; }}
        .stat-label {{ font-size:12px; color:#555; margin-top:8px; }}

        /* FILTERS */
        .filter-bar {{ display:flex; gap:8px; margin-bottom:20px; align-items:center; }}
        .filter {{
            padding:7px 18px; border-radius:20px; font-size:12px;
            cursor:pointer; border:1px solid #333; background:#111; color:#888;
            transition:all 0.2s;
        }}
        .filter:hover {{ border-color:#C9A84C; color:#C9A84C; }}
        .filter.active {{ background:#C9A84C; color:#000; border-color:#C9A84C; font-weight:600; }}

        /* TABLE */
        .table-wrap {{
            background:#111; border-radius:12px;
            border:1px solid rgba(255,255,255,0.05);
            overflow:hidden;
        }}
        table {{ width:100%; border-collapse:collapse; }}
        th {{
            background:rgba(201,168,76,0.1); color:#C9A84C;
            padding:14px 16px; text-align:left; font-size:12px;
            letter-spacing:1px; text-transform:uppercase;
            border-bottom:1px solid rgba(201,168,76,0.15);
        }}
        td {{ padding:14px 16px; border-bottom:1px solid rgba(255,255,255,0.04); font-size:14px; }}
        tr:last-child td {{ border-bottom:none; }}
        tr:hover td {{ background:rgba(255,255,255,0.02); }}
        tr.urgent-row td {{ background:rgba(224,85,85,0.05); }}
        tr.urgent-row:hover td {{ background:rgba(224,85,85,0.1); }}

        .badge {{ display:inline-flex; align-items:center; gap:6px; padding:5px 12px; border-radius:20px; font-size:12px; font-weight:500; }}
        .badge-urgent {{ background:rgba(224,85,85,0.15); color:#E05555; border:1px solid rgba(224,85,85,0.3); }}
        .badge-normal {{ background:rgba(76,175,80,0.15); color:#4CAF50; border:1px solid rgba(76,175,80,0.3); }}
        .badge-user {{ background:rgba(91,141,239,0.15); color:#5B8DEF; border:1px solid rgba(91,141,239,0.3); }}
        .badge-bot {{ background:rgba(201,168,76,0.15); color:#C9A84C; border:1px solid rgba(201,168,76,0.3); }}
        .room-tag {{
            background:#1a1a1a; border:1px solid #333;
            padding:4px 10px; border-radius:6px; font-size:12px; color:#C9A84C;
        }}

        /* POPUP */
        @keyframes slideIn {{
            from {{ transform:translateX(100px); opacity:0; }}
            to {{ transform:translateX(0); opacity:1; }}
        }}

        /* LIVE indicator */
        .live-dot {{
            display:inline-block; width:8px; height:8px; border-radius:50%;
            background:#4CAF50; margin-right:6px;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0%,100% {{ opacity:1; transform:scale(1); }}
            50% {{ opacity:0.4; transform:scale(0.8); }}
        }}

        .empty-state {{
            text-align:center; padding:60px 20px; color:#444;
        }}
        .empty-state .icon {{ font-size:48px; margin-bottom:16px; }}
        .empty-state p {{ font-size:14px; }}

        /* CHARTS */
        .charts-grid {{
            display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:32px;
        }}
        .chart-card {{
            background:#111; border-radius:12px; padding:24px;
            border:1px solid rgba(255,255,255,0.05);
        }}
        .chart-title {{ font-size:13px; color:#888; margin-bottom:16px; letter-spacing:1px; text-transform:uppercase; }}
        .chart-wrap {{ height:160px; display:flex; align-items:flex-end; gap:8px; }}
        .bar-item {{ flex:1; display:flex; flex-direction:column; align-items:center; gap:6px; }}
        .bar-fill {{
            width:100%; border-radius:4px 4px 0 0;
            min-height:4px; transition:height 0.5s ease;
            position:relative;
        }}
        .bar-fill:hover::after {{
            content: attr(data-value);
            position:absolute; top:-24px; left:50%; transform:translateX(-50%);
            background:#333; color:white; padding:2px 8px; border-radius:4px; font-size:11px;
            white-space:nowrap;
        }}
        .bar-label {{ font-size:10px; color:#555; text-align:center; }}
        .top-rooms {{ display:flex; flex-direction:column; gap:10px; }}
        .room-bar-item {{ display:flex; align-items:center; gap:12px; }}
        .room-bar-name {{ font-size:13px; color:#C9A84C; width:60px; flex-shrink:0; }}
        .room-bar-track {{ flex:1; background:rgba(255,255,255,0.05); border-radius:4px; height:8px; overflow:hidden; }}
        .room-bar-fill {{ height:100%; border-radius:4px; background:linear-gradient(90deg, #C9A84C, #E8C96A); transition:width 0.5s ease; }}
        .room-bar-count {{ font-size:12px; color:#555; width:30px; text-align:right; }}

        /* MOBILE */
        @media (max-width: 768px) {{
            .sidebar {{
                position: fixed; bottom:0; top:auto; left:0; right:0; width:100%;
                height:64px; flex-direction:row;
                border-right:none; border-top:1px solid rgba(201,168,76,0.15);
                padding:0; display:flex; align-items:center; justify-content:space-around;
                z-index:200;
            }}
            .sidebar-logo {{ display:none; }}
            .nav-item {{
                flex-direction:column; gap:4px; padding:8px 12px;
                font-size:10px; border-right:none !important;
                border-top:2px solid transparent;
            }}
            .nav-item.active {{ border-top:2px solid #C9A84C; border-right:none; background:none; }}
            .nav-item .nav-icon {{ font-size:20px; }}
            .sidebar > div:last-child {{ display:none; }}
            .main {{
                margin-left:0; padding:16px; padding-bottom:80px;
            }}
            .page-header {{ flex-direction:column; gap:12px; align-items:flex-start; }}
            .header-btns {{ width:100%; display:flex; }}
            .header-btns .btn {{ flex:1; }}
            .stats {{
                grid-template-columns:1fr 1fr;
                gap:12px;
            }}
            .stat {{ padding:16px; }}
            .stat-num {{ font-size:28px; }}
            .charts-grid {{ grid-template-columns:1fr; }}
            .filter-bar {{ flex-wrap:wrap; }}
            table {{ font-size:12px; }}
            th {{ padding:10px 8px; font-size:10px; }}
            td {{ padding:10px 8px; }}
            .badge {{ padding:3px 8px; font-size:11px; }}
            .room-tag {{ font-size:11px; }}
        }}

        @media (max-width: 480px) {{
            .stats {{ grid-template-columns:1fr 1fr; }}
            .page-title {{ font-size:16px; }}
        }}
    </style>
</head>
<body>
    <!-- SIDEBAR -->
    <div class="sidebar">
        <div class="sidebar-logo">
            <h2>🏨 SmartStay AI</h2>
            <p id="hotelName">Yükleniyor...</p>
        </div>
        <a class="nav-item active" onclick="filterMessages('all', this)">
            <span class="nav-icon">📊</span> Tüm Mesajlar
        </a>
        <a class="nav-item" onclick="filterMessages('urgent', this)">
            <span class="nav-icon">🔴</span> Acil Talepler
        </a>
        <a class="nav-item" onclick="filterMessages('user', this)">
            <span class="nav-icon">👤</span> Misafir Mesajları
        </a>
        <a class="nav-item" onclick="filterMessages('bot', this)">
            <span class="nav-icon">🤖</span> AI Yanıtları
        </a>
        <div style="position:absolute; bottom:24px; left:0; right:0; padding:0 16px;">
            <a class="nav-item" onclick="goToEdit()" style="border-radius:8px;">
                <span class="nav-icon">⚙️</span> Ayarlar
            </a>
            <a class="nav-item" onclick="goToQR()" style="border-radius:8px;">
                <span class="nav-icon">📱</span> QR Kodlar
            </a>
        </div>
    </div>

    <!-- MAIN -->
    <div class="main">
        <div class="page-header">
            <div>
                <div class="page-title" id="pageTitle">Панель менеджера</div>
                <div class="page-sub">
                    <span class="live-dot"></span>
                    Canlı • Her 3 saniyede güncellenir
                </div>
            </div>
            <div class="header-btns">
                <button class="btn btn-dark" onclick="markRead()">✅ Okundu</button>
                <button class="btn btn-dark" onclick="exportExcel()">📥 Excel</button>
                <button class="btn btn-gold" onclick="location.reload()">🔄 Yenile</button>
            </div>
        </div>

        <div class="charts-grid" id="chartsGrid" style="display:none">
            <div class="chart-card">
                <div class="chart-title">📈 Son 7 Gün — Mesajlar</div>
                <div class="chart-wrap" id="chartBars"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">🏆 En Aktif Odalar</div>
                <div class="top-rooms" id="topRooms"></div>
            </div>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-icon">💬</div>
                <div class="stat-num" id="statTotal">—</div>
                <div class="stat-label">Toplam Mesaj</div>
            </div>
            <div class="stat red">
                <div class="stat-icon">🔴</div>
                <div class="stat-num" id="statUrgent">—</div>
                <div class="stat-label">Acil Talep</div>
            </div>
            <div class="stat green">
                <div class="stat-icon">🚪</div>
                <div class="stat-num" id="statRooms">—</div>
                <div class="stat-label">Aktif Oda</div>
            </div>
            <div class="stat blue">
                <div class="stat-icon">📬</div>
                <div class="stat-num" id="statUnread">—</div>
                <div class="stat-label">Okunmamış</div>
            </div>
        </div>

        <div class="filter-bar">
            <span style="font-size:12px; color:#555; margin-right:4px;">Filtre:</span>
            <button class="filter active" onclick="filterMessages('all', this)">Tümü</button>
            <button class="filter" onclick="filterMessages('urgent', this)">🔴 Acil</button>
            <button class="filter" onclick="filterMessages('user', this)">👤 Misafir</button>
            <button class="filter" onclick="filterMessages('bot', this)">🤖 AI</button>
            <span id="unreadBadge" style="margin-left:auto"></span>
        </div>

        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Öncelik</th>
                        <th>Oda</th>
                        <th>Kim</th>
                        <th>Mesaj</th>
                        <th>Saat</th>
                    </tr>
                </thead>
                <tbody id="tbody"></tbody>
            </table>
        </div>
    </div>

    <script>
        let allData = [];
        let currentFilter = 'all';
        let lastUrgentCount = 0;
        const slug = window.location.pathname.split('/')[2] || '';
        const apiUrl = slug
            ? window.location.pathname.replace('/dashboard', '').replace('/hotel/', '/api/hotel/') + '/messages'
            : '/api/messages';
        const markReadUrl = slug
            ? window.location.pathname.replace('/dashboard', '').replace('/hotel/', '/api/hotel/') + '/mark-read'
            : '/api/mark-read';

        function loadData() {{
            fetch(apiUrl)
                .then(r => r.json())
                .then(data => {{
                    allData = data;
                    updateStats(data);
                    renderTable(currentFilter === 'all' ? data :
                        currentFilter === 'urgent' ? data.filter(m => m.priority === 'urgent') :
                        data.filter(m => m.role === currentFilter));
                    checkUrgentSound(data);
                }});
        }}

        function updateStats(data) {{
            const urgent = data.filter(m => m.priority === 'urgent').length;
            const rooms = new Set(data.map(m => m.room)).size;
            const unread = data.filter(m => m.is_read === 0 && m.role === 'user').length;

            document.getElementById('statTotal').textContent = data.length;
            document.getElementById('statUrgent').textContent = urgent;
            document.getElementById('statRooms').textContent = rooms;
            document.getElementById('statUnread').textContent = unread;

            document.getElementById('unreadBadge').innerHTML = unread > 0
                ? `<span style="background:#E05555;color:white;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600">${{unread}} yeni</span>`
                : '';
        }}

        function renderTable(data) {{
            if (data.length === 0) {{
                document.getElementById('tbody').innerHTML = `
                    <tr><td colspan="5">
                        <div class="empty-state">
                            <div class="icon">💬</div>
                            <p>Henüz mesaj yok</p>
                        </div>
                    </td></tr>`;
                return;
            }}
            document.getElementById('tbody').innerHTML = data.map(m => `
                <tr class="${{m.priority === 'urgent' ? 'urgent-row' : ''}}">
                    <td>${{m.priority === 'urgent'
                        ? '<span class="badge badge-urgent">🔴 Acil</span>'
                        : '<span class="badge badge-normal">🟢 Normal</span>'}}</td>
                    <td><span class="room-tag">🚪 ${{m.room}}</span></td>
                    <td>${{m.role === 'user'
                        ? '<span class="badge badge-user">👤 Misafir</span>'
                        : '<span class="badge badge-bot">🤖 AI</span>'}}</td>
                    <td style="max-width:400px">${{m.message}}</td>
                    <td style="color:#555;font-size:12px;white-space:nowrap">${{m.created_at}}</td>
                </tr>
            `).join('');
        }}

        function filterMessages(filter, btn) {{
            currentFilter = filter;
            document.querySelectorAll('.filter, .nav-item').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            renderTable(filter === 'all' ? allData :
                filter === 'urgent' ? allData.filter(m => m.priority === 'urgent') :
                allData.filter(m => m.role === filter));
        }}

        function markRead() {{
            fetch(markReadUrl, {{method:'POST'}}).then(() => loadData());
        }}

        function goToEdit() {{
            if (slug) window.location.href = '/hotel/' + slug + '/edit';
        }}

        function goToQR() {{
            if (slug) window.open('/hotel/' + slug + '/qrcodes');
            else window.open('/qrcodes');
        }}

        function exportExcel() {{
            if (slug) {{
                window.location.href = '/api/hotel/' + slug + '/export';
            }}
        }}

        function checkUrgentSound(data) {{
            const urgentCount = data.filter(m => m.priority === 'urgent' && m.is_read === 0).length;
            if (urgentCount > lastUrgentCount) {{
                playAlert();
                const msg = data.find(m => m.priority === 'urgent' && m.is_read === 0);
                showPopup(msg);
                sendPushNotification(msg);
            }}
            lastUrgentCount = urgentCount;
        }}

        function sendPushNotification(msg) {{
            if (!msg) return;
            if (!('Notification' in window)) return;
            if (Notification.permission === 'granted') {{
                new Notification('🔴 ACİL TALEP!', {{
                    body: `Oda ${{msg.room}}: ${{msg.message}}`,
                    icon: '/favicon.ico',
                    badge: '/favicon.ico',
                    vibrate: [200, 100, 200]
                }});
            }} else if (Notification.permission !== 'denied') {{
                Notification.requestPermission().then(permission => {{
                    if (permission === 'granted') {{
                        new Notification('🔴 ACİL TALEP!', {{
                            body: `Oda ${{msg.room}}: ${{msg.message}}`,
                            icon: '/favicon.ico'
                        }});
                    }}
                }});
            }}
        }}

        function playAlert() {{
            try {{
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                [0, 0.3, 0.6].forEach(delay => {{
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
                }});
            }} catch(e) {{}}
        }}

        function showPopup(msg) {{
            if (!msg) return;
            const popup = document.createElement('div');
            popup.style.cssText = `
                position:fixed; top:20px; right:20px; z-index:9999;
                background:#E05555; color:white; padding:20px 24px;
                border-radius:12px; font-size:15px; font-weight:500;
                box-shadow:0 8px 32px rgba(224,85,85,0.4);
                animation:slideIn 0.3s ease; max-width:320px; line-height:1.6;
                cursor:pointer;
            `;
            popup.innerHTML = `
                🔴 <b>ACİL TALEP!</b><br>
                🚪 Oda ${{msg.room}}<br>
                💬 ${{msg.message}}<br>
                <small style="opacity:0.8">Kapatmak için tıklayın</small>
            `;
            popup.onclick = () => popup.remove();
            document.body.appendChild(popup);
            setTimeout(() => popup.remove(), 8000);
        }}

        // Hotel name
        if (slug) {{
            fetch('/api/hotel/' + slug + '/info')
                .then(r => r.json())
                .then(d => {{
                    document.getElementById('hotelName').textContent = d.name || slug;
                    document.getElementById('pageTitle').textContent = d.name + ' — Panel';
                    document.title = d.name + ' — SmartStay';
                }});
        }}

        // Request notification permission on load
        if ('Notification' in window && Notification.permission === 'default') {{
            setTimeout(() => {{
                Notification.requestPermission();
            }}, 2000);
        }}

        loadData();
        setInterval(loadData, 3000);

        // Load charts
        function loadCharts() {{
            fetch('/api/hotel/' + slug + '/stats')
                .then(r => r.json())
                .then(data => {{
                    const grid = document.getElementById('chartsGrid');
                    if (!data.days || data.days.length === 0) return;
                    grid.style.display = 'grid';

                    // Bar chart
                    const max = Math.max(...data.days.map(d => d.total), 1);
                    document.getElementById('chartBars').innerHTML = data.days.map(d => `
                        <div class="bar-item">
                            <div class="bar-fill" 
                                style="height:${{Math.round((d.total/max)*140)}}px; background:linear-gradient(to top, #C9A84C, #E8C96A);"
                                data-value="${{d.total}}">
                            </div>
                            <div class="bar-fill"
                                style="height:${{Math.round((d.urgent/max)*140)}}px; background:#E05555; margin-top:-${{Math.round((d.urgent/max)*140)}}px; opacity:0.7;"
                                data-value="Acil: ${{d.urgent}}">
                            </div>
                            <div class="bar-label">${{d.day.slice(5)}}</div>
                        </div>
                    `).join('');

                    // Top rooms
                    const maxCount = Math.max(...data.top_rooms.map(r => r.count), 1);
                    document.getElementById('topRooms').innerHTML = data.top_rooms.map(r => `
                        <div class="room-bar-item">
                            <div class="room-bar-name">🚪 ${{r.room}}</div>
                            <div class="room-bar-track">
                                <div class="room-bar-fill" style="width:${{Math.round((r.count/maxCount)*100)}}%"></div>
                            </div>
                            <div class="room-bar-count">${{r.count}}</div>
                        </div>
                    `).join('');
                }});
        }}

        if (slug) {{
            loadCharts();
            setInterval(loadCharts, 30000);
        }}
    </script>
</body>
</html>
"""

def get_dashboard_html(hotel_name="SmartStay"):
    return DASHBOARD_HTML.format(hotel_name=hotel_name)