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
        .action-links { display:flex; gap:8px; flex-wrap:wrap; }
        .action-link { color:#C9A84C; font-size:12px; text-decoration:none; padding:5px 12px; border:1px solid rgba(201,168,76,0.3); border-radius:6px; transition:all 0.2s; }
        .action-link:hover { background:rgba(201,168,76,0.1); }
        .plan-pill {
            display:inline-block; padding:3px 10px; border-radius:20px;
            font-size:11px; font-weight:700; letter-spacing:.5px; text-transform:uppercase;
        }
        .plan-trial   { background:rgba(91,141,239,.12); color:#5B8DEF; border:1px solid rgba(91,141,239,.25); }
        .plan-starter { background:rgba(201,168,76,.12); color:#C9A84C; border:1px solid rgba(201,168,76,.25); }
        .plan-pro     { background:rgba(76,175,80,.12);  color:#4CAF50; border:1px solid rgba(76,175,80,.25); }
        .plan-premium { background:rgba(155,89,182,.12); color:#9B59B6; border:1px solid rgba(155,89,182,.25); }
        .plan-select {
            background:#1a1a1a; border:1px solid #333; border-radius:6px;
            color:#C9A84C; font-size:11px; font-weight:700; padding:3px 8px;
            cursor:pointer; outline:none; text-transform:uppercase; letter-spacing:.5px;
        }
        .plan-select:focus { border-color:#C9A84C; }
        .plan-select option { background:#1a1a1a; color:white; }

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
        <a class="nav-item active" onclick="showTab('hotels')" id="tab-hotels"><span>🏨</span> Tüm Oteller</a>
        <a class="nav-item" onclick="showTab('owners')" id="tab-owners"><span>👥</span> Владельцы</a>
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

    <div id="section-hotels" class="main">
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
                <div class="stat-icon">🛎️</div>
                <div class="stat-num" id="totalGuests">—</div>
                <div class="stat-label">Toplam Misafir</div>
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
                        <th>Plan</th>
                        <th>Mesajlar</th>
                        <th>Misafirler</th>
                        <th>Puan</th>
                        <th>Telegram</th>
                        <th>Kayıt</th>
                        <th>İşlemler</th>
                    </tr>
                </thead>
                <tbody id="tbody"></tbody>
            </table>
        </div>
    </div>

    <script>
        function esc(t) {
            const d = document.createElement('div');
            d.appendChild(document.createTextNode(String(t)));
            return d.innerHTML;
        }

        fetch('/api/admin/hotels', {credentials:'include'})
            .then(r => r.json())
            .then(data => {
                const hotels = data.hotels;
                const total = hotels.length;
                const active = hotels.filter(h => h.message_count > 0).length;
                const monthly = data.monthly_revenue || 0;
                const yearly = monthly * 12;

                document.getElementById('totalHotels').textContent = total;
                document.getElementById('totalMessages').textContent = data.total_messages;
                document.getElementById('totalGuests').textContent = data.total_guests || 0;
                document.getElementById('activeHotels').textContent = active;
                document.getElementById('revenueNum').textContent = '$' + monthly.toLocaleString();
                document.getElementById('yearlyRevenue').textContent = '$' + yearly.toLocaleString();

                const PLAN_LABELS = {trial:'Trial', starter:'Starter', pro:'Pro', premium:'Premium'};

                document.getElementById('tbody').innerHTML = hotels.map((h, i) => {
                    const plan = h.plan || 'trial';
                    const stars = h.avg_rating
                        ? '★'.repeat(Math.round(h.avg_rating)) + '☆'.repeat(5-Math.round(h.avg_rating))
                        : '—';
                    const ratingColor = !h.avg_rating ? '#555'
                        : h.avg_rating >= 4 ? '#C9A84C'
                        : h.avg_rating >= 3 ? '#E8A040' : '#E05555';
                    return `<tr>
                        <td style="color:#555">${i+1}</td>
                        <td>
                            <div class="hotel-name">${esc(h.name)}</div>
                            <div class="hotel-slug">${esc(h.slug)}</div>
                        </td>
                        <td>
                        <select class="plan-select" onchange="changePlan('${esc(h.slug)}', this)">
                            ${['trial','starter','pro','premium'].map(p =>
                                `<option value="${p}" ${p===plan?'selected':''}>${PLAN_LABELS[p]||p}</option>`
                            ).join('')}
                        </select>
                    </td>
                        <td>
                            <span class="badge ${h.message_count > 0 ? 'badge-active' : 'badge-new'}">
                                ${h.message_count > 0 ? '✓' : '○'} ${h.message_count}
                            </span>
                        </td>
                        <td style="font-size:13px">
                            <span style="color:#4CAF50;font-weight:600">${h.active_guests}</span>
                            <span style="color:#555"> / ${h.total_guests}</span>
                        </td>
                        <td style="font-size:12px;color:${ratingColor};white-space:nowrap">
                            ${h.avg_rating ? h.avg_rating + ' ' + stars : '—'}
                        </td>
                        <td>
                            ${h.telegram_token
                                ? '<span class="badge badge-active">✓ Bağlı</span>'
                                : '<span style="color:#555;font-size:12px">— Yok</span>'}
                        </td>
                        <td style="color:#555;font-size:12px">${esc(h.created_at)}</td>
                        <td>
                            <div class="action-links">
                                <a href="/hotel/${h.slug}" target="_blank" class="action-link">👤</a>
                                <a href="/hotel/${h.slug}/dashboard" target="_blank" class="action-link">📊</a>
                                <a href="/hotel/${h.slug}/edit" target="_blank" class="action-link">⚙️</a>
                                <a href="/api/admin/hotel/${h.slug}/impersonate" class="action-link" style="background:rgba(74,176,232,0.1);color:#4ab0e8;border:1px solid rgba(74,176,232,0.3);" title="Войти как менеджер">🔓</a>
                                <button onclick="resetPassword('${esc(h.slug)}')" class="action-link" style="background:rgba(201,168,76,0.1);color:#C9A84C;cursor:pointer;" title="Şifre sıfırla">🔑</button>
                                <button onclick="deleteHotel('${esc(h.slug)}', '${esc(h.name)}')" class="action-link" style="background:rgba(224,85,85,0.15);color:#E05555;border:1px solid rgba(224,85,85,0.3);cursor:pointer;">🗑️</button>
                            </div>
                        </td>
                    </tr>`;
                }).join('');
            });

        async function changePlan(slug, selectEl) {
            const plan = selectEl.value;
            try {
                const res = await fetch('/api/admin/hotel/' + slug + '/plan', {
                    method: 'PATCH',
                    headers: {'Content-Type': 'application/json'},
                    credentials: 'include',
                    body: JSON.stringify({plan})
                });
                const data = await res.json();
                if (data.ok) {
                    showToast('✅ Plan güncellendi: ' + plan.toUpperCase(), 'green');
                } else {
                    showToast('❌ ' + (data.error || 'Hata'), 'red');
                }
            } catch(e) {
                showToast('❌ Bağlantı hatası', 'red');
            }
        }

        async function resetPassword(slug) {
            const pw = prompt('🔑 ' + slug + ' için yeni şifre girin (min 6 karakter):');
            if (!pw || pw.trim().length < 6) {
                if (pw !== null) alert('Şifre en az 6 karakter olmalı');
                return;
            }
            try {
                const res = await fetch('/api/admin/hotel/' + slug + '/password', {
                    method: 'PATCH',
                    headers: {'Content-Type': 'application/json'},
                    credentials: 'include',
                    body: JSON.stringify({password: pw.trim()})
                });
                const data = await res.json();
                if (data.ok) showToast('✅ Şifre güncellendi: ' + slug, 'green');
                else showToast('❌ ' + (data.error || 'Hata'), 'red');
            } catch(e) {
                showToast('❌ Bağlantı hatası', 'red');
            }
        }

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

        // ===== OWNERS TAB =====
        function showTab(tab) {
            document.getElementById('section-hotels').style.display = tab === 'hotels' ? '' : 'none';
            document.getElementById('section-owners').style.display = tab === 'owners' ? '' : 'none';
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tab).classList.add('active');
            if (tab === 'owners') loadOwners();
        }

        async function loadOwners() {
            const [ownersRes, hotelsRes] = await Promise.all([
                fetch('/api/admin/owners', {credentials:'include'}).then(r => r.json()),
                fetch('/api/admin/hotels', {credentials:'include'}).then(r => r.json())
            ]);
            const owners = ownersRes.owners || [];
            const hotels = hotelsRes.hotels || [];
            const allSlugs = hotels.map(h => h.slug);

            document.getElementById('owners-count').textContent = owners.length;

            const list = document.getElementById('owners-list');
            if (owners.length === 0) {
                list.innerHTML = '<div style="color:#555;padding:20px;text-align:center">Нет владельцев</div>';
                return;
            }
            list.innerHTML = owners.map(o => `
            <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:20px;margin-bottom:12px">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
                <div>
                  <div style="font-weight:700;font-size:15px">${esc(o.name)}</div>
                  <div style="color:#666;font-size:13px">${esc(o.email)}</div>
                </div>
                <div style="font-size:12px;color:#555">${esc(o.created_at)}</div>
              </div>
              <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
                <select id="sel-${o.id}" style="background:#111;border:1px solid #333;border-radius:6px;color:#eee;padding:6px 10px;font-size:13px">
                  <option value="">— Отель для привязки —</option>
                  ${allSlugs.map(s => `<option value="${esc(s)}">${esc(s)}</option>`).join('')}
                </select>
                <button onclick="assignHotel(${o.id})" style="padding:6px 14px;background:#C9A84C;color:#000;border:none;border-radius:6px;font-weight:700;cursor:pointer;font-size:13px">Привязать</button>
              </div>
            </div>`).join('');
        }

        async function assignHotel(ownerId) {
            const sel = document.getElementById('sel-' + ownerId);
            const slug = sel.value;
            if (!slug) { showToast('Выберите отель', 'red'); return; }
            const r = await fetch('/api/admin/owners/' + ownerId + '/hotels', {
                method: 'POST', credentials: 'include',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({hotel_slug: slug})
            });
            const d = await r.json();
            if (d.ok) { showToast('✅ Отель привязан!', 'green'); }
            else { showToast('❌ ' + (d.error || 'Ошибка'), 'red'); }
        }

        async function createOwner() {
            const name  = document.getElementById('new-owner-name').value.trim();
            const email = document.getElementById('new-owner-email').value.trim();
            const pass  = document.getElementById('new-owner-pass').value.trim();
            if (!name || !email || !pass) { showToast('Заполните все поля', 'red'); return; }
            const r = await fetch('/api/admin/owners', {
                method: 'POST', credentials: 'include',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({name, email, password: pass})
            });
            const d = await r.json();
            if (d.ok) { showToast('✅ Владелец создан!', 'green'); loadOwners(); }
            else { showToast('❌ ' + (d.error || 'Ошибка'), 'red'); }
        }

        setInterval(() => {
            if (document.getElementById('section-hotels').style.display !== 'none') location.reload();
        }, 30000);
    </script>

    <!-- OWNERS SECTION (hidden by default) -->
    <div id="section-owners" style="display:none" class="main">
        <div class="page-header">
            <div>
                <div class="page-title">👥 Владельцы сети</div>
                <div class="page-sub">Аккаунты с доступом к нескольким отелям</div>
            </div>
        </div>

        <!-- Create owner form -->
        <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:14px;padding:24px;margin-bottom:28px">
            <div style="font-weight:700;font-size:15px;margin-bottom:16px">➕ Создать нового владельца</div>
            <div style="display:flex;gap:12px;flex-wrap:wrap">
                <input id="new-owner-name" placeholder="Имя" style="flex:1;min-width:150px;background:#111;border:1px solid #2a2a2a;border-radius:8px;color:#eee;padding:10px 14px;font-size:14px">
                <input id="new-owner-email" placeholder="Email" type="email" style="flex:2;min-width:200px;background:#111;border:1px solid #2a2a2a;border-radius:8px;color:#eee;padding:10px 14px;font-size:14px">
                <input id="new-owner-pass" placeholder="Пароль" type="password" style="flex:1;min-width:150px;background:#111;border:1px solid #2a2a2a;border-radius:8px;color:#eee;padding:10px 14px;font-size:14px">
                <button onclick="createOwner()" style="padding:10px 20px;background:#C9A84C;color:#000;border:none;border-radius:8px;font-weight:700;cursor:pointer;font-size:14px">Создать</button>
            </div>
        </div>

        <div style="font-size:13px;color:#666;margin-bottom:16px">Всего владельцев: <b id="owners-count">—</b></div>
        <div id="owners-list"></div>

        <div style="margin-top:20px;padding:16px;background:#111;border-radius:10px;font-size:13px;color:#555">
            💡 Владелец заходит на <b style="color:#C9A84C">/owner/login</b> и видит только свои отели.
            Кнопка 🔓 в таблице отелей входит в дашборд без пароля (для вас как Super Admin).
        </div>
    </div>
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