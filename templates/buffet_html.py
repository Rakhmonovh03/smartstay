"""
Buffet page template — страница анализа шведского стола.
Доступна только авторизованному персоналу: /hotel/{slug}/buffet
"""


def get_buffet_html(hotel_name: str, slug: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🍽️ Smart Buffet — {hotel_name}</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --bg:     #141414;
    --bg2:    #1c1c1c;
    --bg3:    #252525;
    --border: #2e2e2e;
    --text:   #f0f0f0;
    --text2:  #888;
    --gold:   #C9A84C;
    --gold2:  #d4b85a;
  }}

  body {{
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    min-height: 100vh;
    padding: 24px 16px 60px;
  }}

  .topbar {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 28px;
  }}
  .back-btn {{
    background: var(--bg2);
    border: 1px solid var(--border);
    color: var(--text2);
    padding: 8px 14px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 13px;
    text-decoration: none;
  }}
  .back-btn:hover {{ color: var(--text); }}
  .page-title {{
    font-size: 20px;
    font-weight: 700;
    color: var(--gold);
  }}
  .page-sub {{
    font-size: 13px;
    color: var(--text2);
    margin-top: 2px;
  }}

  /* Upload card */
  .card {{
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
  }}
  .card-title {{
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 16px;
    color: var(--text);
  }}

  .upload-zone {{
    border: 2px dashed var(--border);
    border-radius: 12px;
    padding: 32px 20px;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s;
    position: relative;
  }}
  .upload-zone:hover {{ border-color: var(--gold); }}
  .upload-zone.has-image {{ border-style: solid; border-color: var(--gold); padding: 0; }}

  #previewImg {{
    width: 100%;
    max-height: 320px;
    object-fit: cover;
    border-radius: 10px;
    display: none;
  }}
  .upload-hint {{ font-size: 14px; color: var(--text2); margin-top: 8px; }}
  .upload-icon {{ font-size: 40px; }}

  #fileInput {{ display: none; }}

  .btn-gold {{
    background: var(--gold);
    color: #000;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    width: 100%;
    margin-top: 16px;
    transition: background 0.2s;
  }}
  .btn-gold:hover {{ background: var(--gold2); }}
  .btn-gold:disabled {{
    background: var(--bg3);
    color: var(--text2);
    cursor: not-allowed;
  }}

  /* Spinner */
  .spinner {{
    display: none;
    text-align: center;
    padding: 24px;
    color: var(--text2);
    font-size: 14px;
  }}
  .spinner.active {{ display: block; }}

  /* Results */
  #resultsCard {{ display: none; }}

  .summary-box {{
    background: var(--bg3);
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 13px;
    color: var(--text2);
    margin-bottom: 20px;
    line-height: 1.5;
  }}

  .dish-row {{
    margin-bottom: 14px;
  }}
  .dish-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
  }}
  .dish-name {{
    font-size: 13px;
    font-weight: 600;
  }}
  .dish-pct {{
    font-size: 12px;
    font-weight: 700;
  }}
  .dish-pct.empty  {{ color: #e05555; }}
  .dish-pct.low    {{ color: #E8A040; }}
  .dish-pct.good   {{ color: var(--gold); }}
  .dish-pct.full   {{ color: #4CAF50; }}

  .bar-bg {{
    background: var(--bg3);
    border-radius: 4px;
    height: 8px;
    overflow: hidden;
  }}
  .bar-fill {{
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s ease;
  }}
  .bar-fill.empty  {{ background: #e05555; }}
  .bar-fill.low    {{ background: #E8A040; }}
  .bar-fill.good   {{ background: var(--gold); }}
  .bar-fill.full   {{ background: #4CAF50; }}

  /* Status badges */
  .badge {{
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .badge.empty  {{ background: rgba(224,85,85,0.15);  color: #e05555; }}
  .badge.low    {{ background: rgba(232,160,64,0.15); color: #E8A040; }}
  .badge.good   {{ background: rgba(201,168,76,0.15); color: var(--gold); }}
  .badge.full   {{ background: rgba(76,175,80,0.15);  color: #4CAF50; }}

  /* Alert: dishes needing refill */
  .alert-box {{
    border: 1px solid rgba(224,85,85,0.3);
    background: rgba(224,85,85,0.08);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 20px;
    font-size: 13px;
  }}
  .alert-title {{
    font-weight: 700;
    color: #e05555;
    margin-bottom: 6px;
  }}
  .alert-item {{
    color: var(--text2);
    padding: 2px 0;
  }}

  /* History */
  .history-item {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
    cursor: pointer;
  }}
  .history-item:last-child {{ border-bottom: none; }}
  .history-item:hover .history-time {{ color: var(--gold); }}
  .history-time {{ color: var(--text2); }}
  .history-issues {{
    font-size: 11px;
    color: #e05555;
    font-weight: 700;
  }}
  .history-ok {{
    font-size: 11px;
    color: #4CAF50;
    font-weight: 700;
  }}

  .empty-state {{
    text-align: center;
    padding: 28px;
    color: var(--text2);
    font-size: 14px;
  }}
</style>
</head>
<body>

<div class="topbar">
  <a href="/hotel/{slug}/dashboard" class="back-btn">← Dashboard</a>
  <div>
    <div class="page-title">🍽️ Smart Buffet</div>
    <div class="page-sub" id="pageSub">{hotel_name} — AI анализ шведского стола</div>
  </div>
</div>

<!-- Upload card -->
<div class="card">
  <div class="card-title" id="lblUpload">📷 Загрузить фото буфета</div>
  <div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()">
    <div class="upload-icon">📸</div>
    <div class="upload-hint" id="uploadHint">Нажмите чтобы выбрать фото<br><small>JPG / PNG / WEBP — до 20 МБ</small></div>
    <img id="previewImg" alt="preview">
  </div>
  <input type="file" id="fileInput" accept="image/*" onchange="onFileSelect(this)">
  <button class="btn-gold" id="analyzeBtn" disabled onclick="analyzePhoto()">
    🤖 <span id="lblAnalyze">Анализировать с AI</span>
  </button>
</div>

<!-- Spinner -->
<div class="spinner" id="spinner"><span id="lblSpinner">⏳ AI анализирует фото буфета...</span></div>

<!-- Results -->
<div class="card" id="resultsCard">
  <div class="card-title" id="lblResults">📊 Результат анализа</div>

  <!-- Alert: dishes needing refill -->
  <div class="alert-box" id="alertBox" style="display:none">
    <div class="alert-title" id="lblAlertTitle">⚠️ Требует пополнения</div>
    <div id="alertList"></div>
  </div>

  <div class="summary-box" id="summaryBox"></div>

  <div id="dishesList"></div>
</div>

<!-- History -->
<div class="card" id="historyCard">
  <div class="card-title" id="lblHistory">🕐 История сканов</div>
  <div id="historyList"><div class="empty-state" id="historyLoading">Загрузка...</div></div>
</div>

<script>
  const slug = '{slug}';
  let _selectedFile = null;

  // -------- i18n --------
  const BUFFET_I18N = {{
    en: {{
      pageSub: '{hotel_name} — AI buffet analysis',
      lblUpload: '📷 Upload buffet photo',
      uploadHint: 'Click to select a photo<br><small>JPG / PNG / WEBP — up to 20 MB</small>',
      lblAnalyze: 'Analyze with AI',
      lblSpinner: '⏳ AI is analyzing the buffet photo...',
      lblResults: '📊 Analysis results',
      lblAlertTitle: '⚠️ Needs refill',
      lblHistory: '🕐 Scan history',
      historyLoading: 'Loading...',
      historyEmpty: 'No scans yet',
      historyError: 'Failed to load history',
      urgentBadge: '⚠️ Urgent',
      statusEmpty: 'Empty', statusLow: 'Low', statusGood: 'Good', statusFull: 'Full',
    }},
    ru: {{
      pageSub: '{hotel_name} — AI анализ шведского стола',
      lblUpload: '📷 Загрузить фото буфета',
      uploadHint: 'Нажмите чтобы выбрать фото<br><small>JPG / PNG / WEBP — до 20 МБ</small>',
      lblAnalyze: 'Анализировать с AI',
      lblSpinner: '⏳ AI анализирует фото буфета...',
      lblResults: '📊 Результат анализа',
      lblAlertTitle: '⚠️ Требует пополнения',
      lblHistory: '🕐 История сканов',
      historyLoading: 'Загрузка...',
      historyEmpty: 'Сканов пока нет',
      historyError: 'Ошибка загрузки истории',
      urgentBadge: '⚠️ Срочно',
      statusEmpty: 'Пусто', statusLow: 'Мало', statusGood: 'Норма', statusFull: 'Полно',
    }},
    tr: {{
      pageSub: '{hotel_name} — AI büfe analizi',
      lblUpload: '📷 Büfe fotoğrafı yükle',
      uploadHint: "Fotoğraf seçmek için tıklayın<br><small>JPG / PNG / WEBP — 20 MB'a kadar</small>",
      lblAnalyze: 'AI ile analiz et',
      lblSpinner: '⏳ AI büfe fotoğrafını analiz ediyor...',
      lblResults: '📊 Analiz sonuçları',
      lblAlertTitle: '⚠️ Doldurulması gerekiyor',
      lblHistory: '🕐 Tarama geçmişi',
      historyLoading: 'Yükleniyor...',
      historyEmpty: 'Henüz tarama yok',
      historyError: 'Geçmiş yüklenemedi',
      urgentBadge: '⚠️ Acil',
      statusEmpty: 'Boş', statusLow: 'Az', statusGood: 'İyi', statusFull: 'Dolu',
    }},
    uz: {{
      pageSub: '{hotel_name} — AI bufet tahlili',
      lblUpload: '📷 Bufet rasmini yuklash',
      uploadHint: 'Rasm tanlash uchun bosing<br><small>JPG / PNG / WEBP — 20 MB gacha</small>',
      lblAnalyze: 'AI bilan tahlil qilish',
      lblSpinner: '⏳ AI bufet rasmini tahlil qilmoqda...',
      lblResults: '📊 Tahlil natijalari',
      lblAlertTitle: "⚠️ To'ldirish kerak",
      lblHistory: '🕐 Skanlar tarixi',
      historyLoading: 'Yuklanmoqda...',
      historyEmpty: "Hali skan yo'q",
      historyError: 'Tarixni yuklashda xato',
      urgentBadge: '⚠️ Shoshilinch',
      statusEmpty: "Bo'sh", statusLow: 'Kam', statusGood: 'Normal', statusFull: "To'liq",
    }},
  }};

  function _L() {{
    const lang = localStorage.getItem('ss_lang') || 'en';
    return BUFFET_I18N[lang] || BUFFET_I18N.en;
  }}

  function applyBuffetLang() {{
    const L = _L();
    ['pageSub','lblUpload','lblAnalyze','lblSpinner','lblResults','lblAlertTitle','lblHistory','historyLoading'].forEach(id => {{
      const el = document.getElementById(id);
      if (el) el.innerHTML = L[id] || el.innerHTML;
    }});
    document.getElementById('uploadHint').innerHTML = L.uploadHint;
  }}

  // -------- Upload / Preview --------

  function onFileSelect(input) {{
    const file = input.files[0];
    if (!file) return;
    _selectedFile = file;

    const reader = new FileReader();
    reader.onload = e => {{
      const img = document.getElementById('previewImg');
      img.src = e.target.result;
      img.style.display = 'block';
      const zone = document.getElementById('uploadZone');
      zone.classList.add('has-image');
      zone.querySelector('.upload-icon').style.display = 'none';
      zone.querySelector('.upload-hint').style.display = 'none';
    }};
    reader.readAsDataURL(file);
    document.getElementById('analyzeBtn').disabled = false;
  }}

  // Drag & drop support
  const zone = document.getElementById('uploadZone');
  zone.addEventListener('dragover', e => {{ e.preventDefault(); zone.style.borderColor = 'var(--gold)'; }});
  zone.addEventListener('dragleave', () => {{ zone.style.borderColor = ''; }});
  zone.addEventListener('drop', e => {{
    e.preventDefault();
    zone.style.borderColor = '';
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {{
      // Simulate file input selection
      const dt = new DataTransfer();
      dt.items.add(file);
      const fi = document.getElementById('fileInput');
      fi.files = dt.files;
      onFileSelect(fi);
    }}
  }});

  // -------- Analyze --------

  async function analyzePhoto() {{
    if (!_selectedFile) return;
    document.getElementById('analyzeBtn').disabled = true;
    document.getElementById('spinner').classList.add('active');
    document.getElementById('resultsCard').style.display = 'none';

    const formData = new FormData();
    formData.append('photo', _selectedFile);

    try {{
      const res = await fetch('/hotel/' + slug + '/buffet/analyze', {{
        method: 'POST',
        credentials: 'include',
        body: formData
      }});
      const data = await res.json();
      if (!res.ok || data.error) {{
        alert('Ошибка: ' + (data.error || res.status));
        return;
      }}
      showResults(data.result);
      loadHistory();
    }} catch (e) {{
      alert('Ошибка сети: ' + e.message);
    }} finally {{
      document.getElementById('spinner').classList.remove('active');
      document.getElementById('analyzeBtn').disabled = false;
    }}
  }}

  // -------- Render results --------

  function showResults(result) {{
    const dishes = result.dishes || [];
    const summary = result.summary || '';

    document.getElementById('summaryBox').textContent = '💬 ' + summary;

    // Alert: dishes with fill_percent < 30% need urgent refill
    const needRefill = dishes.filter(d => d.fill_percent < 30);
    const alertBox = document.getElementById('alertBox');
    if (needRefill.length > 0) {{
      alertBox.style.display = 'block';
      document.getElementById('alertList').innerHTML =
        needRefill.map(d =>
          `<div class="alert-item">• ${{d.name}} — <b style="color:#e05555">${{d.fill_percent}}%</b></div>`
        ).join('');
    }} else {{
      alertBox.style.display = 'none';
    }}

    // Dish bars — override color class to red if fill_percent < 30
    document.getElementById('dishesList').innerHTML = dishes.map(d => {{
      const colorClass = d.fill_percent < 30 ? 'empty' : d.status;
      return `
      <div class="dish-row">
        <div class="dish-header">
          <span class="dish-name" style="color:${{d.fill_percent < 30 ? '#e05555' : 'var(--text)'}}">${{d.name}}</span>
          <span style="display:flex;align-items:center;gap:8px">
            <span class="badge ${{colorClass}}">${{d.fill_percent < 30 ? _L().urgentBadge : statusLabel(d.status)}}</span>
            <span class="dish-pct ${{colorClass}}">${{d.fill_percent}}%</span>
          </span>
        </div>
        <div class="bar-bg">
          <div class="bar-fill ${{colorClass}}" style="width:${{d.fill_percent}}%"></div>
        </div>
      </div>`;
    }}).join('');

    document.getElementById('resultsCard').style.display = 'block';
  }}

  function statusLabel(s) {{
    const L = _L();
    return {{empty:L.statusEmpty, low:L.statusLow, good:L.statusGood, full:L.statusFull}}[s] || s;
  }}

  // -------- History --------

  async function loadHistory() {{
    try {{
      const res = await fetch('/api/hotel/' + slug + '/buffet/history?days=7', {{
        credentials: 'include'
      }});
      const data = await res.json();
      renderHistory(data.scans || []);
    }} catch (e) {{
      document.getElementById('historyList').innerHTML =
        `<div class="empty-state">${{_L().historyError}}</div>`;
    }}
  }}

  function renderHistory(scans) {{
    const el = document.getElementById('historyList');
    if (!scans.length) {{
      el.innerHTML = `<div class="empty-state">${{_L().historyEmpty}}</div>`;
      return;
    }}
    el.innerHTML = scans.map(s => {{
      const dishes = s.dishes_data?.dishes || [];
      const issues = dishes.filter(d => d.status === 'empty' || d.status === 'low').length;
      const lang = localStorage.getItem('ss_lang') || 'en';
      const locale = lang === 'ru' ? 'ru-RU' : lang === 'tr' ? 'tr-TR' : lang === 'uz' ? 'uz-UZ' : 'en-US';
      const time = new Date(s.scan_time).toLocaleString(locale, {{
        day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit'
      }});
      const issueHtml = issues > 0
        ? `<span class="history-issues">⚠️ ${{issues}}</span>`
        : `<span class="history-ok">✅ ok</span>`;
      return `
        <div class="history-item" onclick="showResults(${{JSON.stringify(s.dishes_data).replace(/'/g,"\\'")}})">
          <span class="history-time">${{time}}</span>
          <span>${{dishes.length}} 🍽️ &nbsp; ${{issueHtml}}</span>
        </div>`;
    }}).join('');
  }}

  // -------- Init --------
  applyBuffetLang();
  loadHistory();
</script>
</body>
</html>"""
