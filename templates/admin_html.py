ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartStay — Super Admin</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:sans-serif; background:#0a0a0a; color:white; }

        .sidebar {
            position:fixed; left:0; top:0; bottom:0; width:240px;
            background:#111; border-right:1px solid rgba(201,168,76,0.15);
            padding:24px 0;
        }
        .sidebar-logo { padding:0 24px 24px; border-bottom:1px solid rgba(255,255,255,0.06); margin-bottom:24px; }
        .sidebar-logo h2 { font-size:16px; font-weight:700; color:#C9A84C; }
        .sidebar-logo p { font-size:12px; color:#555; margin-top:2px; }
        .nav-item {
            display:flex; align-items:center; gap:12px;
            padding:12px 24px; font-size:14px; color:#888;
            cursor:pointer; transition:all 0.2s; text-decoration:none;
        }
        .nav-item:hover { background:rgba(255,255,255,0.04); color:#fff; }
        .nav-item.active { background:rgba(201,168,76,0.1); color:#C9A84C; border-right:2px solid #C9A84C; }

        .main { margin-left:240px; padding:32px; }
        .page-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:32px; }
        .page-title { font-size:22px; font-weight:700; color:#C9A84C; }
        .page-sub { font-size:13px; color:#555; margin-top:4px; }

        .btn { padding:10px 20px; border-radius:8px; font-size:13px; font-weight:500; cursor:pointer; border:none; transition:all 0.2s; }
        .btn-gold { background:#C9A84C; color:#000; }
        .btn-gold:hover { background:#E8C96A; }
        .btn-dark { background:#1a1a1a; color:#fff; border:1px solid #333; }

        .stats { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:32px; }
        .stat {
            background:#111; border-radius:12px; padding:24px;
            border:1px solid rgba(255,255,255,0.05);
            position:relative; overflow:hidden;
        }
        .stat::before { content:''; position:absolute; bottom:0; left:0; right:0; height:3px; background:var(--accent, #C9A84C); }
        .stat.green { --accent:#4CAF50; }
        .stat.blue { --accent:#5B8DEF; }
        .stat.purple { --accent:#9B59B6; }
        .stat-icon { font-size:24px; margin-bottom:12px; }
        .stat-num { font-size:36px; font-weight:900; color:#C9A84C; line-height:1; }
        .stat.green .stat-num { color:#4CAF50; }
        .stat.blue .stat-num { color:#5B8DEF; }
        .stat.purple .stat-num { color:#9B59B6; }
        .stat-label { font-size:12px; color:#555; margin-top:8px; }

        .table-wrap { background:#111; border-radius:12px; border:1px solid rgba(255,255,255,0.05); overflow:hidden; }
        table { width:100%; border-collapse:collapse; }
        th {
            background:rgba(201,168,76,0.1); color:#C9A84C;
            padding:14px 16px; text-align:left; font-size:12px;
            letter-spacing:1px; text-transform:uppercase;
            border-bottom:1px solid rgba(201,168,76,0.15);
        }
        td { padding:16px; border-bottom:1px solid rgba(255,255,255,0.04); font-size:14px; }
        tr:last-child td { border-bottom:none; }
        tr:hover td { background:rgba(255,255,255,0.02); }

        .badge { display:inline-flex; align-items:center; gap:6px; padding:5px 12px; border-radius:20px; font-size:12px; font-weight:500; }
        .badge-active { background:rgba(76,175,80,0.15); color:#4CAF50; border:1px solid rgba(76,175,80,0.3); }
        .badge-new { background:rgba(201,168,76,0.15); color:#C9A84C; border:1px solid rgba(201,168,76,0.3); }
        .hotel-name { font-weight:600; font-size:15px; }
        .hotel-slug { font-size:12px; color:#555; margin-top:2px; }
        .action-links { display:flex; gap:12px; }
        .action-link { color:#C9A84C; font-size:13px; text-decoration:none; padding:6px 14px; border:1px solid rgba(201,168,76,0.3); border-radius:6px; transition:all 0.2s; }
        .action-link:hover { background:rgba(201,168,76,0.1); }

        .revenue-card {
            background:linear-gradient(135deg, rgba(201,168,76,0.1), rgba(201,168,76,0.03));
            border:1px solid rgba(201,168,76,0.2);
            border-radius:12px; padding:24px; margin-bottom:32px;
            display:flex; justify-content:space-between; align-items:center;
        }
        .revenue-card h3 { font-size:14px; color:#888; margin-bottom:8px; }
        .revenue-num { font-size:40px; font-weight:900; color:#C9A84C; }
        .revenue-sub { font-size:12px; color:#555; margin-top:4px; }

        .live-dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:#4CAF50; margin-right:6px; animation:pulse 2s infinite; }
        @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.4; } }

        /* MODAL */
        .modal-overlay {
            position:fixed; inset:0; background:rgba(0,0,0,0.8);
            display:flex; align-items:center; justify-content:center;
            z-index:1000; opacity:0; pointer-events:none; transition:opacity 0.3s;
        }
        .modal-overlay.active { opacity:1; pointer-events:all; }
        .modal {
            background:#111; border-radius:16px; padding:40px;
            width:420px; border:1px solid rgba(201,168,76,0.2);
            transform:scale(0.9); transition:transform 0.3s;
        }
        .modal-overlay.active .modal { transform:scale(1); }
        .modal-icon { font-size:48px; text-align:center; margin-bottom:16px; }
        .modal h3 { font-size:20px; font-weight:700; margin-bottom:8px; text-align:center; }
        .modal p { font-size:14px; color:#666; text-align:center; margin-bottom:32px; line-height:1.6; }
        .modal-btns { display:flex; gap:12px; }
        .modal-btn { flex:1; padding:14px; border:none; border-radius:8px; font-size:14px; font-weight:600; cursor:pointer; transition:all 0.2s; }
        .modal-btn-cancel { background:#1a1a1a; color:#fff; border:1px solid #333; }
        .modal-btn-cancel:hover { background:#222; }
        .modal-btn-delete { background:#E05555; color:#fff; }
        .modal-btn-delete:hover { background:#f06666; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-logo">
            <h2>🔐 Super Admin</h2>
            <p>SmartStay AI — 2026</p>
        </div>
        <a class="nav-item active"><span>🏨</span> Tüm Oteller</a>
        <a class="nav-item" href="/register"><span>➕</span> Yeni Otel Ekle</a>
        <div style="position:absolute; bottom:24px; left:0; right:0; padding:0 16px;">
            <a class="nav-item" href="/admin/logout" style="border-radius:8px; color:#E05555;">
                <span>🚪</span> Çıkış
            </a>
        </div>
    </div>

    <!-- DELETE MODAL -->
    <div class="modal-overlay" id="deleteModal">
        <div class="modal">
            <div class="modal-icon">🗑️</div>
            <h3>Oteli Sil</h3>
            <p id="modalText">Bu oteli silmek istediğinizden emin misiniz?<br>Tüm mesajlar da silinecek!</p>
            <div class="modal-btns">
                <button class="modal-btn modal-btn-cancel" onclick="closeModal()">İptal</button>
                <button class="modal-btn modal-btn-delete" id="confirmDelete">Evet, Sil</button>
            </div>
        </div>
    </div>

    <div class="main">
        <div class="page-header">
            <div>
                <div class="page-title">Tüm Oteller</div>
                <div class="page-sub"><span class="live-dot"></span>Canlı — Her 30 saniyede güncellenir</div>
            </div>
            <div style="display:flex; gap:10px;">
                <button class="btn btn-dark" onclick="location.reload()">🔄 Yenile</button>
                <button class="btn btn-gold" onclick="window.location.href='/register'">➕ Yeni Otel</button>
            </div>
        </div>

        <div class="revenue-card">
            <div>
                <h3>💰 Aylık Tahmini Gelir</h3>
                <div class="revenue-num" id="revenueNum">$0</div>
                <div class="revenue-sub">Aktif oteller × $800/ay</div>
            </div>
            <div style="text-align:right">
                <h3>📈 Yıllık Projeksiyon</h3>
                <div class="revenue-num" id="yearlyRevenue" style="color:#4CAF50">$0</div>
                <div class="revenue-sub">Mevcut büyüme ile</div>
            </div>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-icon">🏨</div>
                <div class="stat-num" id="totalHotels">—</div>
                <div class="stat-label">Toplam Otel</div>
            </div>
            <div class="stat green">
                <div class="stat-icon">💬</div>
                <div class="stat-num" id="totalMessages">—</div>
                <div class="stat-label">Toplam Mesaj</div>
            </div>
            <div class="stat blue">
                <div class="stat-icon">📊</div>
                <div class="stat-num" id="avgMessages">—</div>
                <div class="stat-label">Ortalama Mesaj/Otel</div>
            </div>
            <div class="stat purple">
                <div class="stat-icon">🚀</div>
                <div class="stat-num" id="activeHotels">—</div>
                <div class="stat-label">Aktif Otel</div>
            </div>
        </div>

        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Otel</th>
                        <th>Mesajlar</th>
                        <th>Telegram</th>
                        <th>Kayıt Tarihi</th>
                        <th>İşlemler</th>
                    </tr>
                </thead>
                <tbody id="tbody"></tbody>
            </table>
        </div>
    </div>

    <script>
        fetch('/api/admin/hotels')
            .then(r => r.json())
            .then(data => {
                const hotels = data.hotels;
                const total = hotels.length;
                const totalMsg = data.total_messages;
                const active = hotels.filter(h => h.message_count > 0).length;
                const monthly = total * 800;
                const yearly = monthly * 12;

                document.getElementById('totalHotels').textContent = total;
                document.getElementById('totalMessages').textContent = totalMsg;
                document.getElementById('avgMessages').textContent = total ? Math.round(totalMsg/total) : 0;
                document.getElementById('activeHotels').textContent = active;
                document.getElementById('revenueNum').textContent = '$' + monthly.toLocaleString();
                document.getElementById('yearlyRevenue').textContent = '$' + yearly.toLocaleString();

                document.getElementById('tbody').innerHTML = hotels.map((h, i) => `
                    <tr>
                        <td style="color:#555">${i+1}</td>
                        <td>
                            <div class="hotel-name">${h.name}</div>
                            <div class="hotel-slug">${h.slug}</div>
                        </td>
                        <td>
                            <span class="badge ${h.message_count > 0 ? 'badge-active' : 'badge-new'}">
                                ${h.message_count > 0 ? '✓' : '○'} ${h.message_count} mesaj
                            </span>
                        </td>
                        <td>
                            ${h.telegram_token
                                ? '<span class="badge badge-active">✓ Bağlı</span>'
                                : '<span style="color:#555; font-size:12px">— Yok</span>'}
                        </td>
                        <td style="color:#555; font-size:12px">${h.created_at}</td>
                        <td>
                            <div class="action-links">
                                <a href="/hotel/${h.slug}" target="_blank" class="action-link">👤 Chat</a>
                                <a href="/hotel/${h.slug}/dashboard" target="_blank" class="action-link">📊 Panel</a>
                                <a href="/hotel/${h.slug}/edit" target="_blank" class="action-link">⚙️ Düzenle</a>
                                <button onclick="deleteHotel('${h.slug}', '${h.name}')" class="action-link" style="background:rgba(224,85,85,0.15);color:#E05555;border:1px solid rgba(224,85,85,0.3);cursor:pointer;">🗑️ Sil</button>
                            </div>
                        </td>
                    </tr>
                `).join('');
            });

        let pendingDeleteSlug = null;

        function deleteHotel(slug, name) {
            pendingDeleteSlug = slug;
            document.getElementById('modalText').innerHTML = 
                `<b style="color:white">${name}</b> otelini silmek istediğinizden emin misiniz?<br><br>
                <span style="color:#E05555">⚠️ Tüm mesajlar da silinecek!</span>`;
            document.getElementById('deleteModal').classList.add('active');
        }

        function closeModal() {
            document.getElementById('deleteModal').classList.remove('active');
            pendingDeleteSlug = null;
        }

        document.getElementById('confirmDelete').onclick = async function() {
            if (!pendingDeleteSlug) return;
            const res = await fetch('/api/admin/hotel/' + pendingDeleteSlug, {
                method: 'DELETE',
                credentials: 'include'
            });
            const data = await res.json();
            closeModal();
            if (data.ok) {
                showToast('✅ Otel silindi!', 'green');
                setTimeout(() => location.reload(), 1000);
            } else {
                showToast('❌ Hata: ' + (data.error || 'Bilinmeyen hata'), 'red');
            }
        };

        document.getElementById('deleteModal').onclick = function(e) {
            if (e.target === this) closeModal();
        };

        function showToast(message, color) {
            const toast = document.createElement('div');
            toast.style.cssText = `
                position:fixed; bottom:24px; right:24px; z-index:9999;
                background:${color === 'green' ? '#4CAF50' : '#E05555'};
                color:white; padding:16px 24px; border-radius:10px;
                font-size:14px; font-weight:500;
                box-shadow:0 8px 24px rgba(0,0,0,0.3);
                animation:slideIn 0.3s ease;
            `;
            toast.textContent = message;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 3000);
        }

        setInterval(() => location.reload(), 30000);
    </script>
</body>
</html>
"""

ADMIN_LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartStay — Admin Giriş</title>
    <meta charset="utf-8">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:sans-serif; background:#0a0a0a; color:white; height:100vh; display:flex; align-items:center; justify-content:center; }
        .box { background:#111; border-radius:16px; padding:48px; width:360px; text-align:center; border:1px solid rgba(201,168,76,0.15); }
        .logo { color:#C9A84C; font-size:28px; font-weight:900; margin-bottom:8px; }
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
        <div class="logo">🔐 Admin</div>
        <div class="sub">SmartStay Super Admin — 2026</div>
        <input type="password" id="pwd" placeholder="Admin şifresi" onkeypress="if(event.key==='Enter') login()">
        <button onclick="login()">Giriş Yap</button>
        <div class="error" id="err">❌ Yanlış şifre</div>
    </div>
    <script>
        function login() {
            fetch('/api/admin/login', {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify({password: document.getElementById('pwd').value})
            })
            .then(r => r.json())
            .then(data => {
                if (data.ok) window.location.href = '/admin';
                else document.getElementById('err').style.display = 'block';
            });
        }
    </script>
</body>
</html>
"""

def get_admin_html():
    return ADMIN_HTML

def get_admin_login_html():
    return ADMIN_LOGIN_HTML