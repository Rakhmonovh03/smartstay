import sqlite3
import bcrypt
from datetime import datetime
from config import DATABASE_PATH, URGENT_KEYWORDS


def hash_password(password: str) -> str:
    """Превращает пароль в защищённый хеш"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """
    Проверяет пароль. Если хеш bcrypt — сравниваем через bcrypt.
    Если старый незахешированный — сравниваем напрямую (и немедленно возвращаем True,
    чтобы caller успел обновить хеш в БД через migrate_password_if_needed).
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        # Plaintext legacy password — только равенство, без timing-safe bypass
        return password == hashed


def is_password_hashed(hashed: str) -> bool:
    """Возвращает True если строка — bcrypt-хеш."""
    return hashed.startswith("$2b$") or hashed.startswith("$2a$")


def migrate_password_if_needed(slug: str, password: str, current_hash: str) -> None:
    """
    Если пароль хранится в открытом виде — хешируем и обновляем БД при первом успешном входе.
    Вызывать только после подтверждённой верификации.
    """
    if not is_password_hashed(current_hash):
        new_hash = hash_password(password)
        conn = sqlite3.connect(DATABASE_PATH)
        conn.execute("UPDATE hotels SET password=? WHERE slug=?", (new_hash, slug))
        conn.commit()
        conn.close()
        print(f"[security] Migrated plaintext password to bcrypt for hotel '{slug}'")


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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_slug TEXT,
            room TEXT,
            rating INTEGER,
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_slug TEXT NOT NULL,
            room TEXT DEFAULT '',
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            passport TEXT NOT NULL,
            nationality TEXT DEFAULT '',
            check_in TEXT NOT NULL,
            check_out TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_hotel_slug ON messages(hotel_slug)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_priority ON messages(priority)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_is_read ON messages(is_read)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ratings_hotel_slug ON ratings(hotel_slug)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_guests_hotel_slug ON guests(hotel_slug)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_guests_status ON guests(status)")

    # Internal staff notes per room (not visible to guests)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS room_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_slug TEXT NOT NULL,
            room TEXT NOT NULL,
            note TEXT NOT NULL,
            author TEXT DEFAULT 'Персонал',
            created_at TEXT NOT NULL
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_room_notes ON room_notes(hotel_slug, room)"
    )

    # Guest service requests (room service, maintenance, housekeeping, etc.)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_slug TEXT NOT NULL,
            room TEXT NOT NULL,
            guest_name TEXT DEFAULT '',
            category TEXT DEFAULT 'general',
            message TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL,
            resolved_at TEXT DEFAULT ''
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_requests_hotel_slug ON requests(hotel_slug)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_requests_status ON requests(status)"
    )

    # Staff accounts (multiple logins per hotel with roles)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_slug TEXT NOT NULL,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'receptionist',
            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_staff_hotel ON staff(hotel_slug)"
    )
    conn.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_staff_slug_user ON staff(hotel_slug, username)"
    )

    # Hotel owners — one login manages multiple hotels
    conn.execute("""
        CREATE TABLE IF NOT EXISTS owners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_owners_email ON owners(email)"
    )
    conn.execute("""
        CREATE TABLE IF NOT EXISTS hotel_owners (
            owner_id INTEGER NOT NULL,
            hotel_slug TEXT NOT NULL,
            PRIMARY KEY (owner_id, hotel_slug)
        )
    """)

    # Maps Telegram message_id → hotel room (for 2-way replies)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS telegram_msg_map (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_slug TEXT NOT NULL,
            room TEXT NOT NULL,
            telegram_msg_id INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_tgmap ON telegram_msg_map(hotel_slug, telegram_msg_id)"
    )

    # Safe migrations — add new columns to existing tables without breaking prod
    _migrations = [
        ("hotels", "plan",        "TEXT DEFAULT 'trial'"),
        ("hotels", "room_count",  "INTEGER DEFAULT 30"),
        ("hotels", "room_start",  "INTEGER DEFAULT 101"),
        ("hotels", "booking_url", "TEXT DEFAULT ''"),
        ("hotels", "ai_name",     "TEXT DEFAULT 'AI Asistan'"),
        # SMTP email notifications
        ("hotels", "smtp_host",   "TEXT DEFAULT ''"),
        ("hotels", "smtp_port",   "INTEGER DEFAULT 587"),
        ("hotels", "smtp_user",   "TEXT DEFAULT ''"),
        ("hotels", "smtp_pass",   "TEXT DEFAULT ''"),
        ("hotels", "smtp_from",   "TEXT DEFAULT ''"),
        ("hotels", "notify_email",          "TEXT DEFAULT ''"),
        # Stripe billing
        ("hotels", "stripe_customer_id",    "TEXT DEFAULT ''"),
        ("hotels", "stripe_subscription_id","TEXT DEFAULT ''"),
        ("hotels", "stripe_status",         "TEXT DEFAULT ''"),
        ("guests", "reviewed",              "INTEGER DEFAULT 0"),
        # Multilanguage
        ("hotels", "default_language",      "TEXT DEFAULT 'auto'"),
        ("hotels", "supported_languages",   "TEXT DEFAULT 'en,ru,tr,ar,de,fr'"),
        # Public page
        ("hotels", "photo_url",         "TEXT DEFAULT ''"),
        ("hotels", "page_description",  "TEXT DEFAULT ''"),
        ("hotels", "amenities",         "TEXT DEFAULT ''"),
        # Floor-based room numbering
        ("hotels", "rooms_per_floor",   "INTEGER DEFAULT 0"),
    ]
    for table, col, definition in _migrations:
        try:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {definition}")
        except sqlite3.OperationalError:
            pass  # column already exists

    # Hotel services catalog (room service, spa, transport, etc.)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_slug TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            category TEXT DEFAULT 'general',
            price REAL DEFAULT 0,
            currency TEXT DEFAULT 'USD',
            icon TEXT DEFAULT '🛎️',
            is_active INTEGER DEFAULT 1,
            sort_order INTEGER DEFAULT 0
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_services_hotel ON services(hotel_slug)"
    )

    # Buffet scans — AI-анализ фото шведского стола
    conn.execute("""
        CREATE TABLE IF NOT EXISTS buffet_scans (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_slug TEXT NOT NULL,
            scan_time  TEXT NOT NULL,
            dishes_json TEXT NOT NULL DEFAULT '{}'
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_buffet_hotel ON buffet_scans(hotel_slug, scan_time)"
    )

    # Internal staff-to-staff chat by channel/department
    conn.execute("""
        CREATE TABLE IF NOT EXISTS staff_chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_slug TEXT NOT NULL,
            channel TEXT NOT NULL DEFAULT 'general',
            sender TEXT NOT NULL,
            role_label TEXT DEFAULT '',
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_staff_chat_hotel ON staff_chat(hotel_slug, channel, id)"
    )

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
        FROM messages WHERE hotel_slug IS NULL
        ORDER BY CASE priority WHEN 'urgent' THEN 0 ELSE 1 END,
        id DESC LIMIT 100"""
    ).fetchall()
    conn.close()
    return rows


def generate_room_numbers(room_count: int, room_start: int, rooms_per_floor: int = 0) -> list:
    """Generate room number list.
    If rooms_per_floor > 0 and room_start >= 100: floor-based numbering.
    E.g. room_start=101, rooms_per_floor=4, room_count=12 →
         [101,102,103,104, 201,202,203,204, 301,302,303,304]
    Otherwise sequential: [101,102,103,...].
    """
    if rooms_per_floor > 0 and room_start >= 100:
        start_floor = room_start // 100        # e.g. 101 → 1
        rooms = []
        floor = start_floor
        pos = 1  # always start from room 1 in each floor
        while len(rooms) < room_count:
            rooms.append(str(floor * 100 + pos))
            pos += 1
            if pos > rooms_per_floor:
                pos = 1
                floor += 1
        return rooms
    else:
        return [str(room_start + i) for i in range(room_count)]


def create_hotel(slug, name, password, info, telegram_token="", telegram_chat_id="",
                 plan="trial", room_count=30, room_start=101, booking_url="",
                 rooms_per_floor=0):
    hashed = hash_password(password)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute(
        """INSERT INTO hotels
           (slug, name, password, info, telegram_token, telegram_chat_id,
            created_at, plan, room_count, room_start, booking_url, rooms_per_floor)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (slug, name, hashed, info, telegram_token, telegram_chat_id,
         datetime.now().strftime("%Y-%m-%d %H:%M"), plan, room_count, room_start, booking_url,
         rooms_per_floor)
    )
    conn.commit()
    conn.close()


def get_hotel(slug):
    conn = sqlite3.connect(DATABASE_PATH)
    row = conn.execute(
        """SELECT slug, name, password, info, telegram_token, telegram_chat_id,
                  plan, room_count, room_start, booking_url, ai_name,
                  smtp_host, smtp_port, smtp_user, smtp_pass, smtp_from, notify_email,
                  stripe_customer_id, stripe_subscription_id, stripe_status,
                  default_language, supported_languages,
                  photo_url, page_description, amenities, rooms_per_floor
           FROM hotels WHERE slug=?""", (slug,)
    ).fetchone()
    conn.close()
    if row:
        return {
            "slug": row[0], "name": row[1], "password": row[2],
            "info": row[3], "telegram_token": row[4], "telegram_chat_id": row[5],
            "plan": row[6] or "trial",
            "room_count": row[7] or 30,
            "room_start": row[8] or 101,
            "booking_url": row[9] or "",
            "ai_name": row[10] or "AI Asistan",
            "smtp_host": row[11] or "",
            "smtp_port": row[12] or 587,
            "smtp_user": row[13] or "",
            "smtp_pass": row[14] or "",
            "smtp_from": row[15] or "",
            "notify_email": row[16] or "",
            "stripe_customer_id": row[17] or "",
            "stripe_subscription_id": row[18] or "",
            "stripe_status": row[19] or "",
            "default_language": row[20] or "auto",
            "supported_languages": row[21] or "en,ru,tr,ar,de,fr",
            "photo_url": row[22] or "",
            "page_description": row[23] or "",
            "amenities": row[24] or "",
            "rooms_per_floor": row[25] or 0,
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


def update_hotel(slug, name, info, password=None, telegram_token=None,
                 telegram_chat_id=None, booking_url=None, ai_name=None,
                 smtp_host=None, smtp_port=None, smtp_user=None, smtp_pass=None,
                 smtp_from=None, notify_email=None,
                 default_language=None, supported_languages=None,
                 photo_url=None, page_description=None, amenities=None,
                 rooms_per_floor=None):
    conn = sqlite3.connect(DATABASE_PATH)
    # Build SET clause dynamically to avoid overwriting unrelated fields
    fields = ["name=?", "info=?"]
    values = [name, info]
    if password:
        fields.append("password=?")
        values.append(hash_password(password))
    if telegram_token is not None:
        fields.append("telegram_token=?")
        fields.append("telegram_chat_id=?")
        values.extend([telegram_token, telegram_chat_id or ""])
    if booking_url is not None:
        fields.append("booking_url=?")
        values.append(booking_url)
    if ai_name is not None:
        fields.append("ai_name=?")
        values.append(ai_name.strip() or "AI Asistan")
    if smtp_host is not None:
        fields.append("smtp_host=?")
        values.append(smtp_host.strip())
    if smtp_port is not None:
        fields.append("smtp_port=?")
        values.append(int(smtp_port) if smtp_port else 587)
    if smtp_user is not None:
        fields.append("smtp_user=?")
        values.append(smtp_user.strip())
    if smtp_pass is not None:
        fields.append("smtp_pass=?")
        values.append(smtp_pass)
    if smtp_from is not None:
        fields.append("smtp_from=?")
        values.append(smtp_from.strip())
    if notify_email is not None:
        fields.append("notify_email=?")
        values.append(notify_email.strip())
    if default_language is not None:
        fields.append("default_language=?")
        values.append(default_language.strip() or "auto")
    if supported_languages is not None:
        fields.append("supported_languages=?")
        values.append(supported_languages.strip() or "en,ru,tr,ar,de,fr")
    if photo_url is not None:
        fields.append("photo_url=?")
        values.append(photo_url.strip())
    if page_description is not None:
        fields.append("page_description=?")
        values.append(page_description.strip())
    if amenities is not None:
        fields.append("amenities=?")
        values.append(amenities.strip())
    if rooms_per_floor is not None:
        fields.append("rooms_per_floor=?")
        values.append(max(0, min(int(rooms_per_floor), 100)))
    values.append(slug)
    conn.execute(f"UPDATE hotels SET {', '.join(fields)} WHERE slug=?", values)
    conn.commit()
    conn.close()


def update_hotel_stripe(slug: str, stripe_customer_id: str = None,
                        stripe_subscription_id: str = None,
                        stripe_status: str = None, plan: str = None):
    """Update Stripe billing fields for a hotel (partial update — only non-None args)."""
    conn = sqlite3.connect(DATABASE_PATH)
    fields, values = [], []
    if stripe_customer_id is not None:
        fields.append("stripe_customer_id=?"); values.append(stripe_customer_id)
    if stripe_subscription_id is not None:
        fields.append("stripe_subscription_id=?"); values.append(stripe_subscription_id)
    if stripe_status is not None:
        fields.append("stripe_status=?"); values.append(stripe_status)
    if plan is not None:
        fields.append("plan=?"); values.append(plan)
    if fields:
        values.append(slug)
        conn.execute(f"UPDATE hotels SET {', '.join(fields)} WHERE slug=?", values)
        conn.commit()
    conn.close()


def get_hotel_by_stripe_customer(customer_id: str):
    """Find hotel by Stripe customer ID (used in webhook handler)."""
    conn = sqlite3.connect(DATABASE_PATH)
    row = conn.execute(
        "SELECT slug FROM hotels WHERE stripe_customer_id=?", (customer_id,)
    ).fetchone()
    conn.close()
    return row[0] if row else None


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
    conn.execute("DELETE FROM ratings WHERE hotel_slug=?", (slug,))
    conn.execute("DELETE FROM guests WHERE hotel_slug=?", (slug,))
    conn.execute("DELETE FROM requests WHERE hotel_slug=?", (slug,))
    conn.execute("DELETE FROM room_notes WHERE hotel_slug=?", (slug,))
    conn.execute("DELETE FROM staff WHERE hotel_slug=?", (slug,))
    conn.execute("DELETE FROM services WHERE hotel_slug=?", (slug,))
    conn.execute("DELETE FROM staff_chat WHERE hotel_slug=?", (slug,))
    conn.execute("DELETE FROM telegram_msg_map WHERE hotel_slug=?", (slug,))
    conn.execute("DELETE FROM hotel_owners WHERE hotel_slug=?", (slug,))
    conn.commit()
    conn.close()


def get_room_messages(slug, room, limit=200):
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        """SELECT id, role, message, created_at, priority
        FROM messages WHERE hotel_slug=? AND room=?
        ORDER BY id ASC LIMIT ?""",
        (slug, room, limit)
    ).fetchall()
    conn.close()
    return [{"id": r[0], "role": r[1], "message": r[2], "created_at": r[3], "priority": r[4]} for r in rows]


def get_new_messages(slug, room, since_id):
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        """SELECT id, role, message, created_at
        FROM messages WHERE hotel_slug=? AND room=? AND id>? AND role IN ('bot','staff')
        ORDER BY id ASC""",
        (slug, room, since_id)
    ).fetchall()
    conn.close()
    return [{"id": r[0], "role": r[1], "message": r[2], "created_at": r[3]} for r in rows]


def save_staff_message(slug, room, message):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute(
        "INSERT INTO messages (hotel_slug, room, role, message, created_at, priority, is_read) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (slug, room, 'staff', message, datetime.now().strftime("%Y-%m-%d %H:%M"), 'normal', 1)
    )
    conn.commit()
    conn.close()


def save_rating(slug, room, rating_value):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute(
        "INSERT INTO ratings (hotel_slug, room, rating, created_at) VALUES (?, ?, ?, ?)",
        (slug, room, rating_value, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()


def get_monthly_message_count(slug: str) -> int:
    """Returns the number of guest (user-role) messages for this hotel in the current calendar month."""
    conn = sqlite3.connect(DATABASE_PATH)
    count = conn.execute(
        """SELECT COUNT(*) FROM messages
           WHERE hotel_slug=? AND role='user'
           AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')""",
        (slug,)
    ).fetchone()[0]
    conn.close()
    return count


def save_guest(hotel_slug, room, first_name, last_name, passport,
               nationality, check_in, check_out) -> int:
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        """INSERT INTO guests
           (hotel_slug, room, first_name, last_name, passport, nationality,
            check_in, check_out, status, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)""",
        (hotel_slug, room, first_name, last_name, passport, nationality,
         check_in, check_out, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    guest_id = cur.lastrowid
    conn.commit()
    conn.close()
    return guest_id


def get_guests(hotel_slug: str) -> list:
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        """SELECT id, room, first_name, last_name, passport, nationality,
                  check_in, check_out, status, notes, created_at
           FROM guests WHERE hotel_slug=?
           ORDER BY id DESC""",
        (hotel_slug,)
    ).fetchall()
    conn.close()
    return [
        {
            "id": r[0], "room": r[1], "first_name": r[2], "last_name": r[3],
            "passport": r[4], "nationality": r[5], "check_in": r[6],
            "check_out": r[7], "status": r[8], "notes": r[9], "created_at": r[10]
        }
        for r in rows
    ]


def update_guest_room(guest_id: int, room: str) -> None:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("UPDATE guests SET room=? WHERE id=?", (room, guest_id))
    conn.commit()
    conn.close()


def update_guest_status(guest_id: int, status: str, notes: str = "") -> None:
    conn = sqlite3.connect(DATABASE_PATH)
    if notes:
        conn.execute("UPDATE guests SET status=?, notes=? WHERE id=?",
                     (status, notes, guest_id))
    else:
        conn.execute("UPDATE guests SET status=? WHERE id=?", (status, guest_id))
    conn.commit()
    conn.close()


def get_active_guests_count(hotel_slug: str) -> int:
    conn = sqlite3.connect(DATABASE_PATH)
    count = conn.execute(
        "SELECT COUNT(*) FROM guests WHERE hotel_slug=? AND status='checked_in'",
        (hotel_slug,)
    ).fetchone()[0]
    conn.close()
    return count


def get_guest_by_room(hotel_slug: str, room: str) -> dict | None:
    """Returns the active (checked_in) guest in a room, or None."""
    conn = sqlite3.connect(DATABASE_PATH)
    row = conn.execute(
        """SELECT id, first_name, last_name, check_in, check_out, reviewed
           FROM guests
           WHERE hotel_slug=? AND room=? AND status='checked_in'
           ORDER BY id DESC LIMIT 1""",
        (hotel_slug, room)
    ).fetchone()
    conn.close()
    if row:
        return {
            "id": row[0], "first_name": row[1], "last_name": row[2],
            "check_in": row[3], "check_out": row[4], "reviewed": row[5]
        }
    return None


def mark_guest_reviewed(guest_id: int) -> None:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("UPDATE guests SET reviewed=1 WHERE id=?", (guest_id,))
    conn.commit()
    conn.close()


def get_recent_ratings(hotel_slug: str, limit: int = 30) -> list:
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        """SELECT r.id, r.room, r.rating, r.created_at,
                  g.first_name, g.last_name
           FROM ratings r
           LEFT JOIN guests g ON g.hotel_slug=r.hotel_slug AND g.room=r.room
               AND g.status IN ('checked_in','checked_out')
           WHERE r.hotel_slug=?
           ORDER BY r.id DESC LIMIT ?""",
        (hotel_slug, limit)
    ).fetchall()
    conn.close()
    return [
        {
            "id": r[0], "room": r[1], "rating": r[2], "created_at": r[3],
            "guest_name": f"{r[4] or ''} {r[5] or ''}".strip() or None
        }
        for r in rows
    ]


def get_overdue_guests(hotel_slug: str) -> list:
    """Return checked_in guests whose check_out date is in the past."""
    conn = sqlite3.connect(DATABASE_PATH)
    today = datetime.now().strftime("%Y-%m-%d")
    rows = conn.execute(
        """SELECT id, first_name, last_name, room, check_out
           FROM guests WHERE hotel_slug=? AND status='checked_in' AND check_out < ?""",
        (hotel_slug, today)
    ).fetchall()
    conn.close()
    return [
        {"id": r[0], "first_name": r[1], "last_name": r[2], "room": r[3], "check_out": r[4]}
        for r in rows
    ]


def auto_checkout_overdue(hotel_slug: str) -> int:
    """
    Mark all checked_in guests with a past check_out date as checked_out.
    Returns the number of guests processed.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    today = datetime.now().strftime("%Y-%m-%d")
    cur = conn.execute(
        """UPDATE guests SET status='checked_out'
           WHERE hotel_slug=? AND status='checked_in' AND check_out < ?""",
        (hotel_slug, today)
    )
    count = cur.rowcount
    conn.commit()
    conn.close()
    return count


def get_daily_digest_data(hotel_slug: str) -> dict:
    """Return today's summary data for the daily Telegram digest."""
    conn = sqlite3.connect(DATABASE_PATH)
    today = datetime.now().strftime("%Y-%m-%d")

    active = conn.execute(
        "SELECT COUNT(*) FROM guests WHERE hotel_slug=? AND status='checked_in'",
        (hotel_slug,)
    ).fetchone()[0]

    checkins_today = conn.execute(
        "SELECT COUNT(*) FROM guests WHERE hotel_slug=? AND check_in=?",
        (hotel_slug, today)
    ).fetchone()[0]

    checkouts_today = conn.execute(
        "SELECT first_name, last_name, room FROM guests "
        "WHERE hotel_slug=? AND check_out=? AND status='checked_in'",
        (hotel_slug, today)
    ).fetchall()

    unread = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE hotel_slug=? AND role='user' AND is_read=0",
        (hotel_slug,)
    ).fetchone()[0]

    avg_row = conn.execute(
        "SELECT ROUND(AVG(rating),1), COUNT(*) FROM ratings WHERE hotel_slug=?",
        (hotel_slug,)
    ).fetchone()

    conn.close()
    return {
        "active_guests": active,
        "checkins_today": checkins_today,
        "checkouts_today": [
            {"name": f"{r[0]} {r[1]}", "room": r[2]} for r in checkouts_today
        ],
        "unread_messages": unread,
        "avg_rating": avg_row[0],
        "rating_count": avg_row[1],
    }


def save_telegram_msg_id(hotel_slug: str, room: str, telegram_msg_id: int) -> None:
    """Store the mapping Telegram message_id → room for 2-way reply routing."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute(
        "INSERT INTO telegram_msg_map (hotel_slug, room, telegram_msg_id, created_at) VALUES (?, ?, ?, ?)",
        (hotel_slug, room, telegram_msg_id, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()


def get_room_by_telegram_msg_id(hotel_slug: str, telegram_msg_id: int) -> str | None:
    """Return the room number for a given Telegram message_id, or None."""
    conn = sqlite3.connect(DATABASE_PATH)
    row = conn.execute(
        "SELECT room FROM telegram_msg_map WHERE hotel_slug=? AND telegram_msg_id=? LIMIT 1",
        (hotel_slug, telegram_msg_id)
    ).fetchone()
    conn.close()
    return row[0] if row else None


# ─── Guest Request Tracker ──────────────────────────────────────────────────

# Keywords that signal a service request, grouped by category.
_REQUEST_KEYWORDS = {
    "room_service": [
        "yemek", "içecek", "su", "çay", "kahve", "meyve", "atıştırma", "menü",
        "food", "water", "tea", "coffee", "drink", "snack", "menu", "room service",
        "еда", "вода", "чай", "кофе", "еду", "напиток", "обед", "ужин", "завтрак",
    ],
    "maintenance": [
        "arızalı", "bozuk", "çalışmıyor", "tamir", "kırık", "akar", "musluk",
        "broken", "not working", "fix", "repair", "leak", "faucet", "toilet",
        "сломан", "не работает", "поломка", "починить", "течёт", "кран",
    ],
    "housekeeping": [
        "temizlik", "temizle", "havlu", "çarşaf", "yatak", "süpürge",
        "clean", "cleaning", "towel", "sheets", "linen", "housekeeping",
        "уборка", "убрать", "полотенце", "простыня", "постель",
    ],
}


def detect_request_category(message: str) -> str | None:
    """
    Returns the request category if the message looks like a service request,
    or None if it's regular conversation.
    """
    msg = message.lower()
    for category, keywords in _REQUEST_KEYWORDS.items():
        if any(kw in msg for kw in keywords):
            return category
    return None


def save_request(hotel_slug: str, room: str, guest_name: str,
                 category: str, message: str) -> int:
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        """INSERT INTO requests
           (hotel_slug, room, guest_name, category, message, status, created_at)
           VALUES (?, ?, ?, ?, ?, 'pending', ?)""",
        (hotel_slug, room, guest_name, category, message,
         datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    req_id = cur.lastrowid
    conn.commit()
    conn.close()
    return req_id


def get_requests(hotel_slug: str, status: str | None = None) -> list:
    conn = sqlite3.connect(DATABASE_PATH)
    if status:
        rows = conn.execute(
            """SELECT id, room, guest_name, category, message, status,
                      created_at, resolved_at
               FROM requests WHERE hotel_slug=? AND status=?
               ORDER BY id DESC""",
            (hotel_slug, status)
        ).fetchall()
    else:
        rows = conn.execute(
            """SELECT id, room, guest_name, category, message, status,
                      created_at, resolved_at
               FROM requests WHERE hotel_slug=?
               ORDER BY CASE status
                   WHEN 'pending'     THEN 0
                   WHEN 'in_progress' THEN 1
                   ELSE 2
               END, id DESC""",
            (hotel_slug,)
        ).fetchall()
    conn.close()
    return [
        {
            "id": r[0], "room": r[1], "guest_name": r[2], "category": r[3],
            "message": r[4], "status": r[5], "created_at": r[6],
            "resolved_at": r[7] or ""
        }
        for r in rows
    ]


def update_request_status(req_id: int, hotel_slug: str, status: str) -> bool:
    resolved_at = datetime.now().strftime("%Y-%m-%d %H:%M") if status == "resolved" else ""
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        "UPDATE requests SET status=?, resolved_at=? WHERE id=? AND hotel_slug=?",
        (status, resolved_at, req_id, hotel_slug)
    )
    changed = cur.rowcount > 0
    conn.commit()
    conn.close()
    return changed


def delete_request(req_id: int, hotel_slug: str) -> bool:
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        "DELETE FROM requests WHERE id=? AND hotel_slug=?",
        (req_id, hotel_slug)
    )
    changed = cur.rowcount > 0
    conn.commit()
    conn.close()
    return changed


def get_pending_requests_count(hotel_slug: str) -> int:
    conn = sqlite3.connect(DATABASE_PATH)
    count = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE hotel_slug=? AND status IN ('pending','in_progress')",
        (hotel_slug,)
    ).fetchone()[0]
    conn.close()
    return count


# ─── Room Notes ─────────────────────────────────────────────────────────────

def get_room_notes(hotel_slug: str, room: str) -> list:
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        """SELECT id, note, author, created_at
           FROM room_notes WHERE hotel_slug=? AND room=?
           ORDER BY id DESC""",
        (hotel_slug, room)
    ).fetchall()
    conn.close()
    return [{"id": r[0], "note": r[1], "author": r[2], "created_at": r[3]} for r in rows]


def save_room_note(hotel_slug: str, room: str, note: str, author: str = "Персонал") -> int:
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        "INSERT INTO room_notes (hotel_slug, room, note, author, created_at) VALUES (?, ?, ?, ?, ?)",
        (hotel_slug, room, note, author, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    note_id = cur.lastrowid
    conn.commit()
    conn.close()
    return note_id


def delete_room_note(note_id: int, hotel_slug: str) -> bool:
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        "DELETE FROM room_notes WHERE id=? AND hotel_slug=?", (note_id, hotel_slug)
    )
    changed = cur.rowcount > 0
    conn.commit()
    conn.close()
    return changed


def get_hotel_avg_rating(slug):
    conn = sqlite3.connect(DATABASE_PATH)
    row = conn.execute(
        "SELECT AVG(rating), COUNT(*) FROM ratings WHERE hotel_slug=?", (slug,)
    ).fetchone()
    conn.close()
    avg, count = row
    return (round(avg, 1) if avg else None), (count or 0)


# ─── Staff Accounts ─────────────────────────────────────────────────────────

STAFF_ROLES = ("manager", "receptionist", "housekeeping")


def create_staff(hotel_slug: str, name: str, username: str,
                 password: str, role: str = "receptionist") -> int | None:
    """Create a new staff member. Returns new id, or None if username already exists."""
    if role not in STAFF_ROLES:
        role = "receptionist"
    pw_hash = hash_password(password)
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cur = conn.execute(
            """INSERT INTO staff (hotel_slug, name, username, password_hash, role, is_active, created_at)
               VALUES (?, ?, ?, ?, ?, 1, ?)""",
            (hotel_slug, name.strip(), username.strip().lower(),
             pw_hash, role, datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        staff_id = cur.lastrowid
        conn.commit()
        return staff_id
    except sqlite3.IntegrityError:
        return None  # username already exists for this hotel
    finally:
        conn.close()


def get_staff_list(hotel_slug: str) -> list:
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        """SELECT id, name, username, role, is_active, created_at
           FROM staff WHERE hotel_slug=? ORDER BY id""",
        (hotel_slug,)
    ).fetchall()
    conn.close()
    return [
        {"id": r[0], "name": r[1], "username": r[2],
         "role": r[3], "is_active": bool(r[4]), "created_at": r[5]}
        for r in rows
    ]


def get_staff_by_credentials(hotel_slug: str, username: str, password: str) -> dict | None:
    """Returns staff dict if credentials are valid and account is active, else None."""
    conn = sqlite3.connect(DATABASE_PATH)
    row = conn.execute(
        """SELECT id, name, username, role, password_hash
           FROM staff WHERE hotel_slug=? AND username=? AND is_active=1""",
        (hotel_slug, username.strip().lower())
    ).fetchone()
    conn.close()
    if not row:
        return None
    try:
        if bcrypt.checkpw(password.encode("utf-8"), row[4].encode("utf-8")):
            return {"id": row[0], "name": row[1], "username": row[2], "role": row[3]}
    except Exception:
        pass
    return None


def get_staff_by_id(hotel_slug: str, staff_id: int) -> dict | None:
    conn = sqlite3.connect(DATABASE_PATH)
    row = conn.execute(
        "SELECT id, name, username, role, is_active FROM staff WHERE id=? AND hotel_slug=?",
        (staff_id, hotel_slug)
    ).fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "username": row[2],
                "role": row[3], "is_active": bool(row[4])}
    return None


def update_staff_password(staff_id: int, hotel_slug: str, new_password: str) -> bool:
    pw_hash = hash_password(new_password)
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        "UPDATE staff SET password_hash=? WHERE id=? AND hotel_slug=?",
        (pw_hash, staff_id, hotel_slug)
    )
    changed = cur.rowcount > 0
    conn.commit()
    conn.close()
    return changed


def delete_staff(staff_id: int, hotel_slug: str) -> bool:
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        "DELETE FROM staff WHERE id=? AND hotel_slug=?", (staff_id, hotel_slug)
    )
    changed = cur.rowcount > 0
    conn.commit()
    conn.close()
    return changed


# ─── Owners (multi-hotel accounts) ──────────────────────────────────────────

def create_owner(name: str, email: str, password: str) -> int | None:
    """Create hotel owner account. Returns id or None if email already exists."""
    pw_hash = hash_password(password)
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cur = conn.execute(
            "INSERT INTO owners (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (name.strip(), email.strip().lower(), pw_hash,
             datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        owner_id = cur.lastrowid
        conn.commit()
        return owner_id
    except sqlite3.IntegrityError:
        return None  # email already exists
    finally:
        conn.close()


def get_owner_by_email(email: str) -> dict | None:
    conn = sqlite3.connect(DATABASE_PATH)
    row = conn.execute(
        "SELECT id, name, email, password_hash FROM owners WHERE email=?",
        (email.strip().lower(),)
    ).fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "email": row[2], "password_hash": row[3]}
    return None


def get_owner_by_id(owner_id: int) -> dict | None:
    conn = sqlite3.connect(DATABASE_PATH)
    row = conn.execute(
        "SELECT id, name, email FROM owners WHERE id=?", (owner_id,)
    ).fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "email": row[2]}
    return None


def get_all_owners() -> list:
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        "SELECT id, name, email, created_at FROM owners ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "email": r[2], "created_at": r[3]} for r in rows]


def assign_hotel_to_owner(owner_id: int, hotel_slug: str) -> bool:
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        conn.execute(
            "INSERT OR IGNORE INTO hotel_owners (owner_id, hotel_slug) VALUES (?, ?)",
            (owner_id, hotel_slug)
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def remove_hotel_from_owner(owner_id: int, hotel_slug: str) -> bool:
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        "DELETE FROM hotel_owners WHERE owner_id=? AND hotel_slug=?",
        (owner_id, hotel_slug)
    )
    changed = cur.rowcount > 0
    conn.commit()
    conn.close()
    return changed


def get_owner_hotels(owner_id: int) -> list:
    """Return list of hotel slugs assigned to this owner."""
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        """SELECT h.slug, h.name, h.plan
           FROM hotels h
           JOIN hotel_owners ho ON ho.hotel_slug = h.slug
           WHERE ho.owner_id=?
           ORDER BY h.name""",
        (owner_id,)
    ).fetchall()
    conn.close()
    return [{"slug": r[0], "name": r[1], "plan": r[2] or "trial"} for r in rows]


def get_hotel_owner_ids(hotel_slug: str) -> list:
    """Return list of owner IDs that have access to this hotel."""
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        "SELECT owner_id FROM hotel_owners WHERE hotel_slug=?", (hotel_slug,)
    ).fetchall()
    conn.close()
    return [r[0] for r in rows]


# ─── Services Catalog ────────────────────────────────────────────────────────

def create_service(hotel_slug: str, name: str, description: str = "",
                   category: str = "general", price: float = 0,
                   currency: str = "USD", icon: str = "🛎️",
                   sort_order: int = 0) -> int:
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        """INSERT INTO services
           (hotel_slug, name, description, category, price, currency, icon, is_active, sort_order)
           VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)""",
        (hotel_slug, name.strip(), description.strip(), category, price, currency, icon, sort_order)
    )
    svc_id = cur.lastrowid
    conn.commit()
    conn.close()
    return svc_id


def get_services(hotel_slug: str, active_only: bool = False) -> list:
    conn = sqlite3.connect(DATABASE_PATH)
    q = """SELECT id, name, description, category, price, currency, icon, is_active, sort_order
           FROM services WHERE hotel_slug=?"""
    params = [hotel_slug]
    if active_only:
        q += " AND is_active=1"
    q += " ORDER BY sort_order ASC, id ASC"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [
        {
            "id": r[0], "name": r[1], "description": r[2], "category": r[3],
            "price": r[4], "currency": r[5], "icon": r[6],
            "is_active": bool(r[7]), "sort_order": r[8]
        }
        for r in rows
    ]


def update_service(svc_id: int, hotel_slug: str, name: str = None,
                   description: str = None, category: str = None,
                   price: float = None, currency: str = None,
                   icon: str = None, is_active: bool = None,
                   sort_order: int = None) -> bool:
    fields, values = [], []
    if name is not None:
        fields.append("name=?"); values.append(name.strip())
    if description is not None:
        fields.append("description=?"); values.append(description.strip())
    if category is not None:
        fields.append("category=?"); values.append(category)
    if price is not None:
        fields.append("price=?"); values.append(float(price))
    if currency is not None:
        fields.append("currency=?"); values.append(currency)
    if icon is not None:
        fields.append("icon=?"); values.append(icon)
    if is_active is not None:
        fields.append("is_active=?"); values.append(1 if is_active else 0)
    if sort_order is not None:
        fields.append("sort_order=?"); values.append(int(sort_order))
    if not fields:
        return False
    values.extend([svc_id, hotel_slug])
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        f"UPDATE services SET {', '.join(fields)} WHERE id=? AND hotel_slug=?", values
    )
    changed = cur.rowcount > 0
    conn.commit()
    conn.close()
    return changed


def delete_service(svc_id: int, hotel_slug: str) -> bool:
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        "DELETE FROM services WHERE id=? AND hotel_slug=?", (svc_id, hotel_slug)
    )
    changed = cur.rowcount > 0
    conn.commit()
    conn.close()
    return changed


# ─── Staff Chat ──────────────────────────────────────────────────────────────

STAFF_CHANNELS = ("general", "reception", "housekeeping", "maintenance")


def save_staff_msg(hotel_slug: str, channel: str, sender: str,
                   role_label: str, message: str) -> int:
    if channel not in STAFF_CHANNELS:
        channel = "general"
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(
        """INSERT INTO staff_chat (hotel_slug, channel, sender, role_label, message, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (hotel_slug, channel, sender.strip(), role_label,
         message.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    msg_id = cur.lastrowid
    conn.commit()
    conn.close()
    return msg_id


def get_staff_msgs(hotel_slug: str, channel: str, limit: int = 60) -> list:
    if channel not in STAFF_CHANNELS:
        channel = "general"
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        """SELECT id, sender, role_label, message, created_at
           FROM staff_chat WHERE hotel_slug=? AND channel=?
           ORDER BY id DESC LIMIT ?""",
        (hotel_slug, channel, limit)
    ).fetchall()
    conn.close()
    return [
        {"id": r[0], "sender": r[1], "role": r[2], "message": r[3], "created_at": r[4]}
        for r in reversed(rows)
    ]


def get_staff_msgs_since(hotel_slug: str, channel: str, since_id: int) -> list:
    if channel not in STAFF_CHANNELS:
        channel = "general"
    conn = sqlite3.connect(DATABASE_PATH)
    rows = conn.execute(
        """SELECT id, sender, role_label, message, created_at
           FROM staff_chat WHERE hotel_slug=? AND channel=? AND id > ?
           ORDER BY id ASC LIMIT 50""",
        (hotel_slug, channel, since_id)
    ).fetchall()
    conn.close()
    return [
        {"id": r[0], "sender": r[1], "role": r[2], "message": r[3], "created_at": r[4]}
        for r in rows
    ]