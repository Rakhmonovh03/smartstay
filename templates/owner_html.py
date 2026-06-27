def get_owner_login_html() -> str:
    return """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SmartStay — Владелец</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #111; color: #eee; font-family: 'Segoe UI', sans-serif;
         display: flex; align-items: center; justify-content: center; min-height: 100vh; }
  .card { background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 14px;
          padding: 40px; width: 100%; max-width: 400px; }
  .logo { text-align: center; font-size: 28px; font-weight: 800; color: #C9A84C;
          margin-bottom: 6px; }
  .sub  { text-align: center; color: #666; font-size: 13px; margin-bottom: 30px; }
  label { display: block; font-size: 12px; color: #888; margin-bottom: 6px; }
  input { width: 100%; padding: 11px 14px; background: #111; border: 1px solid #2a2a2a;
          border-radius: 8px; color: #eee; font-size: 14px; margin-bottom: 16px; }
  input:focus { outline: none; border-color: #C9A84C; }
  .btn { width: 100%; padding: 12px; background: #C9A84C; color: #000; border: none;
         border-radius: 8px; font-weight: 700; font-size: 15px; cursor: pointer; }
  .btn:hover { background: #e0b85c; }
  .err { color: #e05555; font-size: 13px; margin-top: 10px; text-align: center; }
  .admin-link { text-align: center; margin-top: 20px; font-size: 12px; color: #555; }
  .admin-link a { color: #666; text-decoration: none; }
  .admin-link a:hover { color: #C9A84C; }
</style>
</head>
<body>
<div class="card">
  <div class="logo">🏨 SmartStay</div>
  <div class="sub">Портал владельца сети отелей</div>
  <label>Email</label>
  <input type="email" id="email" placeholder="owner@company.com" autocomplete="email">
  <label>Пароль</label>
  <input type="password" id="pass" placeholder="••••••••" autocomplete="current-password">
  <button class="btn" onclick="doLogin()">Войти →</button>
  <div class="err" id="err"></div>
  <div class="admin-link"><a href="/admin/login">← Admin panel</a></div>
</div>
<script>
async function doLogin() {
  const email = document.getElementById('email').value.trim();
  const pass  = document.getElementById('pass').value;
  if (!email || !pass) { document.getElementById('err').textContent = 'Заполните все поля'; return; }
  const r = await fetch('/api/owner/login', {
    method: 'POST', headers: {'Content-Type':'application/json'},
    body: JSON.stringify({email, password: pass})
  });
  const d = await r.json();
  if (d.ok) { window.location.href = '/owner/dashboard'; }
  else { document.getElementById('err').textContent = d.error || 'Ошибка входа'; }
}
document.addEventListener('keydown', e => { if (e.key === 'Enter') doLogin(); });
</script>
</body>
</html>"""


def get_owner_dashboard_html(owner: dict, hotels: list) -> str:
    owner_name = owner.get("name", "")
    owner_email = owner.get("email", "")

    hotel_count = len(hotels)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SmartStay — {owner_name}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #111; color: #eee; font-family: 'Segoe UI', sans-serif; min-height: 100vh; }}

  /* Header */
  .header {{ background: #1a1a1a; border-bottom: 1px solid #2a2a2a;
              padding: 0 28px; display: flex; align-items: center; justify-content: space-between;
              height: 60px; position: sticky; top: 0; z-index: 100; }}
  .logo {{ font-size: 20px; font-weight: 800; color: #C9A84C; }}
  .user-info {{ display: flex; align-items: center; gap: 16px; }}
  .user-name {{ font-size: 14px; color: #aaa; }}
  .logout-btn {{ padding: 7px 16px; background: transparent; border: 1px solid #333;
                 border-radius: 8px; color: #888; font-size: 13px; cursor: pointer;
                 text-decoration: none; }}
  .logout-btn:hover {{ border-color: #C9A84C; color: #C9A84C; }}

  /* Content */
  .content {{ max-width: 1100px; margin: 0 auto; padding: 32px 24px; }}
  .page-title {{ font-size: 22px; font-weight: 700; margin-bottom: 6px; }}
  .page-sub {{ color: #666; font-size: 14px; margin-bottom: 28px; }}

  /* Summary bar */
  .summary {{ display: flex; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }}
  .stat-card {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 12px;
                padding: 18px 24px; flex: 1; min-width: 150px; }}
  .stat-label {{ font-size: 12px; color: #666; margin-bottom: 6px; }}
  .stat-value {{ font-size: 26px; font-weight: 800; color: #C9A84C; }}

  /* Hotel grid */
  .hotel-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 18px; }}
  .hotel-card {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 14px;
                 padding: 22px; transition: border-color .2s; }}
  .hotel-card:hover {{ border-color: #C9A84C44; }}
  .hotel-name {{ font-size: 16px; font-weight: 700; margin-bottom: 4px; }}
  .hotel-slug {{ font-size: 12px; color: #555; margin-bottom: 14px; }}
  .hotel-stats {{ display: flex; gap: 12px; margin-bottom: 18px; flex-wrap: wrap; }}
  .hs {{ background: #111; border-radius: 8px; padding: 8px 12px; text-align: center; flex: 1; }}
  .hs-val {{ font-size: 18px; font-weight: 700; color: #C9A84C; }}
  .hs-lbl {{ font-size: 11px; color: #555; }}
  .plan-badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px;
                 font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 14px; }}
  .plan-trial      {{ background: #2a2010; color: #C9A84C; border: 1px solid #C9A84C44; }}
  .plan-basic      {{ background: #102030; color: #4ab0e8; border: 1px solid #4ab0e844; }}
  .plan-pro        {{ background: #102030; color: #4a8ee8; border: 1px solid #4a8ee844; }}
  .plan-enterprise {{ background: #201030; color: #a04ae8; border: 1px solid #a04ae844; }}
  .actions {{ display: flex; gap: 10px; }}
  .btn-enter {{ flex: 1; padding: 10px; background: #C9A84C; color: #000; border: none;
                border-radius: 8px; font-weight: 700; font-size: 13px; cursor: pointer;
                text-decoration: none; text-align: center; }}
  .btn-enter:hover {{ background: #e0b85c; }}
  .btn-settings {{ padding: 10px 14px; background: transparent; border: 1px solid #2a2a2a;
                   border-radius: 8px; color: #888; font-size: 13px; cursor: pointer;
                   text-decoration: none; text-align: center; }}
  .btn-settings:hover {{ border-color: #555; color: #eee; }}

  /* Empty state */
  .empty {{ text-align: center; padding: 60px 20px; color: #555; }}
  .empty-icon {{ font-size: 48px; margin-bottom: 16px; }}

  /* Loading */
  .loading {{ text-align: center; padding: 40px; color: #555; }}
</style>
</head>
<body>
<div class="header">
  <div class="logo">🏨 SmartStay</div>
  <div class="user-info">
    <span class="user-name">👤 {owner_name} · {owner_email}</span>
    <a href="/owner/logout" class="logout-btn">Выйти</a>
  </div>
</div>

<div class="content">
  <div class="page-title">Мои отели</div>
  <div class="page-sub">Управление сетью · {hotel_count} {"отель" if hotel_count == 1 else "отелей" if hotel_count in [0, 5,6,7,8,9] else "отеля"}</div>

  <div class="summary" id="summaryBar">
    <div class="stat-card">
      <div class="stat-label">Всего отелей</div>
      <div class="stat-value" id="totalHotels">{hotel_count}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Гостей сейчас</div>
      <div class="stat-value" id="totalGuests">—</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Непрочитанных</div>
      <div class="stat-value" id="totalUnread">—</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Средний рейтинг</div>
      <div class="stat-value" id="avgRating">—</div>
    </div>
  </div>

  <div id="hotelGrid" class="hotel-grid">
    <div class="loading">Загрузка...</div>
  </div>
</div>

<script>
function esc(t) {{
  const d = document.createElement('div');
  d.appendChild(document.createTextNode(String(t == null ? '' : t)));
  return d.innerHTML;
}}
const PLAN_CLASS = {{
  trial: 'plan-trial', basic: 'plan-basic', pro: 'plan-pro', enterprise: 'plan-enterprise'
}};
const PLAN_LABEL = {{
  trial: 'Trial', basic: 'Basic', pro: 'Pro', enterprise: 'Enterprise'
}};

async function loadHotels() {{
  const r = await fetch('/api/owner/hotels', {{credentials: 'include'}});
  const d = await r.json();
  if (!d.hotels) return;

  const hotels = d.hotels;
  const grid = document.getElementById('hotelGrid');

  if (hotels.length === 0) {{
    grid.innerHTML = `<div class="empty" style="grid-column:1/-1">
      <div class="empty-icon">🏨</div>
      <div>Нет отелей. Обратитесь к администратору для привязки отеля.</div>
    </div>`;
    return;
  }}

  // Summary stats
  const totalGuests  = hotels.reduce((s, h) => s + (h.active_guests || 0), 0);
  const totalUnread  = hotels.reduce((s, h) => s + (h.unread_messages || 0), 0);
  const ratings      = hotels.filter(h => h.avg_rating && h.avg_rating !== '—').map(h => parseFloat(h.avg_rating));
  const avgRating    = ratings.length ? (ratings.reduce((a, b) => a + b, 0) / ratings.length).toFixed(1) : '—';

  document.getElementById('totalGuests').textContent = totalGuests;
  document.getElementById('totalUnread').textContent = totalUnread;
  document.getElementById('avgRating').textContent = avgRating !== '—' ? '⭐ ' + avgRating : '—';

  grid.innerHTML = hotels.map(h => {{
    const planKey   = h.plan || 'trial';
    const planClass = PLAN_CLASS[planKey] || 'plan-trial';
    const planLabel = PLAN_LABEL[planKey] || planKey;
    const unreadBadge = h.unread_messages > 0
      ? `<span style="background:#e05555;color:#fff;border-radius:20px;padding:2px 8px;font-size:11px;font-weight:700;margin-left:8px">${{h.unread_messages}} new</span>`
      : '';
    return `
    <div class="hotel-card">
      <div class="hotel-name">${{esc(h.name)}}${{unreadBadge}}</div>
      <div class="hotel-slug">${{esc(h.slug)}}</div>
      <span class="plan-badge ${{planClass}}">${{planLabel}}</span>
      <div class="hotel-stats">
        <div class="hs">
          <div class="hs-val">${{h.active_guests || 0}}</div>
          <div class="hs-lbl">Гостей</div>
        </div>
        <div class="hs">
          <div class="hs-val">${{h.unread_messages || 0}}</div>
          <div class="hs-lbl">Непрочитан.</div>
        </div>
        <div class="hs">
          <div class="hs-val">${{h.avg_rating !== '—' ? '⭐ ' + h.avg_rating : '—'}}</div>
          <div class="hs-lbl">Рейтинг</div>
        </div>
      </div>
      <div class="actions">
        <a href="/owner/enter/${{h.slug}}" class="btn-enter">🚀 Открыть дашборд</a>
        <a href="/hotel/${{h.slug}}/login" class="btn-settings">⚙️</a>
      </div>
    </div>`;
  }}).join('');
}}

loadHotels();
// Auto-refresh every 60s
setInterval(loadHotels, 60000);
</script>
</body>
</html>"""
