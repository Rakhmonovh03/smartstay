DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{hotel_name} — Панель</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        :root {{
            --bg: #0a0a0a; --bg2: #111; --bg3: #1a1a1a;
            --border: rgba(255,255,255,0.06); --border2: rgba(201,168,76,0.15);
            --text: #fff; --text2: #888; --text3: #555;
            --gold: #C9A84C; --gold2: #E8C96A;
        }}
        body.light {{
            --bg: #f4f4f4; --bg2: #fff; --bg3: #f0f0f0;
            --border: rgba(0,0,0,0.08); --border2: rgba(201,168,76,0.25);
            --text: #111; --text2: #555; --text3: #999;
        }}
        body {{ font-family:'Inter',sans-serif; background:var(--bg); color:var(--text); transition:background 0.2s,color 0.2s; }}

        /* SIDEBAR */
        .sidebar {{
            position:fixed; left:0; top:0; bottom:0; width:240px;
            background:var(--bg2); border-right:1px solid var(--border2);
            padding:24px 0; z-index:100; display:flex; flex-direction:column;
        }}
        .sidebar-logo {{ padding:0 24px 24px; border-bottom:1px solid var(--border); margin-bottom:16px; }}
        .sidebar-logo h2 {{ font-size:16px; font-weight:700; color:var(--gold); }}
        .sidebar-logo p {{ font-size:12px; color:var(--text3); margin-top:2px; }}
        .nav-item {{
            display:flex; align-items:center; gap:12px;
            padding:11px 24px; font-size:14px; color:var(--text2);
            cursor:pointer; transition:all 0.2s; text-decoration:none;
            background:none; border:none; width:100%; text-align:left;
        }}
        .nav-item:hover {{ background:rgba(201,168,76,0.05); color:var(--text); }}
        .nav-item.active {{ background:rgba(201,168,76,0.1); color:var(--gold); border-right:2px solid var(--gold); }}
        .nav-icon {{ font-size:16px; width:20px; text-align:center; }}
        .sidebar-nav {{ flex:1; overflow-y:auto; overflow-x:hidden; }}
        .sidebar-bottom {{ padding:0 16px 16px; border-top:1px solid var(--border); padding-top:12px; }}
        .lang-btn-dash {{ flex:1; padding:4px 0; border-radius:6px; border:1px solid var(--border); background:transparent; color:var(--text3); font-size:11px; font-weight:700; cursor:pointer; font-family:inherit; transition:.15s; min-width:28px; }}
        .lang-btn-dash:hover, .lang-btn-dash.active {{ border-color:var(--gold); color:var(--gold); background:rgba(201,168,76,.08); }}

        /* MAIN */
        .main {{ margin-left:240px; padding:28px 32px; }}
        .page-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:28px; }}
        .page-title {{ font-size:22px; font-weight:700; color:var(--gold); }}
        .page-sub {{ font-size:13px; color:var(--text3); margin-top:4px; }}
        .header-btns {{ display:flex; gap:10px; align-items:center; }}
        .btn {{ padding:9px 18px; border-radius:8px; font-size:13px; font-weight:500; cursor:pointer; border:none; transition:all 0.2s; font-family:inherit; }}
        .btn-gold {{ background:var(--gold); color:#000; }}
        .btn-gold:hover {{ background:var(--gold2); }}
        .btn-dark {{ background:var(--bg3); color:var(--text); border:1px solid var(--border); }}
        .btn-dark:hover {{ opacity:0.8; }}
        .btn-sm {{ padding:6px 14px; font-size:12px; }}

        /* STATS */
        .stats {{ display:grid; grid-template-columns:repeat(5,1fr); gap:14px; margin-bottom:28px; }}
        .stat {{
            background:var(--bg2); border-radius:12px; padding:20px;
            border:1px solid var(--border); position:relative; overflow:hidden;
        }}
        .stat::before {{ content:''; position:absolute; bottom:0; left:0; right:0; height:3px; background:var(--accent,var(--gold)); }}
        .stat.red {{ --accent:#E05555; }}
        .stat.green {{ --accent:#4CAF50; }}
        .stat.blue {{ --accent:#5B8DEF; }}
        .stat.purple {{ --accent:#a78bfa; }}
        .stat-icon {{ font-size:22px; margin-bottom:10px; }}
        .stat-num {{ font-size:32px; font-weight:900; color:var(--gold); line-height:1; }}
        .stat.red .stat-num {{ color:#E05555; }}
        .stat.green .stat-num {{ color:#4CAF50; }}
        .stat.blue .stat-num {{ color:#5B8DEF; }}
        .stat.purple .stat-num {{ color:#a78bfa; }}
        .stat-label {{ font-size:12px; color:var(--text3); margin-top:6px; }}

        /* GUESTS */
        .guest-card {{
            background:var(--bg2); border:1px solid var(--border); border-radius:12px;
            padding:18px 20px; display:flex; align-items:center; gap:16px;
            transition:border-color 0.2s;
        }}
        .guest-card:hover {{ border-color:var(--border2); }}
        .guest-avatar {{
            width:44px; height:44px; border-radius:50%;
            background:rgba(201,168,76,0.1); border:1px solid rgba(201,168,76,0.2);
            display:flex; align-items:center; justify-content:center;
            font-size:20px; flex-shrink:0;
        }}
        .guest-info {{ flex:1; min-width:0; }}
        .guest-name {{ font-size:15px; font-weight:600; color:var(--text); }}
        .guest-meta {{ font-size:12px; color:var(--text3); margin-top:3px; }}
        .guest-room {{
            font-size:13px; font-weight:700; color:var(--gold);
            background:rgba(201,168,76,0.08); padding:4px 10px;
            border-radius:8px; flex-shrink:0;
        }}
        .status-badge {{
            font-size:11px; font-weight:600; padding:3px 8px;
            border-radius:6px; flex-shrink:0;
        }}
        .status-pending {{ background:rgba(91,141,239,0.12); color:#5B8DEF; }}
        .status-checked_in {{ background:rgba(76,175,80,0.12); color:#4CAF50; }}
        .status-checked_out {{ background:rgba(136,136,136,0.12); color:#666; }}
        .guest-actions {{ display:flex; gap:8px; flex-shrink:0; }}
        .guest-btn {{
            padding:5px 12px; border-radius:8px; font-size:12px;
            font-weight:600; cursor:pointer; border:none; font-family:inherit;
            transition:opacity 0.2s;
        }}
        .guest-btn:hover {{ opacity:0.8; }}
        .guest-btn-green {{ background:rgba(76,175,80,0.15); color:#4CAF50; }}
        .guest-btn-red {{ background:rgba(224,85,85,0.15); color:#E05555; }}
        .guest-btn-gold {{ background:rgba(201,168,76,0.15); color:#C9A84C; }}
        .guests-empty {{ text-align:center; padding:60px 20px; color:var(--text3); }}

        /* REQUESTS */
        .req-table {{ width:100%; border-collapse:collapse; font-size:13px; }}
        .req-table th {{ background:var(--bg2); color:var(--text3); font-weight:600; font-size:11px;
            text-transform:uppercase; letter-spacing:.5px; padding:10px 14px; text-align:left;
            border-bottom:1px solid var(--border); }}
        .req-table td {{ padding:12px 14px; border-bottom:1px solid var(--border); vertical-align:middle; }}
        .req-table tr:last-child td {{ border-bottom:none; }}
        .req-table tr:hover td {{ background:rgba(201,168,76,0.03); }}
        .req-msg {{ max-width:280px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:var(--text); }}
        .req-cat {{
            display:inline-block; padding:2px 10px; border-radius:10px;
            font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.5px;
        }}
        .req-cat-room_service  {{ background:rgba(60,180,100,0.15); color:#3cb464; }}
        .req-cat-maintenance   {{ background:rgba(220,80,80,0.15); color:#dc5050; }}
        .req-cat-housekeeping  {{ background:rgba(80,140,220,0.15); color:#508cdc; }}
        .req-cat-general       {{ background:rgba(150,150,150,0.15); color:var(--text3); }}
        .req-status {{
            display:inline-flex; align-items:center; gap:6px;
            padding:4px 12px; border-radius:20px; font-size:11px; font-weight:600;
            border:none; cursor:pointer; font-family:inherit; transition:all .15s;
        }}
        .req-status-pending    {{ background:rgba(220,180,0,0.15); color:#d4a800; }}
        .req-status-in_progress {{ background:rgba(80,140,220,0.15); color:#508cdc; }}
        .req-status-resolved   {{ background:rgba(60,180,100,0.15); color:#3cb464; }}
        .req-del {{ background:none; border:none; color:var(--text3); cursor:pointer; font-size:15px;
            padding:4px 8px; border-radius:6px; transition:color .15s; }}
        .req-del:hover {{ color:#e05555; }}
        .req-empty {{ text-align:center; padding:60px 20px; color:var(--text3); }}

        /* ROOM NOTES */
        .note-item {{
            display:flex; align-items:flex-start; gap:8px;
            background:var(--bg2); border:1px solid var(--border); border-radius:8px;
            padding:8px 12px; font-size:12px;
        }}
        .note-text {{ flex:1; color:var(--text2); line-height:1.4; word-break:break-word; }}
        .note-meta {{ font-size:10px; color:var(--text3); white-space:nowrap; margin-top:2px; }}
        .note-del {{ background:none; border:none; color:var(--text3); cursor:pointer;
            font-size:13px; padding:0 2px; line-height:1; }}
        .note-del:hover {{ color:#e05555; }}

        /* CALENDAR */
        .cal-wrap {{ overflow-x:auto; border-radius:12px; border:1px solid var(--border); }}
        .cal-table {{ border-collapse:collapse; min-width:100%; font-size:12px; }}
        .cal-table th {{ background:var(--bg2); color:var(--text3); font-weight:600; font-size:11px;
            padding:8px 6px; text-align:center; border-bottom:1px solid var(--border); white-space:nowrap; }}
        .cal-table td {{ padding:0; border:1px solid var(--border); height:36px; min-width:46px; }}
        .cal-room {{ background:var(--bg2); color:var(--gold); font-weight:700; font-size:12px;
            padding:0 12px; white-space:nowrap; position:sticky; left:0; z-index:2; border-right:2px solid var(--border2); }}
        .cal-cell {{ width:100%; height:100%; display:flex; align-items:center; justify-content:center;
            cursor:default; font-size:10px; font-weight:600; transition:filter .15s; }}
        .cal-cell:hover {{ filter:brightness(1.2); }}
        .cal-vacant {{ background:transparent; color:transparent; }}
        .cal-occupied {{ background:rgba(201,168,76,0.18); color:var(--gold); cursor:pointer; }}
        .cal-checkin {{ background:rgba(60,180,100,0.22); color:#3cb464; cursor:pointer; }}
        .cal-checkout {{ background:rgba(220,80,80,0.18); color:#dc5050; cursor:pointer; }}
        .cal-today-col {{ background:rgba(201,168,76,0.04) !important; }}
        .cal-today-head {{ color:var(--gold) !important; font-weight:800 !important; }}
        .cal-tooltip {{
            position:fixed; background:var(--bg2); border:1px solid var(--border2);
            border-radius:8px; padding:8px 12px; font-size:12px; color:var(--text);
            box-shadow:0 4px 20px rgba(0,0,0,.4); z-index:999; pointer-events:none;
            white-space:nowrap; display:none;
        }}

        /* MANUAL REQUEST MODAL */
        .req-modal-overlay {{
            position:fixed; inset:0; background:rgba(0,0,0,.6); z-index:500;
            display:none; align-items:center; justify-content:center;
        }}
        .req-modal-overlay.open {{ display:flex; }}
        .req-modal {{
            background:var(--bg2); border:1px solid var(--border2); border-radius:16px;
            padding:28px; width:420px; max-width:94vw;
        }}
        .req-modal h3 {{ font-size:16px; font-weight:700; margin-bottom:20px; }}
        .req-modal label {{ font-size:11px; font-weight:700; color:var(--text3);
            text-transform:uppercase; letter-spacing:.5px; display:block; margin-bottom:6px; }}
        .req-modal input, .req-modal select, .req-modal textarea {{
            width:100%; background:var(--bg); border:1px solid var(--border);
            border-radius:8px; padding:10px 14px; color:var(--text); font-family:inherit;
            font-size:13px; outline:none; transition:border-color .2s; margin-bottom:14px;
        }}
        .req-modal input:focus, .req-modal select:focus, .req-modal textarea:focus {{
            border-color:var(--gold);
        }}
        .guest-filter-bar {{ display:flex; gap:8px; margin-bottom:16px; align-items:center; flex-wrap:wrap; }}
        .guest-filter {{
            padding:6px 16px; border-radius:20px; font-size:12px;
            cursor:pointer; border:1px solid var(--border); background:var(--bg2); color:var(--text2);
            transition:all 0.2s; font-family:inherit;
        }}
        .guest-filter:hover {{ border-color:var(--gold); color:var(--gold); }}
        .guest-filter.active {{ background:var(--gold); color:#000; border-color:var(--gold); font-weight:600; }}
        .guest-search {{
            background:var(--bg2); border:1px solid var(--border); border-radius:20px;
            padding:6px 16px; color:var(--text); font-size:13px; outline:none;
            font-family:inherit; width:180px; transition:border-color 0.2s; margin-left:auto;
        }}
        .guest-search:focus {{ border-color:var(--gold); }}
        .guest-search::placeholder {{ color:var(--text3); }}
        .checkin-link-box {{
            background:var(--bg2); border:1px solid var(--border2); border-radius:12px;
            padding:16px 20px; margin-bottom:20px; display:flex;
            align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap;
        }}
        .checkin-link-text {{ font-size:13px; color:var(--gold); word-break:break-all; }}

        /* PLAN USAGE BAR */
        .plan-bar-wrap {{
            background:var(--bg2); border:1px solid var(--border); border-radius:12px;
            padding:16px 20px; margin-bottom:20px; display:none;
        }}
        .plan-bar-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }}
        .plan-badge {{
            font-size:11px; font-weight:700; letter-spacing:1px; text-transform:uppercase;
            background:rgba(201,168,76,0.12); color:var(--gold);
            padding:3px 10px; border-radius:20px; border:1px solid rgba(201,168,76,0.2);
        }}
        .plan-badge.plan-trial {{ background:rgba(91,141,239,0.1); color:#5B8DEF; border-color:rgba(91,141,239,0.2); }}
        .plan-badge.plan-premium {{ background:rgba(76,175,80,0.1); color:#4CAF50; border-color:rgba(76,175,80,0.2); }}
        .plan-usage-text {{ font-size:13px; color:var(--text2); }}
        .plan-track {{ background:var(--bg3); border-radius:6px; height:8px; overflow:hidden; }}
        .plan-fill {{
            height:100%; border-radius:6px;
            background:linear-gradient(90deg,#C9A84C,#E8C96A);
            transition:width 0.6s ease;
        }}
        .plan-fill.warn {{ background:linear-gradient(90deg,#E05555,#ff7070); }}

        /* FILTER BAR */
        .filter-bar {{ display:flex; gap:8px; margin-bottom:16px; align-items:center; flex-wrap:wrap; }}
        .filter {{
            padding:6px 16px; border-radius:20px; font-size:12px;
            cursor:pointer; border:1px solid var(--border); background:var(--bg2); color:var(--text2);
            transition:all 0.2s; font-family:inherit;
        }}
        .filter:hover {{ border-color:var(--gold); color:var(--gold); }}
        .filter.active {{ background:var(--gold); color:#000; border-color:var(--gold); font-weight:600; }}
        .search-input {{
            background:var(--bg2); border:1px solid var(--border); border-radius:20px;
            padding:6px 16px; color:var(--text); font-size:13px; outline:none;
            font-family:inherit; width:160px; transition:border-color 0.2s;
        }}
        .search-input:focus {{ border-color:var(--gold); }}
        .search-input::placeholder {{ color:var(--text3); }}

        /* TABLE */
        .table-wrap {{ background:var(--bg2); border-radius:12px; border:1px solid var(--border); overflow:hidden; }}
        table {{ width:100%; border-collapse:collapse; }}
        th {{
            background:rgba(201,168,76,0.08); color:var(--gold);
            padding:12px 16px; text-align:left; font-size:11px;
            letter-spacing:1px; text-transform:uppercase;
            border-bottom:1px solid var(--border2);
        }}
        td {{ padding:12px 16px; border-bottom:1px solid var(--border); font-size:14px; }}
        tr:last-child td {{ border-bottom:none; }}
        tr.clickable {{ cursor:pointer; }}
        tr.clickable:hover td {{ background:rgba(201,168,76,0.04); }}
        tr.urgent-row td {{ background:rgba(224,85,85,0.04); }}
        tr.urgent-row:hover td {{ background:rgba(224,85,85,0.08); }}

        .badge {{ display:inline-flex; align-items:center; gap:5px; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:500; }}
        .badge-urgent {{ background:rgba(224,85,85,0.12); color:#E05555; border:1px solid rgba(224,85,85,0.25); }}
        .badge-normal {{ background:rgba(76,175,80,0.12); color:#4CAF50; border:1px solid rgba(76,175,80,0.25); }}
        .badge-user {{ background:rgba(91,141,239,0.12); color:#5B8DEF; border:1px solid rgba(91,141,239,0.25); }}
        .badge-bot {{ background:rgba(201,168,76,0.12); color:var(--gold); border:1px solid rgba(201,168,76,0.25); }}
        .badge-staff {{ background:rgba(76,175,80,0.12); color:#4CAF50; border:1px solid rgba(76,175,80,0.25); }}
        .room-tag {{ background:var(--bg3); border:1px solid var(--border); padding:3px 9px; border-radius:6px; font-size:12px; color:var(--gold); }}
        .msg-preview {{ max-width:340px; overflow:hidden; white-space:nowrap; text-overflow:ellipsis; color:var(--text2); }}

        /* PAGINATION */
        .pagination {{ display:flex; justify-content:center; gap:8px; padding:16px; }}
        .page-btn {{ padding:6px 14px; border-radius:8px; font-size:13px; cursor:pointer; border:1px solid var(--border); background:var(--bg2); color:var(--text2); font-family:inherit; transition:all 0.2s; }}
        .page-btn:hover, .page-btn.active {{ border-color:var(--gold); color:var(--gold); background:rgba(201,168,76,0.08); }}

        /* MODAL */
        .modal-overlay {{
            display:none; position:fixed; inset:0; background:rgba(0,0,0,0.75);
            z-index:1000; align-items:center; justify-content:center; padding:16px;
        }}
        .modal-overlay.open {{ display:flex; }}
        .modal {{
            background:var(--bg2); border-radius:20px; width:100%; max-width:560px;
            max-height:88vh; display:flex; flex-direction:column;
            border:1px solid var(--border2); box-shadow:0 24px 80px rgba(0,0,0,0.5);
            animation:modalIn 0.25s ease;
        }}
        @keyframes modalIn {{ from{{opacity:0;transform:scale(0.95)}} to{{opacity:1;transform:scale(1)}} }}
        .modal-header {{
            padding:20px 24px 16px; border-bottom:1px solid var(--border);
            display:flex; justify-content:space-between; align-items:center; flex-shrink:0;
        }}
        .modal-title {{ font-size:16px; font-weight:700; color:var(--gold); }}
        .modal-close {{
            background:var(--bg3); border:1px solid var(--border); color:var(--text2);
            width:32px; height:32px; border-radius:50%; cursor:pointer;
            font-size:16px; display:flex; align-items:center; justify-content:center;
        }}
        .modal-close:hover {{ color:var(--text); }}
        .modal-body {{ flex:1; overflow-y:auto; padding:20px 24px; display:flex; flex-direction:column; gap:12px; }}
        .modal-body::-webkit-scrollbar {{ width:4px; }}
        .modal-body::-webkit-scrollbar-thumb {{ background:rgba(201,168,76,0.2); border-radius:4px; }}

        .chat-bubble-wrap {{ display:flex; gap:8px; align-items:flex-end; }}
        .chat-bubble-wrap.right {{ flex-direction:row-reverse; }}
        .bubble-avatar {{ width:28px; height:28px; border-radius:50%; background:rgba(201,168,76,0.12); display:flex; align-items:center; justify-content:center; font-size:13px; flex-shrink:0; }}
        .bubble {{
            padding:10px 14px; border-radius:16px; max-width:76%; font-size:14px; line-height:1.55; word-wrap:break-word;
        }}
        .bubble.user {{ background:linear-gradient(135deg,#C9A84C,#E8C96A); color:#1a1a1a; font-weight:500; border-bottom-right-radius:4px; }}
        .bubble.bot {{ background:var(--bg3); color:var(--text); border-bottom-left-radius:4px; }}
        .bubble.staff {{ background:rgba(76,175,80,0.12); color:#4CAF50; border:1px solid rgba(76,175,80,0.2); border-bottom-left-radius:4px; }}
        .bubble-time {{ font-size:10px; color:var(--text3); margin-top:4px; }}

        .modal-footer {{
            padding:16px 24px; border-top:1px solid var(--border); flex-shrink:0;
            display:flex; gap:10px;
        }}
        .reply-input {{
            flex:1; background:var(--bg3); border:1px solid var(--border);
            border-radius:12px; padding:11px 16px; color:var(--text);
            font-size:14px; outline:none; font-family:inherit; resize:none; height:44px;
            transition:border-color 0.2s;
        }}
        .reply-input:focus {{ border-color:var(--gold); }}
        .reply-input::placeholder {{ color:var(--text3); }}
        .reply-btn {{
            background:var(--gold); color:#000; border:none; border-radius:12px;
            padding:0 20px; font-size:14px; font-weight:600; cursor:pointer;
            font-family:inherit; transition:background 0.2s; white-space:nowrap;
        }}
        .reply-btn:hover {{ background:var(--gold2); }}

        /* CHARTS */
        .charts-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:28px; }}
        .chart-card {{ background:var(--bg2); border-radius:12px; padding:20px; border:1px solid var(--border); }}
        .chart-title {{ font-size:12px; color:var(--text3); margin-bottom:14px; letter-spacing:1px; text-transform:uppercase; }}
        .chart-wrap {{ height:140px; display:flex; align-items:flex-end; gap:6px; }}
        .bar-item {{ flex:1; display:flex; flex-direction:column; align-items:center; gap:5px; }}
        .bar-fill {{ width:100%; border-radius:4px 4px 0 0; min-height:3px; position:relative; cursor:default; }}
        .bar-fill:hover::after {{
            content:attr(data-value); position:absolute; top:-26px; left:50%; transform:translateX(-50%);
            background:#333; color:white; padding:2px 8px; border-radius:4px; font-size:11px; white-space:nowrap; pointer-events:none;
        }}
        .bar-label {{ font-size:10px; color:var(--text3); text-align:center; }}
        .top-rooms {{ display:flex; flex-direction:column; gap:10px; }}
        .room-bar-item {{ display:flex; align-items:center; gap:12px; }}
        .room-bar-name {{ font-size:13px; color:var(--gold); width:56px; flex-shrink:0; }}
        .room-bar-track {{ flex:1; background:var(--border); border-radius:4px; height:7px; overflow:hidden; }}
        .room-bar-fill {{ height:100%; border-radius:4px; background:linear-gradient(90deg,#C9A84C,#E8C96A); }}
        .room-bar-count {{ font-size:12px; color:var(--text3); width:28px; text-align:right; }}

        /* ANALYTICS */
        .analytics-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:24px; }}
        .an-card {{
            background:var(--bg2); border:1px solid var(--border); border-radius:12px;
            padding:20px; text-align:center;
        }}
        .an-num {{ font-size:30px; font-weight:900; color:var(--gold); line-height:1; }}
        .an-label {{ font-size:12px; color:var(--text3); margin-top:6px; }}
        .an-sub {{ font-size:11px; color:var(--text3); margin-top:3px; }}
        .an-section {{ background:var(--bg2); border:1px solid var(--border); border-radius:12px; padding:20px; margin-bottom:16px; }}
        .an-title {{ font-size:11px; color:var(--text3); letter-spacing:1.5px; text-transform:uppercase; margin-bottom:16px; }}
        /* Rating distribution */
        .dist-row {{ display:flex; align-items:center; gap:10px; margin-bottom:8px; }}
        .dist-star {{ font-size:13px; color:var(--gold); width:28px; flex-shrink:0; text-align:right; }}
        .dist-track {{ flex:1; background:var(--bg3); border-radius:4px; height:10px; overflow:hidden; }}
        .dist-fill {{ height:100%; border-radius:4px; background:linear-gradient(90deg,#C9A84C,#E8C96A); transition:width 0.6s ease; }}
        .dist-fill.low {{ background:linear-gradient(90deg,#E05555,#ff7070); }}
        .dist-fill.mid {{ background:linear-gradient(90deg,#E8A040,#f0c060); }}
        .dist-count {{ font-size:12px; color:var(--text3); width:28px; text-align:right; flex-shrink:0; }}
        /* Trend bars */
        .trend-wrap {{ display:flex; align-items:flex-end; gap:6px; height:80px; }}
        .trend-bar {{ flex:1; display:flex; flex-direction:column; align-items:center; gap:4px; }}
        .trend-fill {{
            width:100%; border-radius:4px 4px 0 0; min-height:3px;
            background:linear-gradient(to top,#C9A84C,#E8C96A); position:relative;
        }}
        .trend-fill:hover::after {{
            content:attr(data-tip); position:absolute; top:-28px; left:50%; transform:translateX(-50%);
            background:#333; color:white; padding:2px 8px; border-radius:4px; font-size:11px;
            white-space:nowrap; pointer-events:none;
        }}
        .trend-label {{ font-size:9px; color:var(--text3); text-align:center; }}
        /* Nationalities */
        .nat-row {{ display:flex; align-items:center; gap:10px; margin-bottom:8px; }}
        .nat-name {{ font-size:13px; color:var(--text); width:90px; flex-shrink:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
        .nat-track {{ flex:1; background:var(--bg3); border-radius:4px; height:8px; overflow:hidden; }}
        .nat-fill {{ height:100%; border-radius:4px; background:linear-gradient(90deg,#5B8DEF,#7BA5F5); }}
        .nat-count {{ font-size:12px; color:var(--text3); width:24px; text-align:right; flex-shrink:0; }}
        .an-two {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px; }}
        @media(max-width:768px) {{
            .analytics-grid {{ grid-template-columns:repeat(2,1fr); }}
            .an-two {{ grid-template-columns:1fr; }}
        }}

        /* RATINGS */
        .rating-card {{
            background:var(--bg2); border:1px solid var(--border); border-radius:12px;
            padding:16px 20px; display:flex; align-items:center; gap:16px;
        }}
        .rating-stars {{ font-size:18px; flex-shrink:0; letter-spacing:1px; }}
        .rating-info {{ flex:1; min-width:0; }}
        .rating-guest {{ font-size:14px; font-weight:600; color:var(--text); }}
        .rating-meta {{ font-size:12px; color:var(--text3); margin-top:3px; }}
        .rating-room {{ font-size:13px; font-weight:700; color:var(--gold); background:rgba(201,168,76,0.08); padding:4px 10px; border-radius:8px; flex-shrink:0; }}
        .rating-avg-card {{
            background:var(--bg2); border:1px solid var(--border2); border-radius:12px;
            padding:24px; text-align:center; margin-bottom:20px;
        }}
        .rating-avg-num {{ font-size:48px; font-weight:900; color:var(--gold); line-height:1; }}
        .rating-avg-stars {{ font-size:24px; margin:8px 0 4px; }}
        .rating-avg-sub {{ font-size:13px; color:var(--text3); }}

        /* MISC */
        @keyframes slideIn {{ from{{transform:translateX(110px);opacity:0}} to{{transform:translateX(0);opacity:1}} }}
        .live-dot {{
            display:inline-block; width:7px; height:7px; border-radius:50%;
            background:#4CAF50; margin-right:6px; animation:blink 2s infinite;
        }}
        @keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}
        .empty-state {{ text-align:center; padding:48px 20px; color:var(--text3); }}
        .empty-state .icon {{ font-size:40px; margin-bottom:12px; }}

        /* MOBILE HAMBURGER + DRAWER */
        .hamburger {{
            display:none; align-items:center; justify-content:center;
            position:fixed; top:14px; left:14px; z-index:300;
            width:42px; height:42px; border-radius:10px;
            background:var(--bg2); border:1px solid var(--border2);
            cursor:pointer; font-size:20px; color:var(--text);
            box-shadow:0 2px 12px rgba(0,0,0,.3);
        }}
        .mob-overlay {{
            display:none; position:fixed; inset:0;
            background:rgba(0,0,0,.55); z-index:150;
        }}
        .mob-overlay.open {{ display:block; }}

        @media(max-width:767px) {{
            .hamburger {{ display:flex; }}
            .sidebar {{
                transform:translateX(-100%);
                transition:transform 0.25s ease;
                z-index:200; box-shadow:4px 0 24px rgba(0,0,0,.5);
            }}
            .sidebar.mob-open {{ transform:translateX(0); }}
            .main {{
                margin-left:0; padding:16px;
                padding-top:68px; /* room for hamburger */
            }}
            .page-header {{ flex-direction:column; gap:10px; align-items:flex-start; }}
            .header-btns {{ width:100%; display:flex; }}
            .header-btns .btn {{ flex:1; text-align:center; }}
            .stats {{ grid-template-columns:1fr 1fr; gap:10px; }}
            .stat {{ padding:14px; }}
            .stat-num {{ font-size:26px; }}
            .charts-grid {{ grid-template-columns:1fr; }}
            .filter-bar {{ gap:6px; }}
            table {{ font-size:12px; }}
            th {{ padding:8px 10px; font-size:10px; }}
            td {{ padding:8px 10px; }}
            .msg-preview {{ max-width:140px; }}
            .hide-mobile {{ display:none !important; }}
            .cal-wrap {{ font-size:11px; }}
            .guest-actions {{ flex-wrap:wrap; }}
            .req-modal {{ padding:20px; }}
            /* Staff chat full-height on mobile */
            #staffChatView > div:last-child {{ height:calc(100vh - 140px) !important; }}
        }}
        @media(max-width:480px) {{
            .stats {{ grid-template-columns:1fr 1fr; }}
        }}
    </style>
</head>
<body>
    <!-- MOBILE HAMBURGER + OVERLAY -->
    <button class="hamburger" id="hamburger" onclick="toggleMobNav()" aria-label="Меню">☰</button>
    <div class="mob-overlay" id="mobOverlay" onclick="closeMobNav()"></div>

    <!-- SIDEBAR -->
    <div class="sidebar" id="sidebar">
        <div class="sidebar-logo">
            <h2>🏨 SmartStay AI</h2>
            <p id="hotelName">Yükleniyor...</p>
        </div>
        <div class="sidebar-nav">
        <button type="button" class="nav-item active" id="navAll" onclick="setFilter('all',this)">
            <span class="nav-icon">📊</span> <span id="nt_all">All Messages</span>
        </button>
        <button type="button" class="nav-item" id="navUrgent" onclick="setFilter('urgent',this)">
            <span class="nav-icon">🔴</span> <span id="nt_urgent">Urgent</span>
        </button>
        <button type="button" class="nav-item" id="navGuest" onclick="setFilter('user',this)">
            <span class="nav-icon">👤</span> <span id="nt_guest">Guest</span>
        </button>
        <button type="button" class="nav-item" id="navRooms" onclick="showRoomsView()">
            <span class="nav-icon">🚪</span> <span id="nt_rooms">Rooms</span>
        </button>
        <button type="button" class="nav-item" id="navGuests" onclick="showGuestsView()">
            <span class="nav-icon">🛎️</span> <span id="nt_checkin">Check-in</span> <span id="guestsBadge" style="display:none;background:#C9A84C;color:#000;border-radius:10px;font-size:10px;font-weight:700;padding:1px 6px;margin-left:4px">0</span>
        </button>
        <button type="button" class="nav-item" id="navCalendar" onclick="showCalendarView()">
            <span class="nav-icon">📅</span> <span id="nt_calendar">Calendar</span>
        </button>
        <button type="button" class="nav-item" id="navRequests" onclick="showRequestsView()">
            <span class="nav-icon">📋</span> <span id="nt_requests">Requests</span> <span id="requestsBadge" style="display:none;background:#dc5050;color:#fff;border-radius:10px;font-size:10px;font-weight:700;padding:1px 6px;margin-left:4px">0</span>
        </button>
        <button type="button" class="nav-item" id="navRatings" onclick="showRatingsView()">
            <span class="nav-icon">⭐</span> <span id="nt_ratings">Ratings</span>
        </button>
        <button type="button" class="nav-item" id="navAnalytics" onclick="showAnalyticsView()">
            <span class="nav-icon">📊</span> <span id="nt_analytics">Analytics</span>
        </button>
        <button type="button" class="nav-item" id="navServices" onclick="showServicesView()">
            <span class="nav-icon">🛎️</span> <span id="nt_services">Services</span>
        </button>
        <button type="button" class="nav-item" id="navStaffChat" onclick="showStaffChatView()">
            <span class="nav-icon">💬</span> <span id="nt_staffchat">Staff Chat</span>
            <span id="scBadge" style="display:none;background:#E05555;color:#fff;border-radius:10px;font-size:10px;font-weight:700;padding:1px 6px;margin-left:auto;min-width:18px;text-align:center">0</span>
        </button>
        <button type="button" class="nav-item manager-only" id="navStaff" onclick="showStaffView()">
            <span class="nav-icon">👥</span> <span id="nt_staff">Staff</span>
        </button>
        <button type="button" class="nav-item manager-only" onclick="goToBuffet()">
            <span class="nav-icon">🍽️</span> <span id="nt_buffet">Buffet AI</span>
        </button>
        </div>
        <div class="sidebar-bottom">
            <button type="button" class="nav-item" onclick="goToEdit()" style="border-radius:8px;">
                <span class="nav-icon">⚙️</span> <span id="nt_settings">Settings</span>
            </button>
            <button type="button" class="nav-item" onclick="goToQR()" style="border-radius:8px;">
                <span class="nav-icon">📱</span> <span id="nt_qr">QR Codes</span>
            </button>
            <button type="button" class="nav-item" onclick="toggleTheme()" style="border-radius:8px;" id="themeNav">
                <span class="nav-icon">☀️</span> <span id="themeLabel">Light mode</span>
            </button>
            <div style="display:flex;gap:4px;padding:6px 2px;flex-wrap:wrap">
                <button class="lang-btn-dash" onclick="setDashLang('en')">EN</button>
                <button class="lang-btn-dash" onclick="setDashLang('ru')">RU</button>
                <button class="lang-btn-dash" onclick="setDashLang('tr')">TR</button>
                <button class="lang-btn-dash" onclick="setDashLang('uz')">UZ</button>
            </div>
        </div>
    </div>

    <!-- MAIN -->
    <div class="main">
        <div class="page-header">
            <div>
                <div class="page-title" id="pageTitle">Manager Dashboard</div>
                <div class="page-sub"><span class="live-dot"></span><span id="liveStatus">Live • Updates every 3s</span></div>
            </div>
            <div class="header-btns">
                <button class="btn btn-dark" onclick="markRead()">✅ Okundu</button>
                <button class="btn btn-dark" onclick="exportExcel()">📥 Excel</button>
                <button class="btn btn-gold" onclick="loadData()">🔄 Yenile</button>
            </div>
        </div>

        <!-- STATS -->
        <div class="stats">
            <div class="stat">
                <div class="stat-icon">💬</div>
                <div class="stat-num" id="statTotal">—</div>
                <div class="stat-label" id="lblStatTotal">Total Messages</div>
            </div>
            <div class="stat red">
                <div class="stat-icon">🔴</div>
                <div class="stat-num" id="statUrgent">—</div>
                <div class="stat-label" id="lblStatUrgent">Urgent</div>
            </div>
            <div class="stat green">
                <div class="stat-icon">🚪</div>
                <div class="stat-num" id="statRooms">—</div>
                <div class="stat-label" id="lblStatRooms">Active Rooms</div>
            </div>
            <div class="stat blue">
                <div class="stat-icon">📬</div>
                <div class="stat-num" id="statUnread">—</div>
                <div class="stat-label" id="lblStatUnread">Unread</div>
            </div>
            <div class="stat purple">
                <div class="stat-icon">⭐</div>
                <div class="stat-num" id="statRating">—</div>
                <div class="stat-label" id="lblStatRating">Avg. Rating</div>
            </div>
        </div>

        <!-- PLAN USAGE -->
        <div class="plan-bar-wrap" id="planBar">
            <div class="plan-bar-header">
                <span class="plan-badge" id="planBadge">TRIAL</span>
                <span class="plan-usage-text" id="planUsageText">— / — mesaj</span>
            </div>
            <div class="plan-track">
                <div class="plan-fill" id="planFill" style="width:0%"></div>
            </div>
        </div>

        <!-- CHARTS (Chart.js) -->
        <div id="chartsGrid" style="display:none">
            <!-- KPI row -->
            <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px;margin-bottom:20px">
                <div class="chart-card" style="padding:16px;text-align:center">
                    <div class="chart-title" id="kpiGuestsLbl">GUESTS</div>
                    <div id="kpi-guests" style="font-size:28px;font-weight:800;color:var(--gold)">—</div>
                </div>
                <div class="chart-card" style="padding:16px;text-align:center">
                    <div class="chart-title" id="kpiMsgLbl">MESSAGED</div>
                    <div id="kpi-messaged" style="font-size:28px;font-weight:800;color:#4ab0e8">—</div>
                </div>
                <div class="chart-card" style="padding:16px;text-align:center">
                    <div class="chart-title" id="kpiRatedLbl">RATED</div>
                    <div id="kpi-rated" style="font-size:28px;font-weight:800;color:#4CAF50">—</div>
                </div>
                <div class="chart-card" style="padding:16px;text-align:center">
                    <div class="chart-title" id="kpiRespLbl">RESPONSE (MIN)</div>
                    <div id="kpi-response" style="font-size:28px;font-weight:800;color:#a04ae8">—</div>
                </div>
            </div>
            <!-- Main charts row -->
            <div class="charts-grid">
                <div class="chart-card" style="grid-column:1/-1">
                    <div class="chart-title" id="chartDaysTitle">📈 Guest messages — last 30 days</div>
                    <div style="height:160px;position:relative"><canvas id="chartDays"></canvas></div>
                </div>
                <div class="chart-card">
                    <div class="chart-title" id="chartHoursTitle">🕐 Activity by hour</div>
                    <div style="height:160px;position:relative"><canvas id="chartHours"></canvas></div>
                </div>
                <div class="chart-card">
                    <div class="chart-title" id="chartRatingsTitle">⭐ Rating distribution</div>
                    <div style="height:160px;position:relative"><canvas id="chartRatings"></canvas></div>
                </div>
            </div>
            <!-- Categories + funnel -->
            <div class="charts-grid" style="margin-top:14px">
                <div class="chart-card">
                    <div class="chart-title" id="chartCatsTitle">📋 Top request categories</div>
                    <div style="height:160px;position:relative"><canvas id="chartCategories"></canvas></div>
                    <div id="noCats" style="display:none;color:var(--text3);font-size:13px;margin-top:8px" id="noCatsLbl">No data yet</div>
                </div>
                <div class="chart-card">
                    <div class="chart-title" id="chartFunnelTitle">🔽 Engagement funnel</div>
                    <div id="funnelChart" style="padding:8px 0"></div>
                </div>
            </div>
        </div>

        <!-- MESSAGES VIEW -->
        <div id="messagesView">
            <div class="filter-bar">
                <button class="filter active" id="fAll" onclick="setFilter('all',this)"><span id="fAllLbl">All</span></button>
                <button class="filter" id="fUrgent" onclick="setFilter('urgent',this)">🔴 <span id="fUrgentLbl">Urgent</span></button>
                <button class="filter" id="fUser" onclick="setFilter('user',this)">👤 <span id="fUserLbl">Guest</span></button>
                <button class="filter" id="fBot" onclick="setFilter('bot',this)">🤖 AI</button>
                <input class="search-input" id="roomSearch" placeholder="🔍 Room..." oninput="applyFilters()">
                <span id="unreadBadge" style="margin-left:auto"></span>
            </div>
            <div class="table-wrap">
                <table>
                    <thead><tr>
                        <th id="thPriority">Priority</th><th id="thRoom">Room</th><th class="hide-mobile" id="thWho">Who</th><th id="thMsg">Message</th><th class="hide-mobile" id="thTime">Time</th><th></th>
                    </tr></thead>
                    <tbody id="tbody"></tbody>
                </table>
                <div class="pagination" id="pagination"></div>
            </div>
        </div>

        <!-- GUESTS VIEW -->
        <div id="guestsView" style="display:none">
            <div class="page-header" style="margin-bottom:20px">
                <div>
                    <div class="page-title" id="guestsTitle">🛎️ Check-in List</div>
                    <div class="page-sub" id="guestsSub">Guests who completed digital check-in</div>
                </div>
                <div class="header-btns">
                    <button class="btn btn-gold btn-sm" onclick="loadGuests()">↻ <span id="btnRefresh">Refresh</span></button>
                    <button class="btn btn-dark btn-sm" onclick="openCheckinLink()">🔗 <span id="btnCheckinLink">Check-in Link</span></button>
                    <button class="btn btn-dark btn-sm" onclick="exportGuests()">📥 Excel</button>
                </div>
            </div>
            <div class="checkin-link-box" id="checkinLinkBox" style="display:none">
                <div>
                    <div style="font-size:11px;color:var(--text3);margin-bottom:4px;letter-spacing:1px;text-transform:uppercase">Misafir Check-in Linki</div>
                    <div class="checkin-link-text" id="checkinLinkText"></div>
                </div>
                <button class="btn btn-gold btn-sm" onclick="copyCheckinLink()">📋 Kopyala</button>
            </div>
            <div class="guest-filter-bar">
                <button class="guest-filter active" data-status="" onclick="setGuestFilter('',this)" id="gfAll">All</button>
                <button class="guest-filter" data-status="pending" onclick="setGuestFilter('pending',this)" id="gfPending">⏳ Pending</button>
                <button class="guest-filter" data-status="checked_in" onclick="setGuestFilter('checked_in',this)" id="gfIn">✅ Checked In</button>
                <button class="guest-filter" data-status="checked_out" onclick="setGuestFilter('checked_out',this)" id="gfOut">🚪 Checked Out</button>
                <input class="guest-search" id="guestSearch" placeholder="🔍 Name or room..." oninput="renderGuests()">
            </div>
            <div id="guestsList" style="display:flex;flex-direction:column;gap:10px">
                <div class="guests-empty">Yükleniyor...</div>
            </div>
        </div>

        <!-- CALENDAR VIEW -->
        <div id="calendarView" style="display:none">
            <div class="page-header" style="margin-bottom:20px">
                <div>
                    <h2 style="font-size:20px;font-weight:700;margin:0">📅 Doluluk Takvimi</h2>
                    <p style="color:var(--text3);font-size:13px;margin:4px 0 0">Oda bazında check-in / check-out planı</p>
                </div>
                <div style="display:flex;gap:12px;align-items:center;font-size:12px;color:var(--text3)">
                    <span><span style="display:inline-block;width:12px;height:12px;background:rgba(60,180,100,0.3);border-radius:3px;vertical-align:middle;margin-right:4px"></span>Check-in</span>
                    <span><span style="display:inline-block;width:12px;height:12px;background:rgba(201,168,76,0.2);border-radius:3px;vertical-align:middle;margin-right:4px"></span>Dolu</span>
                    <span><span style="display:inline-block;width:12px;height:12px;background:rgba(220,80,80,0.2);border-radius:3px;vertical-align:middle;margin-right:4px"></span>Check-out</span>
                    <button class="btn btn-outline btn-sm" onclick="loadCalendar()">↻ Yenile</button>
                </div>
            </div>
            <div class="cal-wrap">
                <div id="calendarGrid">
                    <div style="text-align:center;padding:60px;color:var(--text3)">Yükleniyor…</div>
                </div>
            </div>
        </div>

        <!-- TOOLTIP for calendar -->
        <div class="cal-tooltip" id="calTooltip"></div>

        <!-- MANUAL REQUEST MODAL -->
        <div class="req-modal-overlay" id="reqModalOverlay" onclick="if(event.target===this)closeReqModal()">
            <div class="req-modal">
                <h3>➕ Yeni Talep Ekle</h3>
                <label>ODA NUMARASI</label>
                <input type="text" id="reqRoom" placeholder="101">
                <label>MİSAFİR ADI (isteğe bağlı)</label>
                <input type="text" id="reqGuest" placeholder="Ad Soyad">
                <label>KATEGORİ</label>
                <select id="reqCat">
                    <option value="general">📌 Genel</option>
                    <option value="room_service">🍽 Oda Servisi</option>
                    <option value="maintenance">🔧 Bakım</option>
                    <option value="housekeeping">🧹 Temizlik</option>
                </select>
                <label>TALEP DETAYI</label>
                <textarea id="reqMsg" rows="3" placeholder="Talep açıklaması..."></textarea>
                <div style="display:flex;gap:10px;justify-content:flex-end">
                    <button class="btn btn-dark" onclick="closeReqModal()">İptal</button>
                    <button class="btn btn-gold" onclick="submitManualRequest()">💾 Kaydet</button>
                </div>
            </div>
        </div>

        <!-- REQUESTS VIEW -->
        <div id="requestsView" style="display:none">
            <div class="page-header" style="margin-bottom:20px">
                <div>
                    <h2 style="font-size:20px;font-weight:700;margin:0">📋 Misafir Talepleri</h2>
                    <p style="color:var(--text3);font-size:13px;margin:4px 0 0">Oda servisi, bakım ve temizlik talepleri</p>
                </div>
                <div style="display:flex;gap:8px;align-items:center">
                    <button class="btn btn-gold btn-sm" onclick="openReqModal()">➕ Yeni Talep</button>
                    <select id="reqStatusFilter" onchange="loadRequests()" style="background:var(--bg2);border:1px solid var(--border);border-radius:8px;padding:7px 12px;color:var(--text);font-family:inherit;font-size:13px;cursor:pointer">
                        <option value="">Tümü</option>
                        <option value="pending">⏳ Bekliyor</option>
                        <option value="in_progress">🔄 İşlemde</option>
                        <option value="resolved">✅ Çözüldü</option>
                    </select>
                    <button class="btn btn-outline btn-sm" onclick="loadRequests()">↻ Yenile</button>
                </div>
            </div>
            <div style="background:var(--bg2);border:1px solid var(--border);border-radius:12px;overflow:hidden">
                <table class="req-table">
                    <thead>
                        <tr>
                            <th>Oda</th>
                            <th class="hide-mobile">Misafir</th>
                            <th class="hide-mobile">Kategori</th>
                            <th>Talep</th>
                            <th>Durum</th>
                            <th class="hide-mobile">Zaman</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody id="requestsList">
                        <tr><td colspan="7" class="req-empty">Yükleniyor…</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- SERVICES VIEW -->
        <div id="servicesView" style="display:none">
            <div class="page-header" style="margin-bottom:20px">
                <div>
                    <div class="page-title" id="svcPageTitle">🛎️ Services Menu</div>
                    <div style="font-size:13px;color:var(--text2);margin-top:4px" id="svcSubTitle">Hotel services catalog</div>
                </div>
                <button class="btn-gold" id="svcAddBtn" onclick="openSvcForm()">+ Add Service</button>
            </div>

            <!-- Add/Edit form -->
            <div id="svcFormBox" style="display:none;background:var(--bg2);border:1px solid var(--border);border-radius:16px;padding:24px;margin-bottom:24px">
                <div style="font-size:14px;font-weight:700;margin-bottom:16px" id="svcFormTitle">New Service</div>
                <input type="hidden" id="svcEditId">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
                    <div>
                        <label style="font-size:12px;color:var(--text2);display:block;margin-bottom:6px" id="svcLblIcon">ICON (emoji)</label>
                        <input id="svcIcon" type="text" value="🛎️" style="width:100%;padding:10px 14px;background:var(--bg3);border:1px solid var(--border);border-radius:10px;color:var(--text);font-size:18px">
                    </div>
                    <div>
                        <label style="font-size:12px;color:var(--text2);display:block;margin-bottom:6px" id="svcLblCategory">CATEGORY</label>
                        <select id="svcCategory" style="width:100%;padding:10px 14px;background:var(--bg3);border:1px solid var(--border);border-radius:10px;color:var(--text);font-size:14px">
                            <option value="general" id="svcCatGeneral">🛎️ General</option>
                            <option value="food" id="svcCatFood">🍽️ Food & Drinks</option>
                            <option value="housekeeping" id="svcCatHousekeeping">🧹 Housekeeping</option>
                            <option value="spa" id="svcCatSpa">💆 Spa</option>
                            <option value="transport" id="svcCatTransport">🚖 Transport</option>
                            <option value="maintenance" id="svcCatMaintenance">🔧 Maintenance</option>
                        </select>
                    </div>
                </div>
                <div style="margin-bottom:12px">
                    <label style="font-size:12px;color:var(--text2);display:block;margin-bottom:6px" id="svcLblName">SERVICE NAME</label>
                    <input id="svcName" type="text" placeholder="e.g. Breakfast in room" style="width:100%;padding:10px 14px;background:var(--bg3);border:1px solid var(--border);border-radius:10px;color:var(--text);font-size:14px">
                </div>
                <div style="margin-bottom:12px">
                    <label style="font-size:12px;color:var(--text2);display:block;margin-bottom:6px" id="svcLblDesc">DESCRIPTION (optional)</label>
                    <input id="svcDesc" type="text" placeholder="Brief description for guests" style="width:100%;padding:10px 14px;background:var(--bg3);border:1px solid var(--border);border-radius:10px;color:var(--text);font-size:14px">
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
                    <div>
                        <label style="font-size:12px;color:var(--text2);display:block;margin-bottom:6px" id="svcLblPrice">PRICE (0 = free)</label>
                        <input id="svcPrice" type="number" value="0" min="0" step="0.01" style="width:100%;padding:10px 14px;background:var(--bg3);border:1px solid var(--border);border-radius:10px;color:var(--text);font-size:14px">
                    </div>
                    <div>
                        <label style="font-size:12px;color:var(--text2);display:block;margin-bottom:6px" id="svcLblCurrency">CURRENCY</label>
                        <select id="svcCurrency" style="width:100%;padding:10px 14px;background:var(--bg3);border:1px solid var(--border);border-radius:10px;color:var(--text);font-size:14px">
                            <option value="USD">USD $</option>
                            <option value="EUR">EUR €</option>
                            <option value="TRY">TRY ₺</option>
                            <option value="RUB">RUB ₽</option>
                            <option value="AED">AED د.إ</option>
                        </select>
                    </div>
                </div>
                <div style="display:flex;gap:10px">
                    <button class="btn-gold" style="flex:1" id="svcSaveBtn" onclick="saveSvc()">💾 Save</button>
                    <button id="svcCancelBtn" onclick="closeSvcForm()" style="flex:1;padding:10px;background:var(--bg3);border:1px solid var(--border);border-radius:10px;color:var(--text2);cursor:pointer;font-size:14px">Cancel</button>
                </div>
                <div id="svcFormMsg" style="font-size:13px;margin-top:10px;display:none"></div>
            </div>

            <!-- Services grid -->
            <div id="svcGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px">
                <div style="color:var(--text2);font-size:14px;padding:20px">Загрузка...</div>
            </div>
        </div>

        <!-- STAFF VIEW (manager only) -->
        <div id="staffView" style="display:none">
            <div class="page-header" style="margin-bottom:20px">
                <div>
                    <h2 style="font-size:20px;font-weight:700">👥 Personel Yönetimi</h2>
                    <div style="color:#888;font-size:13px">Otele erişimi olan çalışanlar</div>
                </div>
            </div>
            <!-- Add staff form -->
            <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:20px;margin-bottom:24px">
                <div style="font-weight:600;font-size:14px;margin-bottom:14px;color:#C9A84C">➕ Yeni Personel Ekle</div>
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr auto;gap:10px;align-items:end">
                    <div>
                        <div style="font-size:11px;color:#888;margin-bottom:4px">AD SOYAD</div>
                        <input type="text" id="newStaffName" placeholder="Ahmet Yılmaz"
                               style="width:100%;padding:8px 10px;background:#111;border:1px solid #333;border-radius:6px;color:#f0f0f0;font-size:13px">
                    </div>
                    <div>
                        <div style="font-size:11px;color:#888;margin-bottom:4px">KULLANICI ADI</div>
                        <input type="text" id="newStaffUser" placeholder="ahmet.yilmaz"
                               style="width:100%;padding:8px 10px;background:#111;border:1px solid #333;border-radius:6px;color:#f0f0f0;font-size:13px">
                    </div>
                    <div>
                        <div style="font-size:11px;color:#888;margin-bottom:4px">ŞİFRE</div>
                        <input type="password" id="newStaffPass" placeholder="min. 6 karakter"
                               style="width:100%;padding:8px 10px;background:#111;border:1px solid #333;border-radius:6px;color:#f0f0f0;font-size:13px">
                    </div>
                    <div>
                        <div style="font-size:11px;color:#888;margin-bottom:4px">ROL</div>
                        <select id="newStaffRole"
                                style="width:100%;padding:8px 10px;background:#111;border:1px solid #333;border-radius:6px;color:#f0f0f0;font-size:13px">
                            <option value="receptionist">Resepsiyon</option>
                            <option value="housekeeping">Housekeeping</option>
                            <option value="manager">Yönetici</option>
                        </select>
                    </div>
                    <button onclick="addStaffMember()"
                            style="padding:8px 16px;background:#C9A84C;color:#000;border:none;border-radius:6px;font-weight:700;cursor:pointer;white-space:nowrap">
                        ✓ Ekle
                    </button>
                </div>
                <div id="staffAddError" style="color:#e05555;font-size:12px;margin-top:8px;display:none"></div>
            </div>
            <!-- Staff table -->
            <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;overflow:hidden">
                <table style="width:100%;border-collapse:collapse" id="staffTable">
                    <thead>
                        <tr style="background:#222">
                            <th style="padding:12px 16px;text-align:left;font-size:12px;color:#888;font-weight:600">AD SOYAD</th>
                            <th style="padding:12px 16px;text-align:left;font-size:12px;color:#888;font-weight:600">KULLANICI ADI</th>
                            <th style="padding:12px 16px;text-align:left;font-size:12px;color:#888;font-weight:600">ROL</th>
                            <th style="padding:12px 16px;text-align:left;font-size:12px;color:#888;font-weight:600">OLUŞTURULMA</th>
                            <th style="padding:12px 16px;text-align:right;font-size:12px;color:#888;font-weight:600">İŞLEMLER</th>
                        </tr>
                    </thead>
                    <tbody id="staffBody">
                        <tr><td colspan="5" style="padding:24px;text-align:center;color:#555">Yükleniyor...</td></tr>
                    </tbody>
                </table>
            </div>
            <!-- Staff login link -->
            <div style="margin-top:16px;font-size:13px;color:#666">
                👤 Personel giriş sayfası:
                <span id="staffLoginLink" style="color:#C9A84C"></span>
            </div>
        </div>

        <!-- STAFF CHAT VIEW -->
        <div id="staffChatView" style="display:none">
            <div class="page-header" style="margin-bottom:16px">
                <div>
                    <div class="page-title" id="scPageTitle">💬 Staff Chat</div>
                    <div class="page-sub" id="scPageSub">Internal chat — staff only</div>
                </div>
            </div>

            <!-- Channel selector -->
            <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap">
                <button class="filter active" id="scTabGeneral"   onclick="switchScChannel('general')">🏠 Общий</button>
                <button class="filter"        id="scTabReception" onclick="switchScChannel('reception')">🛎️ Рецепция</button>
                <button class="filter"        id="scTabHousekeeping" onclick="switchScChannel('housekeeping')">🧹 Горничная</button>
                <button class="filter"        id="scTabMaintenance"  onclick="switchScChannel('maintenance')">🔧 Техника</button>
            </div>

            <!-- Chat box -->
            <div style="background:var(--bg2);border:1px solid var(--border);border-radius:16px;display:flex;flex-direction:column;height:520px;overflow:hidden">
                <!-- Messages -->
                <div id="scMessages" style="flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px">
                    <div style="text-align:center;color:var(--text3);font-size:13px;padding:40px 0">Загрузка...</div>
                </div>
                <!-- Input -->
                <div style="border-top:1px solid var(--border);padding:12px 16px;display:flex;gap:10px;flex-shrink:0;background:var(--bg2)">
                    <input type="text" id="scInput" placeholder="Сообщение для команды..."
                           style="flex:1;background:var(--bg);border:1px solid var(--border);border-radius:20px;padding:10px 16px;color:var(--text);font-size:13px;outline:none;font-family:inherit"
                           onkeypress="if(event.key==='Enter')scSend()">
                    <button class="btn btn-gold" onclick="scSend()" style="border-radius:20px;padding:9px 20px">➤</button>
                </div>
            </div>
        </div>

        <!-- ANALYTICS VIEW -->
        <div id="analyticsView" style="display:none">
            <div class="page-header" style="margin-bottom:20px">
                <div>
                    <div class="page-title" id="analyticsPageTitle">📊 Analytics</div>
                    <div class="page-sub" id="analyticsPageSub">Hotel performance summary</div>
                </div>
                <div class="header-btns">
                    <button class="btn btn-gold btn-sm" onclick="loadAnalytics()">↻ Yenile</button>
                </div>
            </div>

            <!-- Summary cards -->
            <div class="analytics-grid" id="anCards">
                <div class="an-card"><div class="an-num" id="anAvgRating">—</div><div class="an-label">Ort. Puan</div><div class="an-sub" id="anRatingCount"></div></div>
                <div class="an-card"><div class="an-num" id="anTotalGuests">—</div><div class="an-label">Toplam Misafir</div><div class="an-sub" id="anActiveGuests"></div></div>
                <div class="an-card"><div class="an-num" id="anAvgStay">—</div><div class="an-label">Ort. Konaklama</div><div class="an-sub">gün</div></div>
                <div class="an-card"><div class="an-num" id="anCheckedOut">—</div><div class="an-label">Check-out Yapılan</div><div class="an-sub" id="anCheckedIn"></div></div>
            </div>

            <div class="an-two">
                <!-- Rating distribution -->
                <div class="an-section">
                    <div class="an-title">⭐ Puan Dağılımı</div>
                    <div id="anDist">
                        <div style="color:var(--text3);font-size:13px;text-align:center;padding:20px 0">Veri yok</div>
                    </div>
                </div>

                <!-- Nationality breakdown -->
                <div class="an-section">
                    <div class="an-title">🌍 Misafir Uyruğu (İlk 5)</div>
                    <div id="anNat">
                        <div style="color:var(--text3);font-size:13px;text-align:center;padding:20px 0">Veri yok</div>
                    </div>
                </div>
            </div>

            <!-- Rating trend -->
            <div class="an-section">
                <div class="an-title">📈 Son 7 Gün — Puan Trendi</div>
                <div class="trend-wrap" id="anTrend">
                    <div style="color:var(--text3);font-size:13px;padding:20px 0">Veri yok</div>
                </div>
            </div>
        </div>

        <!-- RATINGS VIEW -->
        <div id="ratingsView" style="display:none">
            <div class="page-header" style="margin-bottom:20px">
                <div>
                    <div class="page-title" id="ratingsPageTitle">⭐ Ratings</div>
                    <div class="page-sub" id="ratingsPageSub">Guest scores and comments</div>
                </div>
                <div class="header-btns">
                    <button class="btn btn-gold btn-sm" onclick="loadRatings()">↻ Yenile</button>
                </div>
            </div>
            <div class="rating-avg-card" id="ratingAvgCard" style="display:none">
                <div class="rating-avg-num" id="ratingAvgNum">—</div>
                <div class="rating-avg-stars" id="ratingAvgStars"></div>
                <div class="rating-avg-sub" id="ratingAvgSub">toplam değerlendirme</div>
            </div>
            <div id="ratingsList" style="display:flex;flex-direction:column;gap:10px">
                <div class="guests-empty">Yükleniyor...</div>
            </div>
        </div>

        <!-- ROOMS VIEW -->
        <div id="roomsView" style="display:none">
            <div class="filter-bar">
                <input class="search-input" id="roomSearchGroup" placeholder="🔍 Oda ara..." oninput="renderRoomsView()" style="width:200px">
            </div>
            <div id="roomsGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px"></div>
        </div>
    </div>

    <!-- CONVERSATION MODAL -->
    <div class="modal-overlay" id="modalOverlay" onclick="closeModal(event)">
        <div class="modal" style="display:flex;flex-direction:column;max-height:90vh">
            <div class="modal-header">
                <div class="modal-title" id="modalTitle">🚪 Oda 101</div>
                <div style="display:flex;gap:8px;align-items:center">
                    <button class="btn btn-outline btn-sm" id="notesToggle" onclick="toggleNotes()" style="font-size:12px">📝 Notlar</button>
                    <button class="modal-close" onclick="closeModalDirect()">✕</button>
                </div>
            </div>

            <!-- Staff notes panel (collapsible) -->
            <div id="notesPanel" style="display:none;border-bottom:1px solid var(--border);padding:12px 20px;background:rgba(201,168,76,0.04)">
                <div style="font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px">📝 Персонал нотлари (мезмонга кўринмайди)</div>
                <div id="notesList" style="display:flex;flex-direction:column;gap:6px;max-height:140px;overflow-y:auto;margin-bottom:8px"></div>
                <div style="display:flex;gap:8px">
                    <input id="noteInput" type="text" placeholder="Yangi not ekle..."
                        style="flex:1;background:var(--bg2);border:1px solid var(--border);border-radius:8px;padding:7px 12px;color:var(--text);font-family:inherit;font-size:13px;outline:none"
                        onkeypress="if(event.key==='Enter')addNote()"
                        onfocus="this.style.borderColor='var(--gold)'" onblur="this.style.borderColor='var(--border)'">
                    <button class="btn btn-gold btn-sm" onclick="addNote()">+ Ekle</button>
                </div>
            </div>

            <div class="modal-body" id="modalBody" style="flex:1;overflow-y:auto"></div>
            <div class="modal-footer" id="modalFooter" style="display:none">
                <textarea class="reply-input" id="replyInput" placeholder="Misafire yanıt yaz..." rows="1"
                    onkeypress="if(event.key==='Enter'&&!event.shiftKey){{event.preventDefault();sendReply();}}"></textarea>
                <button class="reply-btn" onclick="sendReply()">Gönder ➤</button>
            </div>
        </div>
    </div>

    <script>
        let allData = [];
        let currentFilter = 'all';
        let lastUrgentCount = 0;
        let currentPage = 1;
        const PAGE_SIZE = 30;
        let openRoom = null;
        const slug = window.location.pathname.split('/')[2] || '';
        const apiBase = slug ? '/api/hotel/' + slug : '';
        const apiUrl = slug ? apiBase + '/messages' : '/api/messages';
        const markReadUrl = slug ? apiBase + '/mark-read' : '/api/mark-read';

        // Translation cache: key = msgId_lang, value = translated string
        const _translCache = {{}};

        function esc(text) {{
            const d = document.createElement('div');
            d.appendChild(document.createTextNode(String(text)));
            return d.innerHTML;
        }}

        function apiJson(url, opts) {{
            return fetch(url, Object.assign({{ credentials: 'same-origin' }}, opts || {{}}))
                .then(res => res.ok ? res.json() : res.json().then(err => {{ throw new Error(err.error || 'API error'); }}));
        }}

        function handleDashboardError(err) {{
            console.error(err);
            if (err && err.message && err.message.toLowerCase().includes('unauthorized') && slug) {{
                window.location.href = '/hotel/' + slug + '/login';
                return;
            }}
            document.getElementById('tbody').innerHTML = '<tr><td colspan="6"><div class="empty-state"><div class="icon">⚠️</div><p>Veri yüklenemedi</p></div></td></tr>';
        }}

        // ===== DATA =====
        function loadData() {{
            apiJson(apiUrl).then(data => {{
                allData = data;
                updateStats(data);
                applyFilters();
                checkUrgentSound(data);
            }}).catch(handleDashboardError);
        }}

        let _baseTitle = document.title;
        let _lastUnreadCount = 0;

        function updateStats(data) {{
            const urgent = data.filter(m => m.priority === 'urgent').length;
            const rooms = new Set(data.map(m => m.room)).size;
            const unread = data.filter(m => m.is_read === 0 && m.role === 'user').length;
            document.getElementById('statTotal').textContent = data.length;
            document.getElementById('statUrgent').textContent = urgent;
            document.getElementById('statRooms').textContent = rooms;
            document.getElementById('statUnread').textContent = unread;
            document.getElementById('unreadBadge').innerHTML = unread > 0
                ? `<span style="background:#E05555;color:white;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:600">${{unread}} yeni</span>`
                : '';

            // ── Tab title badge ─────────────────────────────────────────
            document.title = unread > 0
                ? `(${{unread}}) ${{_baseTitle}}`
                : _baseTitle;

            // ── Notify on new non-urgent messages ───────────────────────
            if (unread > _lastUnreadCount) {{
                const newMsgs = data.filter(m => m.is_read === 0 && m.role === 'user' && m.priority !== 'urgent');
                if (newMsgs.length && newMsgs.length > (data.filter(m => m.is_read === 0 && m.role === 'user' && m.priority !== 'urgent' && m.priority !== 'normal').length)) {{
                    // subtle ping for non-urgent new message
                    playPing();
                }}
                // show browser notification for new normal messages if window not focused
                if (!document.hasFocus() && unread > _lastUnreadCount) {{
                    const newestUnread = data.find(m => m.is_read === 0 && m.role === 'user' && m.priority !== 'urgent');
                    if (newestUnread) sendPushNotification(newestUnread, false);
                }}
            }}
            _lastUnreadCount = unread;
        }}

        let _audioCtx = null;
        function _getAudioCtx() {{
            if (!_audioCtx) _audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (_audioCtx.state === 'suspended') _audioCtx.resume();
            return _audioCtx;
        }}
        document.addEventListener('click', () => {{ if (_audioCtx && _audioCtx.state === 'suspended') _audioCtx.resume(); }}, {{once:false}});

        function playPing() {{
            try {{
                const ctx = _getAudioCtx();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.connect(gain); gain.connect(ctx.destination);
                osc.frequency.value = 660; osc.type = 'sine';
                gain.gain.setValueAtTime(0.15, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25);
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 0.25);
            }} catch(e) {{}}
        }}

        // ===== FILTERS + PAGINATION =====
        function setFilter(filter, btn) {{
            currentFilter = filter;
            currentPage = 1;
            document.querySelectorAll('.filter').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            if (btn) btn.classList.add('active');
            showMessagesView();
            applyFilters();
        }}

        function applyFilters() {{
            const q = (document.getElementById('roomSearch').value || '').toLowerCase().trim();
            let data = allData;
            if (currentFilter === 'urgent') data = data.filter(m => m.priority === 'urgent');
            else if (currentFilter !== 'all') data = data.filter(m => m.role === currentFilter);
            if (q) data = data.filter(m => String(m.room).toLowerCase().includes(q));
            renderTable(data);
        }}

        function renderTable(data) {{
            const tbody = document.getElementById('tbody');
            const total = data.length;
            const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));
            if (currentPage > totalPages) currentPage = 1;
            const start = (currentPage - 1) * PAGE_SIZE;
            const page = data.slice(start, start + PAGE_SIZE);

            if (total === 0) {{
                tbody.innerHTML = `<tr><td colspan="6"><div class="empty-state"><div class="icon">💬</div><p>Henüz mesaj yok</p></div></td></tr>`;
                document.getElementById('pagination').innerHTML = '';
                return;
            }}

            tbody.innerHTML = '';
            page.forEach(m => {{
                const cacheKey = (m.created_at || '') + '|' + (m.room || '') + '|' + (m.message || '').slice(0, 20);
                const tr = document.createElement('tr');
                tr.className = (m.priority === 'urgent' ? 'urgent-row ' : '') + (slug ? 'clickable' : '');
                tr.dataset.msgkey = cacheKey;
                const L = DASH_I18N[_dashLang] || DASH_I18N.en;
                const roleLabel = m.role === 'user'
                    ? `<span class="badge badge-user">👤 ${{L.fUserLbl || 'Guest'}}</span>`
                    : m.role === 'staff'
                        ? `<span class="badge badge-staff">👨‍💼 ${{L.nt_staff || 'Staff'}}</span>`
                        : '<span class="badge badge-bot">🤖 AI</span>';
                const priorityBadge = m.priority === 'urgent'
                    ? `<span class="badge badge-urgent">🔴 ${{L.fUrgentLbl || 'Urgent'}}</span>`
                    : `<span class="badge badge-normal">🟢 Normal</span>`;
                tr.innerHTML = `
                    <td>${{priorityBadge}}</td>
                    <td><span class="room-tag">🚪 ${{esc(m.room)}}</span></td>
                    <td class="hide-mobile">${{roleLabel}}</td>
                    <td>
                        <div class="msg-preview"></div>
                        <div class="msg-translated" style="display:none;font-size:12px;color:var(--gold);margin-top:4px;font-style:italic"></div>
                    </td>
                    <td class="hide-mobile" style="color:var(--text3);font-size:12px;white-space:nowrap">${{esc(m.created_at)}}</td>
                    <td style="white-space:nowrap;display:flex;gap:4px;align-items:center">
                        <button class="btn btn-dark btn-sm translate-btn" title="Translate" onclick="translateMsg(event, this)" style="padding:5px 8px;font-size:13px">🌐</button>
                        ${{slug ? '<button class="btn btn-dark btn-sm" onclick="openConversation(event,\\'' + esc(m.room) + '\\')">💬</button>' : ''}}
                    </td>
                `;
                tr.querySelector('.msg-preview').textContent = m.message;
                // Restore cached translation if exists
                const cached = _translCache[cacheKey + '|' + _dashLang];
                if (cached) {{
                    const tDiv = tr.querySelector('.msg-translated');
                    tDiv.textContent = '→ ' + cached;
                    tDiv.style.display = 'block';
                    tr.querySelector('.translate-btn').style.color = 'var(--gold)';
                }}
                if (slug) tr.onclick = (e) => {{
                    if (e.target.tagName === 'BUTTON') return;
                    openConversation(e, m.room);
                }};
                tbody.appendChild(tr);
            }});

            // Pagination
            const pag = document.getElementById('pagination');
            if (totalPages <= 1) {{ pag.innerHTML = ''; return; }}
            pag.innerHTML = '';
            const addBtn = (label, page, active) => {{
                const b = document.createElement('button');
                b.className = 'page-btn' + (active ? ' active' : '');
                b.textContent = label;
                b.onclick = () => {{ currentPage = page; applyFilters(); }};
                pag.appendChild(b);
            }};
            if (currentPage > 1) addBtn('← Önceki', currentPage - 1, false);
            for (let i = Math.max(1, currentPage-2); i <= Math.min(totalPages, currentPage+2); i++) addBtn(i, i, i===currentPage);
            if (currentPage < totalPages) addBtn('Sonraki →', currentPage + 1, false);
        }}

        // ===== VIEW HELPERS =====
        function hideAllViews() {{
            // Stop staff chat polling when navigating away
            _scActive = false;
            if (typeof _scPollTimer !== 'undefined' && _scPollTimer) {{
                clearInterval(_scPollTimer); _scPollTimer = null;
            }}
            closeMobNav();
            ['messagesView','roomsView','guestsView','ratingsView','analyticsView','requestsView','calendarView','staffView','servicesView','staffChatView'].forEach(id => {{
                const el = document.getElementById(id);
                if (el) el.style.display = 'none';
            }});
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        }}

        function toggleMobNav() {{
            const sb = document.getElementById('sidebar');
            const ov = document.getElementById('mobOverlay');
            if (!sb) return;
            const isOpen = sb.classList.contains('mob-open');
            if (isOpen) {{
                sb.classList.remove('mob-open');
                if (ov) ov.classList.remove('open');
            }} else {{
                sb.classList.add('mob-open');
                if (ov) ov.classList.add('open');
            }}
        }}

        function closeMobNav() {{
            const sb = document.getElementById('sidebar');
            const ov = document.getElementById('mobOverlay');
            if (sb) sb.classList.remove('mob-open');
            if (ov) ov.classList.remove('open');
        }}

        // ===== ANALYTICS VIEW =====
        function showAnalyticsView() {{
            hideAllViews();
            document.getElementById('analyticsView').style.display = 'block';
            document.getElementById('navAnalytics').classList.add('active');
            loadAnalytics();
        }}

        async function loadAnalytics() {{
            if (!slug) return;
            try {{
                const d = await apiJson(apiBase + '/stats');

                // Summary cards
                document.getElementById('anAvgRating').textContent =
                    d.avg_rating ? d.avg_rating + ' ★' : '—';
                document.getElementById('anRatingCount').textContent =
                    (d.rating_count || 0) + ' değerlendirme';
                document.getElementById('anTotalGuests').textContent = d.guests?.total ?? '—';
                document.getElementById('anActiveGuests').textContent =
                    (d.guests?.checked_in ?? 0) + ' aktif';
                document.getElementById('anAvgStay').textContent =
                    d.guests?.avg_stay_days != null ? d.guests.avg_stay_days : '—';
                document.getElementById('anCheckedOut').textContent = d.guests?.checked_out ?? '—';
                document.getElementById('anCheckedIn').textContent =
                    (d.guests?.checked_in ?? 0) + ' içeride';

                // Rating distribution
                const distEl = document.getElementById('anDist');
                const dist = d.rating_dist || {{}};
                const maxDist = Math.max(...Object.values(dist), 1);
                const totalRatings = Object.values(dist).reduce((a, b) => a + b, 0);
                if (totalRatings === 0) {{
                    distEl.innerHTML = '<div style="color:var(--text3);font-size:13px;text-align:center;padding:20px 0">Henüz değerlendirme yok</div>';
                }} else {{
                    distEl.innerHTML = [5, 4, 3, 2, 1].map(star => {{
                        const cnt = dist[star] || 0;
                        const pct = Math.round((cnt / maxDist) * 100);
                        const cls = star >= 4 ? '' : star === 3 ? ' mid' : ' low';
                        return `<div class="dist-row">
                            <div class="dist-star">${{'★'.repeat(star)}}</div>
                            <div class="dist-track"><div class="dist-fill${{cls}}" style="width:${{pct}}%"></div></div>
                            <div class="dist-count">${{cnt}}</div>
                        </div>`;
                    }}).join('');
                }}

                // Rating trend
                const trendEl = document.getElementById('anTrend');
                if (!d.rating_trend || !d.rating_trend.length) {{
                    trendEl.innerHTML = '<div style="color:var(--text3);font-size:13px;padding:20px 0">Son 7 günde veri yok</div>';
                }} else {{
                    const maxAvg = 5;
                    trendEl.innerHTML = d.rating_trend.map(t => {{
                        const h = Math.max(Math.round((t.avg / maxAvg) * 70), 4);
                        const color = t.avg >= 4 ? '#C9A84C' : t.avg >= 3 ? '#E8A040' : '#E05555';
                        return `<div class="trend-bar">
                            <div class="trend-fill" style="height:${{h}}px;background:${{color}}" data-tip="${{t.avg}}★ (${{t.count}} yorum)"></div>
                            <div class="trend-label">${{t.day.slice(5)}}</div>
                        </div>`;
                    }}).join('');
                }}

                // Nationalities
                const natEl = document.getElementById('anNat');
                if (!d.nationalities || !d.nationalities.length) {{
                    natEl.innerHTML = '<div style="color:var(--text3);font-size:13px;text-align:center;padding:20px 0">Veri yok</div>';
                }} else {{
                    const maxNat = d.nationalities[0]?.count || 1;
                    natEl.innerHTML = d.nationalities.map(n => {{
                        const pct = Math.round((n.count / maxNat) * 100);
                        return `<div class="nat-row">
                            <div class="nat-name">${{esc(n.name)}}</div>
                            <div class="nat-track"><div class="nat-fill" style="width:${{pct}}%"></div></div>
                            <div class="nat-count">${{n.count}}</div>
                        </div>`;
                    }}).join('');
                }}
            }} catch(e) {{
                console.error('Analytics load error', e);
            }}
        }}

        // ===== ROOMS VIEW =====
        async function showRoomsView() {{
            hideAllViews();
            document.getElementById('roomsView').style.display = 'block';
            document.getElementById('navRooms').classList.add('active');
            // Ensure guest data is fresh so room cards show guest names
            if (slug && !allGuests.length) {{
                try {{ allGuests = await apiJson(apiBase + '/guests'); }} catch(e) {{}}
            }}
            renderRoomsView();
        }}
        function showMessagesView() {{
            ['roomsView','guestsView','ratingsView','analyticsView','requestsView',
             'calendarView','staffView','servicesView','staffChatView'].forEach(id => {{
                const el = document.getElementById(id);
                if (el) el.style.display = 'none';
            }});
            document.getElementById('messagesView').style.display = 'block';
        }}

        // ===== GUESTS VIEW =====
        function showGuestsView() {{
            hideAllViews();
            document.getElementById('guestsView').style.display = 'block';
            document.getElementById('navGuests').classList.add('active');
            loadGuests();
        }}

        // ===== REQUESTS VIEW =====
        function showRequestsView() {{
            hideAllViews();
            document.getElementById('requestsView').style.display = 'block';
            document.getElementById('navRequests').classList.add('active');
            loadRequests();
        }}

        const REQ_CAT_LABEL = {{
            room_service: '🍽 Oda Servisi',
            maintenance:  '🔧 Bakım',
            housekeeping: '🧹 Temizlik',
            general:      '📌 Genel',
        }};
        const REQ_STATUS_LABEL = {{
            pending:     '⏳ Bekliyor',
            in_progress: '🔄 İşlemde',
            resolved:    '✅ Çözüldü',
        }};
        const REQ_NEXT_STATUS = {{
            pending:     'in_progress',
            in_progress: 'resolved',
            resolved:    'pending',
        }};

        async function loadRequests() {{
            if (!slug) return;
            const statusFilter = document.getElementById('reqStatusFilter').value;
            const url = apiBase + '/requests' + (statusFilter ? '?status=' + statusFilter : '');
            try {{
                const data = await apiJson(url);
                const tbody = document.getElementById('requestsList');
                updateRequestsBadge(data.pending_count || 0);

                if (!data.requests || !data.requests.length) {{
                    tbody.innerHTML = '<tr><td colspan="7" class="req-empty">📭 Talep yok</td></tr>';
                    return;
                }}

                tbody.innerHTML = data.requests.map(r => {{
                    const catLabel = REQ_CAT_LABEL[r.category] || r.category;
                    const catClass = 'req-cat req-cat-' + r.category;
                    const stLabel  = REQ_STATUS_LABEL[r.status] || r.status;
                    const stClass  = 'req-status req-status-' + r.status;
                    const nextSt   = REQ_NEXT_STATUS[r.status];
                    const time = r.created_at ? r.created_at.slice(5,16) : '';
                    return `<tr>
                        <td><b>${{r.room}}</b></td>
                        <td class="hide-mobile" style="color:var(--text2)">${{esc(r.guest_name || '—')}}</td>
                        <td class="hide-mobile"><span class="${{catClass}}">${{catLabel}}</span></td>
                        <td><div class="req-msg" title="${{esc(r.message)}}">${{esc(r.message)}}</div></td>
                        <td>
                            <button class="${{stClass}}" onclick="advanceRequest(${{r.id}}, '${{nextSt}}')" title="Tıkla: sonraki duruma geç">
                                ${{stLabel}}
                            </button>
                        </td>
                        <td class="hide-mobile" style="color:var(--text3);font-size:12px">${{time}}</td>
                        <td><button class="req-del" onclick="removeRequest(${{r.id}})" title="Sil">✕</button></td>
                    </tr>`;
                }}).join('');
            }} catch(e) {{
                document.getElementById('requestsList').innerHTML =
                    '<tr><td colspan="7" class="req-empty">Yüklenemedi</td></tr>';
            }}
        }}

        async function advanceRequest(id, nextStatus) {{
            try {{
                const data = await fetch(apiBase + '/requests/' + id, {{
                    method: 'PATCH',
                    headers: {{'Content-Type':'application/json'}},
                    body: JSON.stringify({{status: nextStatus}})
                }}).then(r => r.json());
                updateRequestsBadge(data.pending_count || 0);
                loadRequests();
            }} catch(e) {{}}
        }}

        async function removeRequest(id) {{
            if (!confirm('Bu talebi silmek istiyor musunuz?')) return;
            try {{
                await fetch(apiBase + '/requests/' + id, {{method: 'DELETE'}});
                loadRequests();
            }} catch(e) {{}}
        }}

        function updateRequestsBadge(count) {{
            const badge = document.getElementById('requestsBadge');
            if (count > 0) {{
                badge.textContent = count;
                badge.style.display = 'inline';
            }} else {{
                badge.style.display = 'none';
            }}
        }}

        async function loadRequestsBadge() {{
            if (!slug) return;
            try {{
                const data = await apiJson(apiBase + '/requests?status=pending');
                updateRequestsBadge(data.pending_count || 0);
            }} catch(e) {{}}
        }}

        // ===== MANUAL REQUEST MODAL =====
        function openReqModal() {{
            document.getElementById('reqRoom').value = '';
            document.getElementById('reqGuest').value = '';
            document.getElementById('reqMsg').value = '';
            document.getElementById('reqCat').value = 'general';
            document.getElementById('reqModalOverlay').classList.add('open');
            document.getElementById('reqRoom').focus();
        }}
        function closeReqModal() {{
            document.getElementById('reqModalOverlay').classList.remove('open');
        }}
        async function submitManualRequest() {{
            const room    = document.getElementById('reqRoom').value.trim();
            const guest   = document.getElementById('reqGuest').value.trim();
            const cat     = document.getElementById('reqCat').value;
            const message = document.getElementById('reqMsg').value.trim();
            if (!room || !message) {{ alert('Oda ve talep detayı gerekli'); return; }}
            try {{
                const data = await apiJson(apiBase + '/requests', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{room, guest_name: guest, category: cat, message}})
                }});
                if (data.ok) {{
                    closeReqModal();
                    updateRequestsBadge(data.pending_count || 0);
                    loadRequests();
                }}
            }} catch(e) {{ alert('Hata oluştu'); }}
        }}
        document.addEventListener('keydown', e => {{
            if (e.key === 'Escape') closeReqModal();
        }});

        // ===== CALENDAR VIEW =====
        function showCalendarView() {{
            hideAllViews();
            document.getElementById('calendarView').style.display = 'block';
            document.getElementById('navCalendar').classList.add('active');
            loadCalendar();
        }}

        async function loadCalendar() {{
            if (!slug) return;
            const grid = document.getElementById('calendarGrid');
            grid.innerHTML = '<div style="text-align:center;padding:60px;color:var(--text3)">Yükleniyor…</div>';
            try {{
                const guests = await apiJson(apiBase + '/guests');
                renderCalendar(guests);
            }} catch(e) {{
                grid.innerHTML = '<div style="text-align:center;padding:60px;color:#e05555">Yüklenemedi</div>';
            }}
        }}

        function renderCalendar(guests) {{
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const DAYS_BACK = 7, DAYS_AHEAD = 21;
            const totalDays = DAYS_BACK + DAYS_AHEAD + 1;

            // Build date range
            const dates = [];
            for (let i = -DAYS_BACK; i <= DAYS_AHEAD; i++) {{
                const d = new Date(today);
                d.setDate(today.getDate() + i);
                dates.push(d);
            }}

            // Collect rooms from checked_in / checked_out guests
            const rooms = [...new Set(guests
                .filter(g => g.room && ['checked_in','checked_out','pending'].includes(g.status))
                .map(g => g.room)
            )].sort((a, b) => a.localeCompare(b, undefined, {{numeric: true}}));

            if (!rooms.length) {{
                document.getElementById('calendarGrid').innerHTML =
                    '<div style="text-align:center;padding:60px;color:var(--text3)">📭 Henüz misafir kaydı yok</div>';
                return;
            }}

            // Build table
            const fmtDay = d => String(d.getDate()).padStart(2, '0');
            const fmtMon = d => ['Oca','Şub','Mar','Nis','May','Haz','Tem','Ağu','Eyl','Eki','Kas','Ara'][d.getMonth()];
            const fmtDate = d => d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');

            let html = '<table class="cal-table"><thead><tr>';
            html += '<th class="cal-room" style="min-width:80px">Oda</th>';
            dates.forEach(d => {{
                const isToday = d.getTime() === today.getTime();
                html += `<th class="${{isToday ? 'cal-today-head' : ''}}" style="min-width:46px">
                    <div>${{fmtMon(d)}}</div>
                    <div style="font-size:14px;font-weight:800">${{fmtDay(d)}}</div>
                </th>`;
            }});
            html += '</tr></thead><tbody>';

            rooms.forEach(room => {{
                html += `<tr><td class="cal-room">${{esc(room)}}</td>`;
                dates.forEach(d => {{
                    const ds = fmtDate(d);
                    const isToday = d.getTime() === today.getTime();
                    // Find guest staying this day
                    const g = guests.find(g => g.room === room &&
                        ['checked_in','checked_out'].includes(g.status) &&
                        g.check_in <= ds && g.check_out >= ds);
                    let cellClass = 'cal-vacant';
                    let label = '';
                    let tip = '';
                    if (g) {{
                        const isCI = g.check_in === ds;
                        const isCO = g.check_out === ds;
                        cellClass = isCI ? 'cal-checkin' : isCO ? 'cal-checkout' : 'cal-occupied';
                        label = isCI ? 'GİR' : isCO ? 'ÇIK' : '●';
                        tip = `${{g.first_name}} ${{g.last_name}} (${{g.check_in}} – ${{g.check_out}})`;
                    }}
                    const todayCls = isToday ? ' cal-today-col' : '';
                    html += `<td class="${{todayCls}}"><div class="cal-cell ${{cellClass}}"
                        ${{tip ? `onmouseenter="showCalTip(event,'${{tip.replace(/'/g,'')}}',event)"
                                  onmouseleave="hideCalTip()"` : ''}}>
                        ${{label}}
                    </div></td>`;
                }});
                html += '</tr>';
            }});

            html += '</tbody></table>';
            document.getElementById('calendarGrid').innerHTML = html;

            // Scroll to today column
            const wrap = document.querySelector('.cal-wrap');
            if (wrap) {{
                const todayIdx = DAYS_BACK;
                const cellW = 46;
                wrap.scrollLeft = Math.max(0, todayIdx * cellW - wrap.clientWidth / 2 + cellW / 2);
            }}
        }}

        function showCalTip(event, text) {{
            const tip = document.getElementById('calTooltip');
            tip.textContent = text;
            tip.style.display = 'block';
            tip.style.left = (event.clientX + 12) + 'px';
            tip.style.top  = (event.clientY - 36) + 'px';
        }}
        function hideCalTip() {{
            document.getElementById('calTooltip').style.display = 'none';
        }}

        // ===== SERVICES VIEW =====
        function _svcCatLabel(cat) {{
            const L = DASH_I18N[_dashLang] || DASH_I18N.en;
            const map = {{
                food: L.svcCatFood, housekeeping: L.svcCatHousekeeping,
                spa: L.svcCatSpa, transport: L.svcCatTransport,
                maintenance: L.svcCatMaintenance, general: L.svcCatGeneral
            }};
            return map[cat] || cat;
        }}

        function showServicesView() {{
            hideAllViews();
            document.getElementById('servicesView').style.display = 'block';
            document.getElementById('navServices').classList.add('active');
            loadSvcList();
        }}

        let _allSvcs = [];

        function editSvcById(id) {{
            const s = _allSvcs.find(x => x.id === id);
            if (s) editSvc(s);
        }}

        async function loadSvcList() {{
            const L = DASH_I18N[_dashLang] || DASH_I18N.en;
            const grid = document.getElementById('svcGrid');
            grid.innerHTML = '<div style="color:var(--text2);font-size:14px;padding:20px">' + L.svcLoading + '</div>';
            try {{
                const res = await fetch('/api/hotel/' + slug + '/services', {{credentials:'include'}});
                const svcs = await res.json();
                _allSvcs = svcs;
                if (!svcs.length) {{
                    grid.innerHTML = '<div style="color:var(--text2);font-size:14px;padding:20px;grid-column:1/-1">' + L.svcEmpty + '</div>';
                    return;
                }}
                grid.innerHTML = svcs.map(s => `
                    <div style="background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:18px;position:relative">
                        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
                            <span style="font-size:24px">${{s.icon}}</span>
                            <label style="display:flex;align-items:center;gap:6px;cursor:pointer;font-size:12px;color:var(--text2)">
                                <input type="checkbox" ${{s.is_active?'checked':''}} onchange="toggleSvc(${{s.id}},this)"
                                       style="accent-color:#C9A84C;width:14px;height:14px">
                                ${{L.svcActive}}
                            </label>
                        </div>
                        <div style="font-size:14px;font-weight:700;margin-bottom:4px">${{s.name}}</div>
                        <div style="font-size:11px;color:var(--gold);margin-bottom:6px">${{_svcCatLabel(s.category)}}</div>
                        ${{s.description ? '<div style="font-size:12px;color:var(--text2);margin-bottom:8px">'+s.description+'</div>' : ''}}
                        <div style="font-size:13px;font-weight:700;color:${{s.price>0?'var(--gold)':'#4caf50'}}">
                            ${{s.price > 0 ? s.price.toFixed(0)+' '+s.currency : L.svcFree}}
                        </div>
                        <div style="display:flex;gap:8px;margin-top:12px">
                            <button onclick="editSvcById(${{s.id}})"
                                    style="flex:1;padding:7px;background:var(--bg3);border:1px solid var(--border);
                                           border-radius:8px;color:var(--text2);cursor:pointer;font-size:12px">✏️ ${{L.svcEdit}}</button>
                            <button onclick="deleteSvc(${{s.id}})"
                                    style="padding:7px 12px;background:rgba(220,80,80,0.1);border:1px solid rgba(220,80,80,0.25);
                                           border-radius:8px;color:#dc5050;cursor:pointer;font-size:12px">🗑</button>
                        </div>
                    </div>`).join('');
            }} catch(e) {{
                grid.innerHTML = '<div style="color:#dc5050;font-size:14px;padding:20px">' + L.svcError + '</div>';
            }}
        }}

        function openSvcForm() {{
            document.getElementById('svcEditId').value = '';
            document.getElementById('svcFormTitle').textContent = (DASH_I18N[_dashLang]||DASH_I18N.en).svcNewTitle;
            document.getElementById('svcIcon').value = '🛎️';
            document.getElementById('svcName').value = '';
            document.getElementById('svcDesc').value = '';
            document.getElementById('svcPrice').value = '0';
            document.getElementById('svcCategory').value = 'general';
            document.getElementById('svcCurrency').value = 'USD';
            document.getElementById('svcFormBox').style.display = 'block';
            document.getElementById('svcFormMsg').style.display = 'none';
            document.getElementById('svcName').focus();
        }}

        function closeSvcForm() {{
            document.getElementById('svcFormBox').style.display = 'none';
        }}

        function editSvc(s) {{
            document.getElementById('svcEditId').value = s.id;
            document.getElementById('svcFormTitle').textContent = (DASH_I18N[_dashLang]||DASH_I18N.en).svcEditTitle;
            document.getElementById('svcIcon').value = s.icon || '🛎️';
            document.getElementById('svcName').value = s.name || '';
            document.getElementById('svcDesc').value = s.description || '';
            document.getElementById('svcPrice').value = s.price || 0;
            document.getElementById('svcCategory').value = s.category || 'general';
            document.getElementById('svcCurrency').value = s.currency || 'USD';
            document.getElementById('svcFormBox').style.display = 'block';
            document.getElementById('svcFormMsg').style.display = 'none';
            document.getElementById('svcName').focus();
        }}

        async function saveSvc() {{
            const editId = document.getElementById('svcEditId').value;
            const body = {{
                name: document.getElementById('svcName').value.trim(),
                description: document.getElementById('svcDesc').value.trim(),
                category: document.getElementById('svcCategory').value,
                price: parseFloat(document.getElementById('svcPrice').value) || 0,
                currency: document.getElementById('svcCurrency').value,
                icon: document.getElementById('svcIcon').value.trim() || '🛎️',
                is_active: true,
                sort_order: 0
            }};
            if (!body.name) {{
                showSvcMsg('❌ Введите название', '#dc5050');
                return;
            }}
            const url = editId
                ? '/api/hotel/' + slug + '/services/' + editId
                : '/api/hotel/' + slug + '/services';
            const method = editId ? 'PUT' : 'POST';
            try {{
                const res = await fetch(url, {{
                    method, credentials:'include',
                    headers:{{'Content-Type':'application/json'}},
                    body: JSON.stringify(body)
                }});
                const data = await res.json();
                if (data.ok) {{
                    closeSvcForm();
                    loadSvcList();
                }} else {{
                    showSvcMsg('❌ ' + (data.error||'Ошибка'), '#dc5050');
                }}
            }} catch(e) {{ showSvcMsg('❌ Ошибка сети', '#dc5050'); }}
        }}

        async function toggleSvc(id, cb) {{
            try {{
                const res = await fetch('/api/hotel/' + slug + '/services/' + id + '/toggle', {{
                    method:'PATCH', credentials:'include'
                }});
                const data = await res.json();
                if (!data.ok) cb.checked = !cb.checked; // revert on error
            }} catch(e) {{ cb.checked = !cb.checked; }}
        }}

        async function deleteSvc(id) {{
            if (!confirm('Удалить эту услугу?')) return;
            try {{
                const res = await fetch('/api/hotel/' + slug + '/services/' + id, {{
                    method:'DELETE', credentials:'include'
                }});
                const data = await res.json();
                if (data.ok) loadSvcList();
                else alert('Ошибка: ' + (data.error||''));
            }} catch(e) {{ alert('Ошибка сети'); }}
        }}

        function showSvcMsg(text, color) {{
            const el = document.getElementById('svcFormMsg');
            el.textContent = text;
            el.style.color = color;
            el.style.display = 'block';
        }}

        // ===== STAFF VIEW =====
        const _ROLE_LABELS = {{ manager: '👑 Yönetici', receptionist: '🛎️ Resepsiyon', housekeeping: '🧹 Housekeeping' }};
        const _ROLE_COLORS = {{ manager: '#C9A84C', receptionist: '#4a9eff', housekeeping: '#4caf50' }};

        // ===== STAFF CHAT =====
        let _scChannel = 'general';
        let _scLastId  = 0;
        let _scPollTimer = null;
        let _scActive = false;
        let _scMyName = '';

        const SC_CHAN_LABELS = {{
            general: '🏠 Общий', reception: '🛎️ Рецепция',
            housekeeping: '🧹 Горничная', maintenance: '🔧 Техника'
        }};
        const SC_ROLE_COLORS = {{ manager: '#C9A84C', receptionist: '#4a9eff', housekeeping: '#4caf50', maintenance: '#ff9a3c' }};

        function showStaffChatView() {{
            hideAllViews();
            document.getElementById('staffChatView').style.display = 'block';
            document.getElementById('navStaffChat').classList.add('active');
            _scActive = true;
            _scLastId = 0;
            scUpdateBadge(0); // clear badge when opening chat
            loadScHistory();
            clearInterval(_scPollTimer);
            _scPollTimer = setInterval(scPoll, 3000);
        }}

        function switchScChannel(ch) {{
            _scChannel = ch;
            _scLastId  = 0;
            scUpdateBadge(0); // clear badge when switching channels
            // Update tab buttons
            ['general','reception','housekeeping','maintenance'].forEach(c => {{
                const el = document.getElementById('scTab' + c.charAt(0).toUpperCase() + c.slice(1));
                if (el) el.classList.toggle('active', c === ch);
            }});
            loadScHistory();
        }}

        async function loadScHistory() {{
            const box = document.getElementById('scMessages');
            box.innerHTML = '<div style="text-align:center;color:var(--text3);font-size:13px;padding:40px 0">Загрузка...</div>';
            try {{
                const r = await fetch('/api/hotel/' + slug + '/staff-chat/' + _scChannel, {{credentials:'include'}});
                const data = await r.json();
                const msgs = data.messages || [];
                if (!msgs.length) {{
                    box.innerHTML = '<div style="text-align:center;color:var(--text3);font-size:13px;padding:40px 0">Сообщений нет. Будьте первым!</div>';
                    _scLastId = 0;
                    return;
                }}
                _scLastId = msgs[msgs.length - 1].id;
                box.innerHTML = msgs.map(m => scRenderMsg(m)).join('');
                box.scrollTop = box.scrollHeight;
                scMarkChannelSeen(); // mark as read on open
            }} catch(e) {{
                box.innerHTML = '<div style="color:#e05555;padding:20px">Ошибка загрузки</div>';
            }}
        }}

        function scRenderMsg(m) {{
            const isMe = (m.sender === (_scMyName || ''));
            const roleColor = SC_ROLE_COLORS[m.role] || '#888';
            const align = isMe ? 'flex-end' : 'flex-start';
            const bubbleBg = isMe
                ? 'linear-gradient(135deg,#C9A84C,#E8C96A)'
                : 'var(--bg3)';
            const textColor = isMe ? '#1a1a1a' : 'var(--text)';
            return `<div style="display:flex;flex-direction:column;align-items:${{align}};gap:3px">
                <div style="font-size:11px;color:${{roleColor}};font-weight:600;${{isMe?'text-align:right':''}}">${{m.sender}}</div>
                <div style="max-width:72%;background:${{bubbleBg}};color:${{textColor}};padding:9px 14px;border-radius:16px;font-size:13px;line-height:1.5;word-break:break-word">${{escHtml(m.message)}}</div>
                <div style="font-size:10px;color:var(--text3)">${{m.created_at.slice(11,16)}}</div>
            </div>`;
        }}

        function escHtml(s) {{
            return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
        }}

        async function scPoll() {{
            if (!_scActive) return;
            try {{
                const r = await fetch(
                    '/api/hotel/' + slug + '/staff-chat/' + _scChannel + '/poll?since_id=' + _scLastId,
                    {{credentials:'include'}}
                );
                const data = await r.json();
                const msgs = data.messages || [];
                if (!msgs.length) return;
                const box = document.getElementById('scMessages');
                // If box had the "no messages" placeholder — clear it
                if (box.querySelector('div[style*="40px 0"]')) box.innerHTML = '';
                msgs.forEach(m => {{
                    box.insertAdjacentHTML('beforeend', scRenderMsg(m));
                    _scLastId = Math.max(_scLastId, m.id);
                }});
                box.scrollTop = box.scrollHeight;
            }} catch(e) {{}}
        }}

        async function scSend() {{
            const inp = document.getElementById('scInput');
            const text = inp.value.trim();
            if (!text) return;
            inp.value = '';
            inp.disabled = true;
            try {{
                await fetch('/api/hotel/' + slug + '/staff-chat/' + _scChannel, {{
                    method:'POST', credentials:'include',
                    headers:{{'Content-Type':'application/json'}},
                    body: JSON.stringify({{message: text}})
                }});
                // Immediately poll to show the message
                await scPoll();
            }} catch(e) {{}}
            inp.disabled = false;
            inp.focus();
        }}

        // ===== STAFF CHAT — BACKGROUND BADGE POLLING =====

        // Per-channel last-seen IDs (persisted in localStorage)
        const SC_CHANNELS = ['general','reception','housekeeping','maintenance'];
        const SC_LS_KEY = 'sc_seen_' + slug;

        function scLoadSeen() {{
            try {{ return JSON.parse(localStorage.getItem(SC_LS_KEY) || '{{}}'); }}
            catch(e) {{ return {{}}; }}
        }}
        function scSaveSeen(seen) {{
            try {{ localStorage.setItem(SC_LS_KEY, JSON.stringify(seen)); }} catch(e) {{}}
        }}

        let _scBgTimer = null;
        let _scBadgeCount = 0;

        // Tiny beep via Web Audio API (no file needed)
        function scBeep() {{
            try {{
                const ctx = _getAudioCtx();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.connect(gain); gain.connect(ctx.destination);
                osc.frequency.value = 880;
                gain.gain.setValueAtTime(0.08, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25);
                osc.start(); osc.stop(ctx.currentTime + 0.25);
            }} catch(e) {{}}
        }}

        function scUpdateBadge(count) {{
            _scBadgeCount = count;
            const badge = document.getElementById('scBadge');
            if (!badge) return;
            if (count > 0) {{
                badge.textContent = count > 99 ? '99+' : count;
                badge.style.display = 'inline';
            }} else {{
                badge.style.display = 'none';
            }}
        }}

        async function scBgPoll() {{
            if (!slug) return;
            const seen = scLoadSeen();
            let newTotal = 0;
            let gotNew = false;
            for (const ch of SC_CHANNELS) {{
                // Skip the currently-open channel (already polled by the view)
                if (_scActive && ch === _scChannel) continue;
                const lastId = seen[ch] || 0;
                try {{
                    const r = await fetch(
                        '/api/hotel/' + slug + '/staff-chat/' + ch + '/poll?since_id=' + lastId,
                        {{credentials:'include'}}
                    );
                    if (!r.ok) continue;
                    const data = await r.json();
                    const msgs = data.messages || [];
                    if (msgs.length) {{
                        // Only count messages NOT from me
                        const foreign = msgs.filter(m => m.sender !== _scMyName);
                        newTotal += foreign.length;
                        if (foreign.length) gotNew = true;
                        // Advance seen pointer regardless (so we don't double-count)
                        seen[ch] = msgs[msgs.length - 1].id;
                    }}
                }} catch(e) {{}}
            }}
            scSaveSeen(seen);
            if (gotNew) {{
                scBeep();
                // Browser notification if tab is hidden
                if (document.hidden && Notification.permission === 'granted') {{
                    new Notification('💬 Новое сообщение в чате персонала', {{
                        body: 'Откройте вкладку «Чат персонала»',
                        icon: '/hotel/' + slug + '/favicon.ico'
                    }});
                }}
            }}
            // Add to existing unseen badge count
            scUpdateBadge(_scBadgeCount + newTotal);
        }}

        function scStartBgPoll() {{
            if (_scBgTimer) return; // already running
            // Request notification permission once
            if (Notification.permission === 'default') {{
                Notification.requestPermission().catch(() => {{}});
            }}
            // Bootstrap: seed seen IDs with current latest (so we don't flood on first load)
            (async () => {{
                const seen = scLoadSeen();
                for (const ch of SC_CHANNELS) {{
                    if (seen[ch] !== undefined) continue; // already seeded
                    try {{
                        const r = await fetch('/api/hotel/' + slug + '/staff-chat/' + ch, {{credentials:'include'}});
                        if (!r.ok) continue;
                        const data = await r.json();
                        const msgs = data.messages || [];
                        seen[ch] = msgs.length ? msgs[msgs.length - 1].id : 0;
                    }} catch(e) {{}}
                }}
                scSaveSeen(seen);
                // Start the interval after seeding
                _scBgTimer = setInterval(scBgPoll, 6000);
            }})();
        }}

        // Clear badge when entering staff chat and mark current channel as seen
        function scMarkChannelSeen() {{
            const seen = scLoadSeen();
            if (_scLastId > 0) seen[_scChannel] = _scLastId;
            scSaveSeen(seen);
            // Recompute badge: subtract current channel's unseen from badge
            // (simplest: just reset to 0, bg poll will pick up real count next tick)
            scUpdateBadge(0);
        }}

        function showStaffView() {{
            hideAllViews();
            document.getElementById('staffView').style.display = 'block';
            document.getElementById('navStaff').classList.add('active');
            loadStaff();
            const link = document.getElementById('staffLoginLink');
            if (link) link.textContent = window.location.origin + '/hotel/' + slug + '/staff/login';
        }}

        async function loadStaff() {{
            const r = await fetch('/api/hotel/' + slug + '/staff', {{credentials:'include'}});
            if (!r.ok) return;
            const list = await r.json();
            const tbody = document.getElementById('staffBody');
            if (!list.length) {{
                tbody.innerHTML = '<tr><td colspan="5" style="padding:24px;text-align:center;color:#555">Henüz personel eklenmedi</td></tr>';
                return;
            }}
            tbody.innerHTML = list.map(s => `
                <tr style="border-top:1px solid #2a2a2a">
                    <td style="padding:12px 16px;font-weight:600">${{s.name}}</td>
                    <td style="padding:12px 16px;color:#888;font-family:monospace">${{s.username}}</td>
                    <td style="padding:12px 16px">
                        <span style="background:${{_ROLE_COLORS[s.role]}}22;color:${{_ROLE_COLORS[s.role]}};
                                     padding:3px 10px;border-radius:20px;font-size:12px;font-weight:600">
                            ${{_ROLE_LABELS[s.role] || s.role}}
                        </span>
                    </td>
                    <td style="padding:12px 16px;color:#666;font-size:13px">${{s.created_at}}</td>
                    <td style="padding:12px 16px;text-align:right">
                        <button onclick="resetStaffPw(${{s.id}},'${{s.name}}')"
                                style="padding:5px 10px;background:#2a2a2a;border:1px solid #333;color:#aaa;border-radius:6px;cursor:pointer;font-size:12px;margin-right:6px">
                            🔑 Şifre
                        </button>
                        <button onclick="removeStaff(${{s.id}},'${{s.name}}')"
                                style="padding:5px 10px;background:#3a1515;border:1px solid #5a2020;color:#e05555;border-radius:6px;cursor:pointer;font-size:12px">
                            🗑️ Sil
                        </button>
                    </td>
                </tr>`).join('');
        }}

        async function addStaffMember() {{
            const name = document.getElementById('newStaffName').value.trim();
            const username = document.getElementById('newStaffUser').value.trim();
            const password = document.getElementById('newStaffPass').value;
            const role = document.getElementById('newStaffRole').value;
            const errEl = document.getElementById('staffAddError');
            errEl.style.display = 'none';
            if (!name || !username || !password) {{ errEl.textContent = 'Tüm alanları doldurun'; errEl.style.display='block'; return; }}
            const r = await fetch('/api/hotel/' + slug + '/staff', {{
                method: 'POST', credentials: 'include',
                headers: {{'Content-Type':'application/json'}},
                body: JSON.stringify({{name, username, password, role}})
            }});
            const d = await r.json();
            if (d.ok) {{
                document.getElementById('newStaffName').value = '';
                document.getElementById('newStaffUser').value = '';
                document.getElementById('newStaffPass').value = '';
                loadStaff();
            }} else {{
                errEl.textContent = '❌ ' + (d.error || 'Hata');
                errEl.style.display = 'block';
            }}
        }}

        async function removeStaff(id, name) {{
            if (!confirm(`"${{name}}" adlı personeli silmek istediğinize emin misiniz?`)) return;
            const r = await fetch('/api/hotel/' + slug + '/staff/' + id, {{method:'DELETE', credentials:'include'}});
            const d = await r.json();
            if (d.ok) loadStaff();
            else alert('❌ ' + (d.error || 'Silinemedi'));
        }}

        async function resetStaffPw(id, name) {{
            const pw = prompt(`"${{name}}" için yeni şifre (min. 6 karakter):`);
            if (!pw) return;
            const r = await fetch('/api/hotel/' + slug + '/staff/' + id + '/password', {{
                method: 'PATCH', credentials: 'include',
                headers: {{'Content-Type':'application/json'}},
                body: JSON.stringify({{password: pw}})
            }});
            const d = await r.json();
            if (d.ok) alert('✅ Şifre güncellendi');
            else alert('❌ ' + (d.error || 'Hata'));
        }}

        // ===== RATINGS VIEW =====
        function showRatingsView() {{
            hideAllViews();
            document.getElementById('ratingsView').style.display = 'block';
            document.getElementById('navRatings').classList.add('active');
            loadRatings();
        }}

        async function loadRatings() {{
            if (!slug) return;
            try {{
                const ratings = await apiJson(apiBase + '/ratings');
                const list = document.getElementById('ratingsList');
                if (!ratings.length) {{
                    list.innerHTML = '<div class="guests-empty">📭 Henüz değerlendirme yok</div>';
                    document.getElementById('ratingAvgCard').style.display = 'none';
                    return;
                }}
                // Compute average
                const avg = ratings.reduce((s, r) => s + r.rating, 0) / ratings.length;
                const avgCard = document.getElementById('ratingAvgCard');
                avgCard.style.display = 'block';
                document.getElementById('ratingAvgNum').textContent = avg.toFixed(1);
                document.getElementById('ratingAvgStars').textContent = '★'.repeat(Math.round(avg)) + '☆'.repeat(5 - Math.round(avg));
                document.getElementById('ratingAvgSub').textContent = ratings.length + ' değerlendirme';

                function stars(n) {{
                    return '★'.repeat(n) + '☆'.repeat(5 - n);
                }}
                list.innerHTML = ratings.map(r => `
                    <div class="rating-card">
                        <div class="rating-stars" style="color:${{r.rating >= 4 ? '#C9A84C' : r.rating >= 3 ? '#E8A040' : '#E05555'}}">${{stars(r.rating)}}</div>
                        <div class="rating-info">
                            <div class="rating-guest">${{r.guest_name ? esc(r.guest_name) : '—'}}</div>
                            <div class="rating-meta">⏰ ${{esc(r.created_at)}}</div>
                        </div>
                        <div class="rating-room">🚪 ${{esc(r.room)}}</div>
                        <span style="font-size:22px;flex-shrink:0">${{r.rating >= 4 ? '😊' : r.rating >= 3 ? '😐' : '😟'}}</span>
                    </div>
                `).join('');
            }} catch(e) {{
                document.getElementById('ratingsList').innerHTML =
                    '<div class="guests-empty" style="color:#E05555">Yükleme hatası</div>';
            }}
        }}

        function openCheckinLink() {{
            const box = document.getElementById('checkinLinkBox');
            box.style.display = box.style.display === 'none' ? 'flex' : 'none';
            document.getElementById('checkinLinkText').textContent =
                window.location.origin + '/hotel/' + slug + '/checkin';
        }}

        function copyCheckinLink() {{
            const link = window.location.origin + '/hotel/' + slug + '/checkin';
            navigator.clipboard.writeText(link).then(() => {{
                const btn = event.target;
                btn.textContent = '✅ Kopyalandı';
                setTimeout(() => btn.textContent = '📋 Kopyala', 2000);
            }});
        }}

        const STATUS_LABELS = {{
            pending: 'Bekliyor',
            checked_in: 'Check-in',
            checked_out: 'Check-out'
        }};

        let allGuests = [];
        let guestStatusFilter = '';

        function setGuestFilter(status, btn) {{
            guestStatusFilter = status;
            document.querySelectorAll('.guest-filter').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            renderGuests();
        }}

        function renderGuests() {{
            const q = (document.getElementById('guestSearch')?.value || '').toLowerCase().trim();
            let data = allGuests;
            if (guestStatusFilter) data = data.filter(g => g.status === guestStatusFilter);
            if (q) data = data.filter(g =>
                (g.first_name + ' ' + g.last_name).toLowerCase().includes(q) ||
                String(g.room).toLowerCase().includes(q) ||
                (g.passport || '').toLowerCase().includes(q)
            );
            const list = document.getElementById('guestsList');
            if (!data.length) {{
                list.innerHTML = '<div class="guests-empty">📭 ' +
                    (allGuests.length ? 'Filtreye uyan misafir yok' : 'Henüz check-in yok') + '</div>';
                return;
            }}
            list.innerHTML = data.map(g => `
                <div class="guest-card" id="gcard-${{g.id}}">
                    <div class="guest-avatar">👤</div>
                    <div class="guest-info">
                        <div class="guest-name">${{esc(g.first_name)}} ${{esc(g.last_name)}}</div>
                        <div class="guest-meta">
                            🪪 ${{esc(g.passport)}}
                            ${{g.nationality ? ' · ' + esc(g.nationality) : ''}}
                            · 📅 ${{g.check_in}} → ${{g.check_out}}
                            · ⏰ ${{g.created_at}}
                        </div>
                    </div>
                    <div class="guest-room">🚪 ${{g.room || '—'}}</div>
                    <span class="status-badge status-${{g.status}}">${{STATUS_LABELS[g.status] || g.status}}</span>
                    <div class="guest-actions">
                        ${{g.status === 'pending' ? `
                            <button class="guest-btn guest-btn-green" onclick="checkInGuest(${{g.id}}, '${{esc(g.room)}}')">✓ Giriş</button>
                        ` : ''}}
                        ${{g.status === 'checked_in' ? `
                            <button class="guest-btn guest-btn-red" onclick="checkOutGuest(${{g.id}})">✗ Çıkış</button>
                        ` : ''}}
                        ${{(!g.room || g.status === 'pending') ? `
                            <button class="guest-btn guest-btn-gold" onclick="assignRoom(${{g.id}})">🚪 Oda</button>
                        ` : ''}}
                    </div>
                </div>
            `).join('');
        }}

        async function loadGuests() {{
            if (!slug) return;
            try {{
                allGuests = await apiJson(apiBase + '/guests');
                const badge = document.getElementById('guestsBadge');
                const active = allGuests.filter(g => g.status === 'checked_in').length;
                badge.textContent = active;
                badge.style.display = active > 0 ? 'inline' : 'none';
                renderGuests();
            }} catch(e) {{
                document.getElementById('guestsList').innerHTML =
                    '<div class="guests-empty" style="color:#E05555">Yükleme hatası</div>';
            }}
        }}

        async function checkInGuest(id, room) {{
            if (!room) {{ assignRoom(id); return; }}
            await apiJson(apiBase + '/guests/' + id + '/status', {{
                method:'POST', headers:{{'Content-Type':'application/json'}},
                body: JSON.stringify({{status:'checked_in', room}})
            }});
            loadGuests();
        }}

        async function checkOutGuest(id) {{
            if (!confirm('Misafiri check-out yapıyorsunuz. Emin misiniz?')) return;
            await apiJson(apiBase + '/guests/' + id + '/status', {{
                method:'POST', headers:{{'Content-Type':'application/json'}},
                body: JSON.stringify({{status:'checked_out'}})
            }});
            loadGuests();
        }}

        function assignRoom(id) {{
            const room = prompt('Oda numarasını girin:');
            if (!room) return;
            apiJson(apiBase + '/guests/' + id + '/status', {{
                method:'POST', headers:{{'Content-Type':'application/json'}},
                body: JSON.stringify({{status:'checked_in', room: room.trim()}})
            }}).then(() => loadGuests());
        }}

        function renderRoomsView() {{
            const q = (document.getElementById('roomSearchGroup').value || '').toLowerCase();
            const roomMap = {{}};
            allData.forEach(m => {{
                if (!roomMap[m.room]) roomMap[m.room] = {{ room: m.room, msgs: [], unread: 0, urgent: 0 }};
                roomMap[m.room].msgs.push(m);
                if (m.is_read === 0 && m.role === 'user') roomMap[m.room].unread++;
                if (m.priority === 'urgent') roomMap[m.room].urgent++;
            }});
            let rooms = Object.values(roomMap).filter(r => !q || r.room.toLowerCase().includes(q));
            rooms.sort((a,b) => b.urgent - a.urgent || b.unread - a.unread);

            const grid = document.getElementById('roomsGrid');
            if (!rooms.length) {{
                grid.innerHTML = '<div class="empty-state"><div class="icon">🚪</div><p>Oda yok</p></div>';
                return;
            }}
            grid.innerHTML = '';
            rooms.forEach(r => {{
                const last = r.msgs[r.msgs.length - 1];
                const guest = allGuests.find(g => g.room == r.room && g.status === 'checked_in');
                const card = document.createElement('div');
                card.style.cssText = 'background:var(--bg2);border-radius:12px;padding:18px;border:1px solid ' +
                    (r.urgent ? 'rgba(224,85,85,0.3)' : 'var(--border)') + ';cursor:pointer;transition:border-color 0.2s;';
                card.onmouseenter = () => card.style.borderColor = 'var(--gold)';
                card.onmouseleave = () => card.style.borderColor = r.urgent ? 'rgba(224,85,85,0.3)' : 'var(--border)';
                const urgentBadge = r.urgent ? `<span class="badge badge-urgent" style="font-size:11px">🔴 ${{r.urgent}} acil</span>` : '';
                const unreadBadge = r.unread ? `<span style="background:#E05555;color:white;padding:2px 8px;border-radius:20px;font-size:11px;font-weight:600">${{r.unread}} yeni</span>` : '';
                const guestLine = guest
                    ? `<div style="font-size:12px;color:var(--gold);margin-bottom:4px">👤 ${{esc(guest.first_name)}} ${{esc(guest.last_name)}} · çıkış: ${{guest.check_out}}</div>`
                    : '';
                card.innerHTML = `
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                        <span style="font-size:15px;font-weight:700;color:var(--gold)">🚪 Oda ${{esc(r.room)}}</span>
                        <div style="display:flex;gap:6px">${{urgentBadge}}${{unreadBadge}}</div>
                    </div>
                    ${{guestLine}}
                    <div style="font-size:12px;color:var(--text3);margin-bottom:8px">${{r.msgs.length}} mesaj · 💬 Yanıtla</div>
                    <div style="font-size:13px;color:var(--text2);overflow:hidden;white-space:nowrap;text-overflow:ellipsis"></div>
                    <div style="font-size:11px;color:var(--text3);margin-top:6px">${{esc(last.created_at)}}</div>
                `;
                card.querySelectorAll('div')[card.querySelectorAll('div').length - 2].textContent = last.message;
                card.onclick = () => openConversation(null, r.room);
                grid.appendChild(card);
            }});
        }}

        // ===== CONVERSATION MODAL =====
        let _modalPollInterval = null;
        let _modalLastMsgId = 0;

        async function openConversation(event, room) {{
            if (event) event.stopPropagation();
            openRoom = room;
            _modalLastMsgId = 0;
            document.getElementById('modalTitle').textContent = '🚪 Oda ' + room;
            document.getElementById('modalBody').innerHTML = '<div style="text-align:center;padding:32px;color:var(--text3)">Yükleniyor...</div>';
            document.getElementById('modalOverlay').classList.add('open');
            document.getElementById('modalFooter').style.display = slug ? 'flex' : 'none';
            document.getElementById('replyInput').value = '';

            // Find guest for this room and show in title
            const guestRow = allGuests.find(g => g.room == room && g.status === 'checked_in');
            if (guestRow) {{
                document.getElementById('modalTitle').textContent =
                    '🚪 Oda ' + room + ' — ' + guestRow.first_name + ' ' + guestRow.last_name;
            }}

            try {{
                const msgs = await apiJson(apiBase + '/room/' + encodeURIComponent(room) + '/messages');
                renderModalMessages(msgs);
                if (msgs.length) _modalLastMsgId = msgs[msgs.length - 1].id;
            }} catch(e) {{
                console.error(e);
                document.getElementById('modalBody').innerHTML = '<div style="color:#E05555;padding:20px">Hata oluştu</div>';
            }}

            // Live poll for new messages every 5 seconds
            if (_modalPollInterval) clearInterval(_modalPollInterval);
            _modalPollInterval = setInterval(async () => {{
                if (!openRoom) return;
                try {{
                    const newMsgs = await apiJson(
                        apiBase + '/room/' + encodeURIComponent(openRoom) +
                        '/new-messages?since_id=' + _modalLastMsgId
                    );
                    if (newMsgs.length) {{
                        const body = document.getElementById('modalBody');
                        const atBottom = body.scrollHeight - body.scrollTop - body.clientHeight < 50;
                        newMsgs.forEach(m => {{
                            const wrap = document.createElement('div');
                            wrap.className = 'chat-bubble-wrap' + (m.role === 'user' ? ' right' : '');
                            const avatar = document.createElement('div');
                            avatar.className = 'bubble-avatar';
                            avatar.textContent = m.role === 'user' ? '👤' : m.role === 'staff' ? '👨‍💼' : '🤖';
                            const inner = document.createElement('div');
                            inner.style.maxWidth = '76%';
                            const bubble = document.createElement('div');
                            bubble.className = 'bubble ' + (m.role === 'user' ? 'user' : m.role === 'staff' ? 'staff' : 'bot');
                            bubble.textContent = m.message;
                            const time = document.createElement('div');
                            time.className = 'bubble-time';
                            time.style.textAlign = m.role === 'user' ? 'right' : 'left';
                            time.textContent = m.created_at;
                            inner.appendChild(bubble); inner.appendChild(time);
                            if (m.role === 'user') {{ wrap.appendChild(inner); wrap.appendChild(avatar); }}
                            else {{ wrap.appendChild(avatar); wrap.appendChild(inner); }}
                            body.appendChild(wrap);
                            _modalLastMsgId = m.id;
                        }});
                        if (atBottom) body.scrollTop = body.scrollHeight;
                    }}
                }} catch(e) {{}}
            }}, 5000);
        }}

        function renderModalMessages(msgs) {{
            const body = document.getElementById('modalBody');
            body.innerHTML = '';
            if (!msgs.length) {{
                body.innerHTML = '<div class="empty-state"><div class="icon">💬</div><p>Henüz mesaj yok</p></div>';
                return;
            }}
            if (msgs.length) _modalLastMsgId = msgs[msgs.length - 1].id;
            msgs.forEach(m => {{
                const wrap = document.createElement('div');
                wrap.className = 'chat-bubble-wrap' + (m.role === 'user' ? ' right' : '');

                const avatar = document.createElement('div');
                avatar.className = 'bubble-avatar';
                avatar.textContent = m.role === 'user' ? '👤' : m.role === 'staff' ? '👨‍💼' : '🤖';

                const inner = document.createElement('div');
                inner.style.maxWidth = '76%';

                const bubble = document.createElement('div');
                bubble.className = 'bubble ' + (m.role === 'user' ? 'user' : m.role === 'staff' ? 'staff' : 'bot');
                bubble.textContent = m.message;

                const time = document.createElement('div');
                time.className = 'bubble-time';
                time.style.textAlign = m.role === 'user' ? 'right' : 'left';
                time.textContent = m.created_at;

                inner.appendChild(bubble);
                inner.appendChild(time);
                if (m.role === 'user') {{ wrap.appendChild(inner); wrap.appendChild(avatar); }}
                else {{ wrap.appendChild(avatar); wrap.appendChild(inner); }}
                body.appendChild(wrap);
            }});
            body.scrollTop = body.scrollHeight;
        }}

        async function sendReply() {{
            if (!slug || !openRoom) return;
            const input = document.getElementById('replyInput');
            const text = input.value.trim();
            if (!text) return;
            input.value = '';
            try {{
                const data = await apiJson(apiBase + '/room/' + encodeURIComponent(openRoom) + '/reply', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{message: text}})
                }});
                if (data.ok) {{
                    const msgs = await apiJson(apiBase + '/room/' + encodeURIComponent(openRoom) + '/messages');
                    renderModalMessages(msgs);
                    loadData();
                }}
            }} catch(e) {{
                console.error(e);
            }}
        }}

        function closeModal(event) {{
            if (event.target === document.getElementById('modalOverlay')) closeModalDirect();
        }}
        function closeModalDirect() {{
            document.getElementById('modalOverlay').classList.remove('open');
            openRoom = null;
            if (_modalPollInterval) {{ clearInterval(_modalPollInterval); _modalPollInterval = null; }}
            _modalLastMsgId = 0;
            // Reset notes panel
            _notesVisible = false;
            document.getElementById('notesPanel').style.display = 'none';
            document.getElementById('notesToggle').style.background = '';
            document.getElementById('notesToggle').style.color = '';
            document.getElementById('notesList').innerHTML = '';
            document.getElementById('noteInput').value = '';
        }}
        document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeModalDirect(); }});

        // ===== ROOM NOTES =====
        let _notesVisible = false;

        function toggleNotes() {{
            _notesVisible = !_notesVisible;
            document.getElementById('notesPanel').style.display = _notesVisible ? 'block' : 'none';
            document.getElementById('notesToggle').style.background =
                _notesVisible ? 'rgba(201,168,76,0.15)' : '';
            document.getElementById('notesToggle').style.color =
                _notesVisible ? 'var(--gold)' : '';
            if (_notesVisible && openRoom) loadNotes();
        }}

        async function loadNotes() {{
            if (!slug || !openRoom) return;
            try {{
                const notes = await apiJson(apiBase + '/room/' + encodeURIComponent(openRoom) + '/notes');
                renderNotes(notes);
            }} catch(e) {{}}
        }}

        function renderNotes(notes) {{
            const list = document.getElementById('notesList');
            if (!notes.length) {{
                list.innerHTML = '<div style="color:var(--text3);font-size:12px;padding:4px 0">Henüz not yok</div>';
                return;
            }}
            list.innerHTML = notes.map(n => `
                <div class="note-item">
                    <div style="flex:1">
                        <div class="note-text">${{esc(n.note)}}</div>
                        <div class="note-meta">${{esc(n.author)}} · ${{n.created_at}}</div>
                    </div>
                    <button class="note-del" onclick="deleteNote(${{n.id}})" title="Sil">✕</button>
                </div>
            `).join('');
        }}

        async function addNote() {{
            const input = document.getElementById('noteInput');
            const text = input.value.trim();
            if (!text || !slug || !openRoom) return;
            input.value = '';
            try {{
                await apiJson(apiBase + '/room/' + encodeURIComponent(openRoom) + '/notes', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{note: text, author: 'Персонал'}})
                }});
                loadNotes();
            }} catch(e) {{}}
        }}

        async function deleteNote(id) {{
            if (!slug || !openRoom) return;
            try {{
                await fetch(apiBase + '/room/' + encodeURIComponent(openRoom) + '/notes/' + id,
                    {{method: 'DELETE', credentials: 'same-origin'}});
                loadNotes();
            }} catch(e) {{}}
        }}

        // ===== URGENT =====
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

        function playAlert() {{
            try {{
                const ctx = _getAudioCtx();
                [0, 0.3, 0.6].forEach(delay => {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.connect(gain); gain.connect(ctx.destination);
                    osc.frequency.value = 880; osc.type = 'sine';
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
            popup.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;background:#E05555;color:white;padding:18px 22px;border-radius:12px;font-size:14px;font-weight:500;box-shadow:0 8px 32px rgba(224,85,85,0.4);animation:slideIn 0.3s ease;max-width:300px;line-height:1.6;cursor:pointer;';
            const title = document.createElement('b'); title.textContent = '🔴 ACİL TALEP!';
            const room = document.createElement('div'); room.textContent = '🚪 Oda ' + msg.room;
            const msgEl = document.createElement('div'); msgEl.textContent = '💬 ' + msg.message;
            const hint = document.createElement('small'); hint.style.opacity = '0.75'; hint.textContent = 'Tıkla → kapat';
            popup.append(title, document.createElement('br'), room, msgEl, document.createElement('br'), hint);
            popup.onclick = () => popup.remove();
            document.body.appendChild(popup);
            setTimeout(() => popup.remove(), 8000);
        }}

        function sendPushNotification(msg, isUrgent=true) {{
            if (!msg || !('Notification' in window)) return;
            const title = isUrgent ? '🔴 ACİL MESAJ!' : '💬 Yeni Mesaj';
            const body  = 'Oda ' + msg.room + ': ' + (msg.message || '').slice(0, 80);
            const show  = () => {{
                const n = new Notification(title, {{ body, icon: '/favicon.ico', tag: 'smartstay-' + msg.room }});
                n.onclick = () => {{ window.focus(); openConversation(null, msg.room); n.close(); }};
            }};
            if (Notification.permission === 'granted') show();
            else if (Notification.permission !== 'denied') Notification.requestPermission().then(p => {{ if (p === 'granted') show(); }});
        }}

        // ===== THEME =====
        function toggleTheme() {{
            const isLight = document.body.classList.toggle('light');
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
            document.getElementById('themeLabel').textContent = isLight ? 'Dark mode' : 'Light mode';
            document.querySelector('#themeNav .nav-icon').textContent = isLight ? '🌙' : '☀️';
            // Redraw Chart.js with updated colors
            if (document.getElementById('chartsGrid').style.display !== 'none') {{
                Object.keys(_chartInstances).forEach(id => _destroyChart(id));
                loadCharts();
            }}
        }}

        // ===== CHARTS (Chart.js) =====
        const _chartInstances = {{}};
        function _destroyChart(id) {{
            if (_chartInstances[id]) {{ _chartInstances[id].destroy(); delete _chartInstances[id]; }}
        }}
        function _mkChart(id, type, labels, datasets, opts={{}}) {{
            _destroyChart(id);
            const canvas = document.getElementById(id);
            if (!canvas) return;
            const isDark = !document.body.classList.contains('light');
            const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)';
            const textColor = isDark ? '#888' : '#666';
            _chartInstances[id] = new Chart(canvas.getContext('2d'), {{
                type,
                data: {{ labels, datasets }},
                options: {{
                    responsive: true, maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ labels: {{ color: textColor, font: {{ size: 11, family: 'Inter' }} }} }},
                        tooltip: {{ bodyFont: {{ family: 'Inter' }}, titleFont: {{ family: 'Inter' }} }}
                    }},
                    scales: type === 'doughnut' || type === 'pie' ? {{}} : {{
                        x: {{ ticks: {{ color: textColor, font: {{ size: 10 }} }}, grid: {{ color: gridColor }} }},
                        y: {{ ticks: {{ color: textColor, font: {{ size: 10 }} }}, grid: {{ color: gridColor }} }}
                    }},
                    ...opts
                }}
            }});
        }}

        function loadCharts() {{
            if (!slug) return;
            // Keep existing avg_rating from stats
            apiJson(apiBase + '/stats').then(data => {{
                if (data.avg_rating) document.getElementById('statRating').textContent = data.avg_rating + '★';
            }}).catch(() => {{}});

            apiJson(apiBase + '/analytics').then(d => {{
                const AL = DASH_I18N[_dashLang] || DASH_I18N.en;
                const grid = document.getElementById('chartsGrid');
                grid.style.display = 'block';

                // KPIs
                document.getElementById('kpi-guests').textContent   = d.funnel?.check_ins ?? '—';
                document.getElementById('kpi-messaged').textContent = d.funnel?.messaged ?? '—';
                document.getElementById('kpi-rated').textContent    = d.funnel?.rated ?? '—';
                document.getElementById('kpi-response').textContent = d.avg_response_min != null ? d.avg_response_min : '—';

                // Line chart: messages by day
                const dayLabels = d.messages_by_day.map(x => x.date.slice(5)); // MM-DD
                const dayCounts = d.messages_by_day.map(x => x.count);
                _mkChart('chartDays', 'line', dayLabels, [{{
                    label: AL.chartLblMessages, data: dayCounts,
                    borderColor: '#C9A84C', backgroundColor: 'rgba(201,168,76,0.1)',
                    tension: 0.4, fill: true, pointRadius: 2, borderWidth: 2
                }}]);

                // Bar chart: messages by hour
                const hourLabels = d.messages_by_hour.map(x => x.hour + 'h');
                const hourCounts = d.messages_by_hour.map(x => x.count);
                const peakHour  = hourCounts.indexOf(Math.max(...hourCounts));
                _mkChart('chartHours', 'bar', hourLabels, [{{
                    label: AL.chartLblMessages, data: hourCounts,
                    backgroundColor: hourCounts.map((_, i) =>
                        i === peakHour ? '#E8C96A' : 'rgba(201,168,76,0.5)'),
                    borderRadius: 4, borderWidth: 0
                }}], {{ plugins: {{ legend: {{ display: false }} }} }});

                // Doughnut: ratings
                const ratingTotal = d.rating_dist.reduce((a, b) => a + b, 0);
                if (ratingTotal > 0) {{
                    _mkChart('chartRatings', 'doughnut',
                        ['1★','2★','3★','4★','5★'],
                        [{{ data: d.rating_dist,
                           backgroundColor: ['#E05555','#E07040','#E8A040','#a0d060','#4CAF50'],
                           borderWidth: 0 }}],
                        {{ plugins: {{ legend: {{ position: 'right' }} }}, cutout: '65%' }});
                }} else {{
                    const ctx = document.getElementById('chartRatings');
                    if (ctx && ctx.parentElement) {{
                        ctx.parentElement.innerHTML = '<div style="color:var(--text3);font-size:13px;text-align:center;padding-top:50px">' + AL.chartNoRatings + '</div>';
                    }}
                }}

                // Horizontal bar: top categories
                if (d.top_categories && d.top_categories.length) {{
                    const catLabels = d.top_categories.map(c => c.category.replace(/_/g,' '));
                    const catCounts = d.top_categories.map(c => c.count);
                    _mkChart('chartCategories', 'bar', catLabels, [{{
                        label: AL.chartLblRequests, data: catCounts,
                        backgroundColor: 'rgba(74,176,232,0.7)',
                        borderRadius: 4, borderWidth: 0
                    }}], {{
                        indexAxis: 'y',
                        plugins: {{ legend: {{ display: false }} }}
                    }});
                }} else {{
                    document.getElementById('noCats').style.display = 'block';
                    const ctx = document.getElementById('chartCategories');
                    if (ctx) ctx.style.display = 'none';
                }}

                // Funnel
                const f = d.funnel;
                const funnelMax = Math.max(f.check_ins, 1);
                const funnelSteps = [
                    {{ label: AL.funnelLblGuests,   val: f.check_ins, color: '#C9A84C' }},
                    {{ label: AL.funnelLblMessaged, val: f.messaged,  color: '#4ab0e8' }},
                    {{ label: AL.funnelLblRated,    val: f.rated,     color: '#4CAF50' }},
                ];
                document.getElementById('funnelChart').innerHTML = funnelSteps.map(s => {{
                    const pct = Math.round((s.val / funnelMax) * 100);
                    return `<div style="margin-bottom:14px">
                        <div style="display:flex;justify-content:space-between;font-size:12px;color:var(--text2);margin-bottom:4px">
                            <span>${{s.label}}</span><b style="color:var(--text)">${{s.val}} (${{pct}}%)</b>
                        </div>
                        <div style="background:var(--bg3);border-radius:4px;height:10px;overflow:hidden">
                            <div style="width:${{pct}}%;height:100%;background:${{s.color}};border-radius:4px;transition:width 0.6s ease"></div>
                        </div>
                    </div>`;
                }}).join('');

            }}).catch(handleDashboardError);
        }}

        // ===== MISC =====
        function markRead() {{ apiJson(markReadUrl, {{method:'POST'}}).then(() => loadData()).catch(handleDashboardError); }}
        function goToEdit() {{ if (slug) window.location.href = '/hotel/' + slug + '/edit'; }}
        function goToQR() {{ if (slug) window.open('/hotel/' + slug + '/qrcodes'); else window.open('/qrcodes'); }}
        function goToBuffet() {{ if (slug) window.location.href = '/hotel/' + slug + '/buffet'; }}
        function exportExcel() {{ if (slug) window.location.href = apiBase + '/export'; }}
        function exportGuests() {{ if (slug) window.location.href = apiBase + '/guests/export'; }}

        // ===== INIT =====
        if (localStorage.getItem('theme') === 'light') {{
            document.body.classList.add('light');
            document.getElementById('themeLabel').textContent = 'Dark mode';
            document.querySelector('#themeNav .nav-icon').textContent = '🌙';
        }}

        // Role-based tab visibility
        // Roles: manager (full), receptionist (messages/guests/requests), housekeeping (requests only)
        const ROLE_TABS = {{
            manager:      ['navMessages','navRooms','navGuests','navCalendar','navRequests','navRatings','navAnalytics','navServices','navStaffChat','navStaff'],
            receptionist: ['navMessages','navRooms','navGuests','navRequests','navStaffChat'],
            housekeeping: ['navRequests','navStaffChat'],
        }};
        // Elements only managers can see (settings, QR, etc.)
        const MANAGER_ONLY_SELECTORS = ['.manager-only'];

        let _currentRole = 'manager';

        function applyRoleVisibility(role) {{
            _currentRole = role;
            const allowed = ROLE_TABS[role] || ROLE_TABS['receptionist'];
            ['navMessages','navRooms','navGuests','navCalendar','navRequests','navRatings','navAnalytics','navServices','navStaffChat','navStaff'].forEach(id => {{
                const el = document.getElementById(id);
                if (el) el.style.display = allowed.includes(id) ? '' : 'none';
            }});
            // Hide manager-only sidebar items (settings, QR, etc.) for non-managers
            if (role !== 'manager') {{
                document.querySelectorAll('.manager-only').forEach(el => el.style.display = 'none');
                // Also hide sidebar bottom buttons (settings/QR) for non-managers
                const sideBottom = document.querySelector('.sidebar-bottom');
                if (sideBottom) sideBottom.style.display = 'none';
            }}
            // Auto-navigate to first allowed tab
            const firstNav = document.getElementById(allowed[0]);
            if (firstNav) firstNav.click();
        }}

        if (slug) {{
            apiJson(apiBase + '/info').then(d => {{
                document.getElementById('hotelName').textContent = d.name || slug;
                document.getElementById('pageTitle').textContent = d.name + ' — Panel';
                _baseTitle = (d.name || slug) + ' — SmartStay';
                document.title = _baseTitle;
            }}).catch(handleDashboardError);

            // Fetch current user role and adapt UI
            apiJson(apiBase + '/me').then(d => {{
                applyRoleVisibility(d.role || 'manager');
                // Show staff name if not manager
                if (d.role && d.role !== 'manager' && d.name) {{
                    document.getElementById('hotelName').textContent = d.name;
                }}
                // Store name for staff chat sender highlighting
                if (d.name) _scMyName = d.name;
                // Start background staff chat polling (badge)
                scStartBgPoll();
            }}).catch(() => {{ applyRoleVisibility('manager'); scStartBgPoll(); }});

            loadCharts();
            loadPlanUsage();
            loadGuestsBadge();
            loadRequestsBadge();
            setInterval(loadCharts, 30000);
            setInterval(loadPlanUsage, 60000);
            setInterval(loadGuestsBadge, 30000);
            setInterval(loadRequestsBadge, 60000);
        }}

        function loadGuestsBadge() {{
            if (!slug) return;
            apiJson(apiBase + '/guests').then(guests => {{
                const active = guests.filter(g => g.status === 'checked_in').length;
                const badge = document.getElementById('guestsBadge');
                badge.textContent = active;
                badge.style.display = active > 0 ? 'inline' : 'none';
            }}).catch(() => {{}});
        }}

        function loadPlanUsage() {{
            if (!slug) return;
            apiJson(apiBase + '/plan').then(d => {{
                const wrap = document.getElementById('planBar');
                const badge = document.getElementById('planBadge');
                const text = document.getElementById('planUsageText');
                const fill = document.getElementById('planFill');
                wrap.style.display = 'block';
                const plan = (d.plan || 'trial').toUpperCase();
                badge.textContent = plan;
                badge.className = 'plan-badge plan-' + d.plan;
                if (d.unlimited) {{
                    text.textContent = d.used + ' mesaj (limitsiz)';
                    fill.style.width = '100%';
                    fill.classList.remove('warn');
                }} else {{
                    text.textContent = d.used + ' / ' + d.limit + ' mesaj (' + d.percent + '%)';
                    fill.style.width = Math.min(d.percent, 100) + '%';
                    fill.classList.toggle('warn', d.percent >= 85);
                }}
            }}).catch(() => {{}});
        }}

        if ('Notification' in window && Notification.permission === 'default') {{
            setTimeout(() => Notification.requestPermission(), 2000);
        }}

        loadData();
        setInterval(loadData, 3000);

        // ===== DASHBOARD i18n =====
        const DASH_I18N = {{
            en: {{
                nt_all:'All Messages', nt_urgent:'Urgent', nt_guest:'Guest', nt_rooms:'Rooms',
                nt_checkin:'Check-in', nt_calendar:'Calendar', nt_requests:'Requests',
                nt_ratings:'Ratings', nt_analytics:'Analytics', nt_services:'Services',
                nt_staffchat:'Staff Chat', nt_staff:'Staff', nt_buffet:'Buffet AI',
                nt_settings:'Settings', nt_qr:'QR Codes', pageTitle:'Manager Dashboard',
                liveStatus:'Live • Updates every 3s',
                lblStatTotal:'Total Messages', lblStatUrgent:'Urgent', lblStatRooms:'Active Rooms',
                lblStatUnread:'Unread', lblStatRating:'Avg. Rating',
                kpiGuestsLbl:'GUESTS', kpiMsgLbl:'MESSAGED', kpiRatedLbl:'RATED', kpiRespLbl:'RESPONSE (MIN)',
                chartDaysTitle:'📈 Guest messages — last 30 days', chartHoursTitle:'🕐 Activity by hour',
                chartRatingsTitle:'⭐ Rating distribution', chartCatsTitle:'📋 Top request categories',
                chartFunnelTitle:'🔽 Engagement funnel',
                fAllLbl:'All', fUrgentLbl:'Urgent', fUserLbl:'Guest',
                thPriority:'Priority', thRoom:'Room', thWho:'Who', thMsg:'Message', thTime:'Time',
                guestsTitle:'🛎️ Check-in List', guestsSub:'Guests who completed digital check-in',
                btnRefresh:'Refresh', btnCheckinLink:'Check-in Link',
                gfAll:'All', gfPending:'⏳ Pending', gfIn:'✅ Checked In', gfOut:'🚪 Checked Out',
                svcPageTitle:'🛎️ Services Menu',
                svcSubTitle:'Hotel services catalog',
                svcAddBtn:'+ Add Service',
                svcLblIcon:'ICON (emoji)', svcLblCategory:'CATEGORY',
                svcLblName:'SERVICE NAME', svcLblDesc:'DESCRIPTION (optional)',
                svcLblPrice:'PRICE (0 = free)', svcLblCurrency:'CURRENCY',
                svcCatGeneral:'🛎️ General', svcCatFood:'🍽️ Food & Drinks',
                svcCatHousekeeping:'🧹 Housekeeping', svcCatSpa:'💆 Spa',
                svcCatTransport:'🚖 Transport', svcCatMaintenance:'🔧 Maintenance',
                svcSaveBtn:'💾 Save', svcCancelBtn:'Cancel',
                svcNewTitle:'New Service', svcEditTitle:'Edit Service',
                svcLoading:'Loading...', svcEmpty:'No services added yet. Click «+ Add Service».',
                svcActive:'Active', svcFree:'Free', svcEdit:'Edit', svcError:'Failed to load',
                scPageTitle:'💬 Staff Chat', scPageSub:'Internal chat — staff only',
                analyticsPageTitle:'📊 Analytics', analyticsPageSub:'Hotel performance summary',
                chartLblMessages:'Messages', chartLblRequests:'Requests', chartNoRatings:'No ratings yet',
                funnelLblGuests:'🏨 Guests reg.', funnelLblMessaged:'💬 Sent a message', funnelLblRated:'⭐ Left a rating',
                ratingsPageTitle:'⭐ Ratings', ratingsPageSub:'Guest scores and comments'
            }},
            ru: {{
                nt_all:'Все сообщения', nt_urgent:'Срочные', nt_guest:'Гость', nt_rooms:'Номера',
                nt_checkin:'Заезд', nt_calendar:'Календарь', nt_requests:'Запросы',
                nt_ratings:'Рейтинги', nt_analytics:'Аналитика', nt_services:'Услуги',
                nt_staffchat:'Чат персонала', nt_staff:'Персонал', nt_buffet:'Буфет AI',
                nt_settings:'Настройки', nt_qr:'QR-коды', pageTitle:'Панель управления',
                liveStatus:'Live • Обновляется каждые 3с',
                lblStatTotal:'Всего сообщений', lblStatUrgent:'Срочные', lblStatRooms:'Активных номеров',
                lblStatUnread:'Непрочитанных', lblStatRating:'Средний рейтинг',
                kpiGuestsLbl:'ГОСТЕЙ', kpiMsgLbl:'НАПИСАЛИ', kpiRatedLbl:'ОЦЕНИЛИ', kpiRespLbl:'ОТВЕТ (МИН)',
                chartDaysTitle:'📈 Сообщения гостей — последние 30 дней', chartHoursTitle:'🕐 Активность по часам',
                chartRatingsTitle:'⭐ Распределение рейтингов', chartCatsTitle:'📋 Топ категории запросов',
                chartFunnelTitle:'🔽 Воронка вовлечённости',
                fAllLbl:'Все', fUrgentLbl:'Срочные', fUserLbl:'Гость',
                thPriority:'Приоритет', thRoom:'Номер', thWho:'Кто', thMsg:'Сообщение', thTime:'Время',
                guestsTitle:'🛎️ Список заездов', guestsSub:'Гости, прошедшие цифровой check-in',
                btnRefresh:'Обновить', btnCheckinLink:'Ссылка check-in',
                gfAll:'Все', gfPending:'⏳ Ожидают', gfIn:'✅ Заселились', gfOut:'🚪 Выехали',
                svcPageTitle:'🛎️ Меню услуг',
                svcSubTitle:'Каталог услуг отеля',
                svcAddBtn:'+ Добавить услугу',
                svcLblIcon:'ИКОНКА (эмодзи)', svcLblCategory:'КАТЕГОРИЯ',
                svcLblName:'НАЗВАНИЕ УСЛУГИ', svcLblDesc:'ОПИСАНИЕ (необязательно)',
                svcLblPrice:'ЦЕНА (0 = бесплатно)', svcLblCurrency:'ВАЛЮТА',
                svcCatGeneral:'🛎️ Прочее', svcCatFood:'🍽️ Питание',
                svcCatHousekeeping:'🧹 Горничная', svcCatSpa:'💆 Спа',
                svcCatTransport:'🚖 Транспорт', svcCatMaintenance:'🔧 Технический',
                svcSaveBtn:'💾 Сохранить', svcCancelBtn:'Отмена',
                svcNewTitle:'Новая услуга', svcEditTitle:'Редактировать услугу',
                svcLoading:'Загрузка...', svcEmpty:'Услуги пока не добавлены. Нажмите «+ Добавить услугу».',
                svcActive:'Активна', svcFree:'Бесплатно', svcEdit:'Изм.', svcError:'Ошибка загрузки',
                scPageTitle:'💬 Чат персонала', scPageSub:'Внутренний чат — только для сотрудников',
                analyticsPageTitle:'📊 Аналитика', analyticsPageSub:'Сводка по работе отеля',
                chartLblMessages:'Сообщения', chartLblRequests:'Запросов', chartNoRatings:'Рейтингов пока нет',
                funnelLblGuests:'🏨 Гостей зарег.', funnelLblMessaged:'💬 Написали в чат', funnelLblRated:'⭐ Оставили рейтинг',
                ratingsPageTitle:'⭐ Рейтинги', ratingsPageSub:'Оценки и комментарии гостей'
            }},
            tr: {{
                nt_all:'Tüm Mesajlar', nt_urgent:'Acil', nt_guest:'Misafir', nt_rooms:'Odalar',
                nt_checkin:'Check-in', nt_calendar:'Takvim', nt_requests:'Talepler',
                nt_ratings:'Değerlendirmeler', nt_analytics:'Analitik', nt_services:'Hizmetler',
                nt_staffchat:'Personel Sohbeti', nt_staff:'Personel', nt_buffet:'Büfe AI',
                nt_settings:'Ayarlar', nt_qr:'QR Kodlar', pageTitle:'Yönetici Paneli',
                liveStatus:'Canlı • Her 3s güncellenir',
                lblStatTotal:'Toplam Mesaj', lblStatUrgent:'Acil Talep', lblStatRooms:'Aktif Oda',
                lblStatUnread:'Okunmamış', lblStatRating:'Ort. Puan',
                kpiGuestsLbl:'MİSAFİR', kpiMsgLbl:'YAZDI', kpiRatedLbl:'PUANLADI', kpiRespLbl:'YANIT (DK)',
                chartDaysTitle:'📈 Misafir mesajları — son 30 gün', chartHoursTitle:'🕐 Saate göre aktivite',
                chartRatingsTitle:'⭐ Puan dağılımı', chartCatsTitle:'📋 En çok talep kategorileri',
                chartFunnelTitle:'🔽 Etkileşim hunisi',
                fAllLbl:'Tümü', fUrgentLbl:'Acil', fUserLbl:'Misafir',
                thPriority:'Öncelik', thRoom:'Oda', thWho:'Kim', thMsg:'Mesaj', thTime:'Saat',
                guestsTitle:'🛎️ Check-in Listesi', guestsSub:'Dijital check-in yapan misafirler',
                btnRefresh:'Yenile', btnCheckinLink:'Check-in Linki',
                gfAll:'Tümü', gfPending:'⏳ Bekliyor', gfIn:'✅ İçeride', gfOut:'🚪 Çıktı',
                svcPageTitle:'🛎️ Hizmetler Menüsü',
                svcSubTitle:'Otel hizmetleri kataloğu',
                svcAddBtn:'+ Hizmet Ekle',
                svcLblIcon:'SİMGE (emoji)', svcLblCategory:'KATEGORİ',
                svcLblName:'HİZMET ADI', svcLblDesc:'AÇIKLAMA (isteğe bağlı)',
                svcLblPrice:'FİYAT (0 = ücretsiz)', svcLblCurrency:'PARA BİRİMİ',
                svcCatGeneral:'🛎️ Genel', svcCatFood:'🍽️ Yiyecek & İçecek',
                svcCatHousekeeping:'🧹 Temizlik', svcCatSpa:'💆 Spa',
                svcCatTransport:'🚖 Ulaşım', svcCatMaintenance:'🔧 Teknik',
                svcSaveBtn:'💾 Kaydet', svcCancelBtn:'İptal',
                svcNewTitle:'Yeni Hizmet', svcEditTitle:'Hizmeti Düzenle',
                svcLoading:'Yükleniyor...', svcEmpty:'Henüz hizmet eklenmedi. «+ Hizmet Ekle» butonuna tıklayın.',
                svcActive:'Aktif', svcFree:'Ücretsiz', svcEdit:'Düzenle', svcError:'Yükleme hatası',
                scPageTitle:'💬 Personel Sohbeti', scPageSub:'Dahili sohbet — yalnızca personel',
                analyticsPageTitle:'📊 Analitik', analyticsPageSub:'Otel performans özeti',
                chartLblMessages:'Mesajlar', chartLblRequests:'Talepler', chartNoRatings:'Henüz değerlendirme yok',
                funnelLblGuests:'🏨 Kayıtlı misafir', funnelLblMessaged:'💬 Mesaj gönderdi', funnelLblRated:'⭐ Değerlendirme bıraktı',
                ratingsPageTitle:'⭐ Değerlendirmeler', ratingsPageSub:'Misafir puanları ve yorumlar'
            }},
            uz: {{
                nt_all:"Barcha xabarlar", nt_urgent:"Shoshilinch", nt_guest:"Mehmon", nt_rooms:"Xonalar",
                nt_checkin:"Ro'yxatdan o'tish", nt_calendar:"Taqvim", nt_requests:"So'rovlar",
                nt_ratings:"Reytinglar", nt_analytics:"Analitika", nt_services:"Xizmatlar",
                nt_staffchat:"Xodimlar chati", nt_staff:"Xodimlar", nt_buffet:"Bufet AI",
                nt_settings:"Sozlamalar", nt_qr:"QR kodlar", pageTitle:"Boshqaruv paneli",
                liveStatus:"Jonli • Har 3s yangilanadi",
                lblStatTotal:"Jami xabarlar", lblStatUrgent:"Shoshilinch", lblStatRooms:"Faol xonalar",
                lblStatUnread:"O'qilmagan", lblStatRating:"O'rt. reyting",
                kpiGuestsLbl:"MEHMONLAR", kpiMsgLbl:"YOZDI", kpiRatedLbl:"BAHOLADI", kpiRespLbl:"JAVOB (MIN)",
                chartDaysTitle:"📈 Mehmon xabarlari — oxirgi 30 kun", chartHoursTitle:"🕐 Soatlik faollik",
                chartRatingsTitle:"⭐ Reyting taqsimoti", chartCatsTitle:"📋 Top so'rov kategoriyalari",
                chartFunnelTitle:"🔽 Jalb qilish hunisi",
                fAllLbl:"Barchasi", fUrgentLbl:"Shoshilinch", fUserLbl:"Mehmon",
                thPriority:"Muhimlik", thRoom:"Xona", thWho:"Kim", thMsg:"Xabar", thTime:"Vaqt",
                guestsTitle:"🛎️ Check-in Ro'yxati", guestsSub:"Raqamli check-in qilgan mehmonlar",
                btnRefresh:"Yangilash", btnCheckinLink:"Check-in Havolasi",
                gfAll:"Barchasi", gfPending:"⏳ Kutmoqda", gfIn:"✅ Ichkarida", gfOut:"🚪 Chiqdi",
                svcPageTitle:"🛎️ Xizmatlar Menyusi",
                svcSubTitle:"Mehmonxona xizmatlari katalogi",
                svcAddBtn:"+ Xizmat Qo'shish",
                svcLblIcon:"BELGI (emoji)", svcLblCategory:"KATEGORIYA",
                svcLblName:"XIZMAT NOMI", svcLblDesc:"TAVSIF (ixtiyoriy)",
                svcLblPrice:"NARX (0 = bepul)", svcLblCurrency:"VALYUTA",
                svcCatGeneral:"🛎️ Umumiy", svcCatFood:"🍽️ Taom va ichimlik",
                svcCatHousekeeping:"🧹 Xonadon tozalash", svcCatSpa:"💆 Spa",
                svcCatTransport:"🚖 Transport", svcCatMaintenance:"🔧 Texnik xizmat",
                svcSaveBtn:"💾 Saqlash", svcCancelBtn:"Bekor qilish",
                svcNewTitle:"Yangi xizmat", svcEditTitle:"Xizmatni tahrirlash",
                svcLoading:"Yuklanmoqda...", svcEmpty:"Hali xizmat qo'shilmagan. «+ Xizmat Qo'shish» tugmasini bosing.",
                svcActive:"Faol", svcFree:"Bepul", svcEdit:"Tahrirlash", svcError:"Yuklash xatosi",
                scPageTitle:"💬 Xodimlar Chati", scPageSub:"Ichki chat — faqat xodimlar uchun",
                analyticsPageTitle:"📊 Analitika", analyticsPageSub:"Mehmonxona ishlashi xulosasi",
                chartLblMessages:"Xabarlar", chartLblRequests:"So'rovlar", chartNoRatings:"Hali reytinglar yo'q",
                funnelLblGuests:"🏨 Ro'yxatdagi mehmonlar", funnelLblMessaged:"💬 Xabar yozdi", funnelLblRated:"⭐ Reyting qoldirdi",
                ratingsPageTitle:"⭐ Reytinglar", ratingsPageSub:"Mehmon ballari va sharhlari"
            }}
        }};

        let _dashLang = localStorage.getItem('ss_lang') || 'en';
        if (!DASH_I18N[_dashLang]) _dashLang = 'en';

        function applyDashLang() {{
            const L = DASH_I18N[_dashLang] || DASH_I18N.en;
            Object.keys(L).forEach(id => {{
                const el = document.getElementById(id);
                if (el) el.textContent = L[id];
            }});
            document.querySelectorAll('.lang-btn-dash').forEach(b => {{
                b.classList.toggle('active', b.textContent === _dashLang.toUpperCase());
            }});
        }}

        function setDashLang(l) {{
            _dashLang = l;
            localStorage.setItem('ss_lang', l);
            applyDashLang();
        }}

        async function translateMsg(e, btn) {{
            e.stopPropagation();
            const tr = btn.closest('tr');
            const cacheKey = (tr.dataset.msgkey || '') + '|' + _dashLang;
            const td = btn.closest('td').previousElementSibling.previousElementSibling;
            const preview = td.querySelector('.msg-preview');
            const translated = td.querySelector('.msg-translated');
            if (!preview || !translated) return;

            // Toggle off if already showing
            if (translated.style.display !== 'none') {{
                translated.style.display = 'none';
                btn.style.color = '';
                return;
            }}

            // Already in cache — just show
            if (_translCache[cacheKey]) {{
                translated.textContent = '→ ' + _translCache[cacheKey];
                translated.style.display = 'block';
                btn.style.color = 'var(--gold)';
                return;
            }}

            btn.textContent = '⏳';
            btn.disabled = true;
            try {{
                const res = await fetch('/api/translate', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{ text: preview.textContent, target: _dashLang }})
                }});
                const data = await res.json();
                if (data.translation) {{
                    _translCache[cacheKey] = data.translation;
                    translated.textContent = '→ ' + data.translation;
                    translated.style.display = 'block';
                    btn.style.color = 'var(--gold)';
                }} else {{
                    translated.textContent = '⚠️ Error';
                    translated.style.display = 'block';
                }}
            }} catch(err) {{
                translated.textContent = '⚠️ Network error';
                translated.style.display = 'block';
            }}
            btn.textContent = '🌐';
            btn.disabled = false;
        }}

        applyDashLang();
    </script>
</body>
</html>
"""

def get_dashboard_html(hotel_name="SmartStay"):
    return DASHBOARD_HTML.format(hotel_name=hotel_name)
