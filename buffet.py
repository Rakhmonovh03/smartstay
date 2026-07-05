"""
Smart Buffet — AI-анализ шведского стола.

Главная функция:
  analyze_buffet_photo(image_base64, media_type)
    → отправляет фото в Claude Vision (claude-sonnet-4-5)
    → возвращает JSON со списком блюд и уровнем заполнения

Вспомогательные функции для базы данных:
  save_buffet_scan     — сохранить результат
  get_buffet_latest    — последний скан отеля
  get_buffet_history   — история за N дней
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Optional

from anthropic import Anthropic
from config import DATABASE_PATH

_client = Anthropic()   # использует ANTHROPIC_API_KEY из окружения

# --------------------------------------------------------------------------- #
#  AI-анализ                                                                   #
# --------------------------------------------------------------------------- #

MAX_PHOTOS = 6   # максимум фото за один скан

_LANG_NAMES = {"en": "English", "ru": "Russian", "tr": "Turkish", "uz": "Uzbek"}


def analyze_buffet_photos(images: list, lang: str = "en") -> dict:
    """
    Отправляет одно или несколько фото шведского стола в Claude Vision
    одним запросом.

    images — список кортежей (image_base64, media_type), максимум MAX_PHOTOS.
             Фото считаются разными ракурсами / секциями ОДНОГО буфета:
             AI объединяет блюда со всех снимков в один список без дублей.

    Возвращает словарь вида:
    {
      "dishes": [
        {"name": "Название блюда", "fill_percent": 75, "status": "good"},
        ...
      ],
      "summary": "Общий комментарий о состоянии буфета"
    }

    fill_percent — от 0 (пусто) до 100 (полное).
    status       — "empty" (0-20%), "low" (21-50%), "good" (51-80%), "full" (81-100%).
    """
    images = images[:MAX_PHOTOS]
    n = len(images)
    lang_name = _LANG_NAMES.get(lang, "English")

    prompt = (
        "You are a hotel buffet monitoring system. "
        + (f"Analyze these {n} photos, which show different angles/sections of the SAME hotel buffet. "
           if n > 1 else
           "Analyze this photo of a hotel buffet table. ")
        + "Return a JSON object with EXACTLY this structure (no markdown, no extra text):\n\n"
        "{\n"
        '  "dishes": [\n'
        '    {"name": "Dish name", "fill_percent": 75, "status": "good"},\n'
        "    ...\n"
        "  ],\n"
        '  "summary": "Brief overall buffet status"\n'
        "}\n\n"
        "Rules:\n"
        "- List every visible dish / food container / tray across ALL photos.\n"
        "- If the same dish appears in several photos, list it ONCE (use the clearest view for the estimate).\n"
        "- fill_percent: integer 0–100 (0=completely empty, 100=completely full).\n"
        "- status must be one of: empty (0-20), low (21-50), good (51-80), full (81-100).\n"
        f"- Write dish names and the summary in {lang_name}. Keep names short and descriptive.\n"
        "- Return ONLY the JSON object."
    )

    content = [
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": mt or "image/jpeg",
                "data": b64,
            },
        }
        for b64, mt in images
    ]
    content.append({"type": "text", "text": prompt})

    response = _client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1536,
        messages=[{"role": "user", "content": content}],
    )

    text = response.content[0].text.strip()

    # Убираем markdown-обёртку ```json ... ``` если Claude добавил её
    if text.startswith("```"):
        lines = text.splitlines()
        # убрать первую и последнюю строки (``` и ```)
        inner = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(inner).strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        # Если Claude вернул что-то непонятное — возвращаем пустой результат
        result = {"dishes": [], "summary": text[:200]}

    # Нормализуем статус на случай если Claude вернул не то слово
    for d in result.get("dishes", []):
        # fill_percent may arrive as 75, "75", "75%", or garbage — parse defensively.
        raw = str(d.get("fill_percent", 0))
        digits = "".join(ch for ch in raw if ch.isdigit())
        pct = int(digits) if digits else 0
        pct = max(0, min(pct, 100))
        d["fill_percent"] = pct
        if pct <= 20:
            d["status"] = "empty"
        elif pct <= 50:
            d["status"] = "low"
        elif pct <= 80:
            d["status"] = "good"
        else:
            d["status"] = "full"

    return result


def analyze_buffet_photo(image_base64: str, media_type: str = "image/jpeg", lang: str = "en") -> dict:
    """Обратная совместимость: анализ одного фото."""
    return analyze_buffet_photos([(image_base64, media_type)], lang)


# --------------------------------------------------------------------------- #
#  База данных                                                                 #
# --------------------------------------------------------------------------- #

def save_buffet_scan(hotel_slug: str, data: dict) -> int:
    """
    Сохраняет результат анализа в таблицу buffet_scans.
    Возвращает id новой записи.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    # Local time — consistent with the rest of the app (messages, guests, etc.)
    cur = conn.execute(
        "INSERT INTO buffet_scans (hotel_slug, scan_time, dishes_json) VALUES (?, ?, ?)",
        (hotel_slug, datetime.now().isoformat(), json.dumps(data, ensure_ascii=False)),
    )
    row_id = cur.lastrowid
    conn.commit()
    conn.close()
    return row_id


def get_buffet_latest(hotel_slug: str) -> Optional[dict]:
    """
    Возвращает самый последний скан отеля или None если сканов нет.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM buffet_scans WHERE hotel_slug=? ORDER BY id DESC LIMIT 1",
        (hotel_slug,),
    ).fetchone()
    conn.close()
    if not row:
        return None
    r = dict(row)
    r["dishes_data"] = json.loads(r["dishes_json"])
    return r


def get_buffet_history(hotel_slug: str, days: int = 7) -> list:
    """
    Возвращает все сканы за последние N дней (по умолчанию 7),
    отсортированные от новых к старым.
    """
    since = (datetime.now() - timedelta(days=days)).isoformat()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM buffet_scans "
        "WHERE hotel_slug=? AND scan_time >= ? "
        "ORDER BY id DESC",
        (hotel_slug, since),
    ).fetchall()
    conn.close()
    result = []
    for row in rows:
        r = dict(row)
        r["dishes_data"] = json.loads(r["dishes_json"])
        result.append(r)
    return result
