import sqlite3
from datetime import datetime
from config import DATABASE_PATH, URGENT_KEYWORDS

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE,
            name TEXT,
            password TEXT,
            info TEXT,
            telegram_token TEXT DEFAULT '',
            telegram_chat_id TEXT DEFAULT '',
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_slug TEXT,
            room TEXT,
            role TEXT,
            message TEXT,
            created_at TEXT,
            priority TEXT DEFAULT 'normal',
            is_read INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def get_priority(message):
    msg_lower = message.lower()
    for keyword in URGENT_KEYWORDS:
        if keyword in msg_lower:
            return "urgent"
    return "normal"

def save_message(room, role, message):
    priority = get_priority(message) if role == "user" else "normal"
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute(
        "INSERT INTO messages (room, role, message, created_at, priority, is_read) VALUES (?, ?, ?, ?, ?, ?)",
        (room, role, message, datetime.now().strftime("%Y-%m-%d %H:%M"), priority, 0)
    )
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        """SELECT room, role, message, created_at, priority, is_read 
        FROM messages ORDER BY 
        CASE priority WHEN 'urgent' THEN 0 ELSE 1 END,
        id DESC LIMIT 100"""
    ).fetchall()
    conn.close()
    return rows

def create_hotel(slug, name, password, info, telegram_token="", telegram_chat_id=""):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute(
        "INSERT INTO hotels (slug, name, password, info, telegram_token, telegram_chat_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (slug, name, password, info, telegram_token, telegram_chat_id, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()

def get_hotel(slug):
    conn = sqlite3.connect(DATABASE_PATH)
    row = conn.execute(
        "SELECT slug, name, password, info, telegram_token, telegram_chat_id FROM hotels WHERE slug=?", (slug,)
    ).fetchone()
    conn.close()
    if row:
        return {
            "slug": row[0], "name": row[1], "password": row[2],
            "info": row[3], "telegram_token": row[4], "telegram_chat_id": row[5]
        }
    return None

def get_all_hotels():
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        "SELECT slug, name, created_at FROM hotels ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [{"slug": r[0], "name": r[1], "created_at": r[2]} for r in rows]

def get_hotel_messages(slug):
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        """SELECT room, role, message, created_at, priority, is_read 
        FROM messages WHERE hotel_slug=?
        ORDER BY CASE priority WHEN 'urgent' THEN 0 ELSE 1 END, id DESC LIMIT 100""",
        (slug,)
    ).fetchall()
    conn.close()
    return rows

def save_hotel_message(slug, room, role, message):
    priority = get_priority(message) if role == "user" else "normal"
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute(
        "INSERT INTO messages (hotel_slug, room, role, message, created_at, priority, is_read) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (slug, room, role, message, datetime.now().strftime("%Y-%m-%d %H:%M"), priority, 0)
    )
    conn.commit()
    conn.close()
    return priority

def mark_hotel_read(slug):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("UPDATE messages SET is_read=1 WHERE hotel_slug=?", (slug,))
    conn.commit()
    conn.close()

def mark_all_read():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("UPDATE messages SET is_read=1")
    conn.commit()
    conn.close()

def update_hotel(slug, name, info, password=None, telegram_token=None, telegram_chat_id=None):
    conn = sqlite3.connect(DATABASE_PATH)
    if password and telegram_token is not None:
        conn.execute(
            "UPDATE hotels SET name=?, info=?, password=?, telegram_token=?, telegram_chat_id=? WHERE slug=?",
            (name, info, password, telegram_token, telegram_chat_id, slug)
        )
    elif password:
        conn.execute(
            "UPDATE hotels SET name=?, info=?, password=? WHERE slug=?",
            (name, info, password, slug)
        )
    elif telegram_token is not None:
        conn.execute(
            "UPDATE hotels SET name=?, info=?, telegram_token=?, telegram_chat_id=? WHERE slug=?",
            (name, info, telegram_token, telegram_chat_id, slug)
        )
    else:
        conn.execute(
            "UPDATE hotels SET name=?, info=? WHERE slug=?",
            (name, info, slug)
        )
    conn.commit()
    conn.close()

def get_hotel_stats(slug):
    conn = sqlite3.connect(DATABASE_PATH)
    total = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE hotel_slug=?", (slug,)
    ).fetchone()[0]
    urgent = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE hotel_slug=? AND priority='urgent'", (slug,)
    ).fetchone()[0]
    unread = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE hotel_slug=? AND is_read=0 AND role='user'", (slug,)
    ).fetchone()[0]
    today = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE hotel_slug=? AND created_at LIKE ?",
        (slug, datetime.now().strftime("%Y-%m-%d") + "%")
    ).fetchone()[0]
    conn.close()
    return {"total": total, "urgent": urgent, "unread": unread, "today": today}

def delete_hotel(slug):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("DELETE FROM hotels WHERE slug=?", (slug,))
    conn.execute("DELETE FROM messages WHERE hotel_slug=?", (slug,))
    conn.commit()
    conn.close()