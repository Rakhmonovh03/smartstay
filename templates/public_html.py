def get_public_page_html(hotel: dict, avg_rating: float, rating_count: int, recent_reviews: list) -> str:
    name            = hotel.get("name", "")
    slug            = hotel.get("slug", "")
    photo_url       = hotel.get("photo_url", "")
    page_desc       = hotel.get("page_description", "") or hotel.get("info", "")
    amenities_raw   = hotel.get("amenities", "")
    ai_name         = hotel.get("ai_name", "AI Asistan")
    booking_url     = hotel.get("booking_url", "")

    # Parse amenities
    amenities = [a.strip() for a in amenities_raw.split(",") if a.strip()] if amenities_raw else []

    # Rating stars HTML
    def stars_html(r):
        r = round(r or 0)
        return "★" * r + "☆" * (5 - r)

    # Amenity pill
    amenity_pills = "".join(
        f'<span class="pill">{a}</span>' for a in amenities
    ) if amenities else ""

    # Reviews HTML
    reviews_html = ""
    for rv in recent_reviews[:6]:
        stars = "★" * rv.get("rating", 0) + "☆" * (5 - rv.get("rating", 0))
        date  = (rv.get("created_at") or "")[:10]
        reviews_html += f"""
        <div class="review-card">
            <div class="review-stars">{stars}</div>
            <div class="review-date">{date}</div>
        </div>"""

    # Photo section
    if photo_url:
        hero_style = f'background:url("{photo_url}") center/cover no-repeat;'
        hero_overlay = '<div class="hero-overlay"></div>'
    else:
        hero_style = "background:linear-gradient(135deg,#0a0a0a 0%,#1a1410 60%,#2a1a05 100%);"
        hero_overlay = ""

    rating_display = f"{avg_rating:.1f}" if avg_rating else "—"
    booking_btn = f'<a href="{booking_url}" class="btn-booking" target="_blank" rel="noopener">📅 Бронировать</a>' if booking_url else ""

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#C9A84C">
<title>{name}</title>
<meta name="description" content="{page_desc[:160]}">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  :root {{ --gold:#C9A84C; --gold2:#E8C96A; --bg:#111; --bg2:#1a1a1a; --bg3:#222; --text:#eee; --text2:#888; }}
  body {{ font-family:'Segoe UI',system-ui,sans-serif; background:var(--bg); color:var(--text); min-height:100vh; }}

  /* HERO */
  .hero {{ position:relative; height:320px; display:flex; flex-direction:column;
           align-items:center; justify-content:flex-end; padding:32px 24px;
           {hero_style} }}
  .hero-overlay {{ position:absolute; inset:0; background:linear-gradient(to top,rgba(0,0,0,0.85) 0%,rgba(0,0,0,0.3) 60%,transparent 100%); }}
  .hero-content {{ position:relative; z-index:1; text-align:center; max-width:600px; }}
  .hotel-badge {{ display:inline-block; background:rgba(201,168,76,0.2); border:1px solid rgba(201,168,76,0.4);
                  border-radius:20px; padding:4px 14px; font-size:11px; letter-spacing:2px;
                  text-transform:uppercase; color:var(--gold); margin-bottom:12px; }}
  .hotel-name {{ font-size:32px; font-weight:800; color:#fff; text-shadow:0 2px 8px rgba(0,0,0,0.5); margin-bottom:8px; }}
  .rating-row {{ display:flex; align-items:center; justify-content:center; gap:10px; }}
  .stars {{ color:var(--gold); font-size:18px; letter-spacing:2px; }}
  .rating-num {{ font-size:20px; font-weight:700; color:#fff; }}
  .rating-cnt {{ font-size:13px; color:rgba(255,255,255,0.6); }}

  /* CONTENT */
  .content {{ max-width:680px; margin:0 auto; padding:32px 20px 60px; }}

  /* ACTIONS */
  .actions {{ display:flex; gap:12px; margin-bottom:32px; flex-wrap:wrap; }}
  .btn-chat {{ flex:1; min-width:180px; display:flex; align-items:center; justify-content:center; gap:8px;
               padding:16px 24px; background:linear-gradient(135deg,var(--gold),var(--gold2));
               color:#1a1a1a; font-weight:800; font-size:16px; border-radius:14px;
               text-decoration:none; transition:transform 0.15s,box-shadow 0.15s; }}
  .btn-chat:hover {{ transform:translateY(-2px); box-shadow:0 8px 24px rgba(201,168,76,0.3); }}
  .btn-booking {{ flex:1; min-width:180px; display:flex; align-items:center; justify-content:center; gap:8px;
                  padding:16px 24px; background:transparent; color:var(--gold);
                  border:2px solid var(--gold); font-weight:700; font-size:15px; border-radius:14px;
                  text-decoration:none; transition:all 0.15s; }}
  .btn-booking:hover {{ background:rgba(201,168,76,0.1); }}

  /* SECTION */
  .section {{ margin-bottom:32px; }}
  .section-title {{ font-size:11px; letter-spacing:2px; text-transform:uppercase;
                    color:var(--gold); margin-bottom:16px; padding-bottom:10px;
                    border-bottom:1px solid rgba(201,168,76,0.15); }}
  .description {{ font-size:15px; color:var(--text2); line-height:1.7; white-space:pre-line; }}

  /* AMENITIES */
  .pills {{ display:flex; flex-wrap:wrap; gap:8px; }}
  .pill {{ background:var(--bg2); border:1px solid rgba(201,168,76,0.2); border-radius:20px;
           padding:6px 14px; font-size:13px; color:var(--text); }}

  /* AI WIDGET */
  .ai-widget {{ background:var(--bg2); border:1px solid rgba(201,168,76,0.2); border-radius:16px;
                padding:20px 24px; display:flex; align-items:center; gap:16px; }}
  .ai-icon {{ width:48px; height:48px; border-radius:50%; background:linear-gradient(135deg,var(--gold),var(--gold2));
              display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0; }}
  .ai-text h3 {{ font-size:15px; font-weight:700; margin-bottom:4px; }}
  .ai-text p {{ font-size:13px; color:var(--text2); line-height:1.5; }}

  /* REVIEWS */
  .reviews-grid {{ display:flex; flex-wrap:wrap; gap:10px; }}
  .review-card {{ background:var(--bg2); border:1px solid rgba(255,255,255,0.06); border-radius:12px;
                  padding:14px 16px; flex:1; min-width:120px; max-width:160px; text-align:center; }}
  .review-stars {{ color:var(--gold); font-size:16px; letter-spacing:2px; margin-bottom:4px; }}
  .review-date {{ font-size:11px; color:var(--text2); }}

  /* NO REVIEWS */
  .no-reviews {{ color:var(--text2); font-size:14px; text-align:center; padding:20px; }}

  /* FOOTER */
  footer {{ text-align:center; padding:20px; font-size:12px; color:var(--text2);
            border-top:1px solid rgba(255,255,255,0.05); }}
  footer a {{ color:var(--gold); text-decoration:none; }}

  @media (max-width:480px) {{
    .hero {{ height:260px; }}
    .hotel-name {{ font-size:24px; }}
    .btn-chat, .btn-booking {{ font-size:14px; padding:14px 18px; }}
  }}
</style>
</head>
<body>

<!-- HERO -->
<div class="hero">
  {hero_overlay}
  <div class="hero-content">
    <div class="hotel-badge">🏨 SmartStay</div>
    <h1 class="hotel-name">{name}</h1>
    <div class="rating-row">
      <span class="stars">{stars_html(avg_rating or 0)}</span>
      <span class="rating-num">{rating_display}</span>
      <span class="rating-cnt">({rating_count} отзывов)</span>
    </div>
  </div>
</div>

<div class="content">

  <!-- CTA BUTTONS -->
  <div class="actions" style="margin-top:24px">
    <a href="/hotel/{slug}" class="btn-chat">💬 Открыть чат с консьержем</a>
    {booking_btn}
  </div>

  <!-- AI CONCIERGE WIDGET -->
  <div class="section">
    <div class="ai-widget">
      <div class="ai-icon">🤖</div>
      <div class="ai-text">
        <h3>{ai_name} — ваш AI-консьерж</h3>
        <p>Доступен 24/7 на вашем языке. Отвечает на вопросы, принимает заявки и помогает с любыми запросами.</p>
      </div>
    </div>
  </div>

  {"<!-- DESCRIPTION --><div class='section'><div class='section-title'>Об отеле</div><div class='description'>" + page_desc + "</div></div>" if page_desc else ""}

  {"<!-- AMENITIES --><div class='section'><div class='section-title'>Удобства</div><div class='pills'>" + amenity_pills + "</div></div>" if amenities else ""}

  <!-- REVIEWS -->
  <div class="section">
    <div class="section-title">Отзывы гостей</div>
    {"<div class='reviews-grid'>" + reviews_html + "</div>" if recent_reviews else "<div class='no-reviews'>Отзывов пока нет — будьте первым! ⭐</div>"}
  </div>

</div>

<footer>
  Powered by <a href="https://smartstay.ai" target="_blank">SmartStay AI</a>
</footer>

</body>
</html>"""
