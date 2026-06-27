"""
Localized staff-facing notification strings (Telegram + email subjects).

Notifications used to be a mix of hardcoded Turkish and Russian regardless of the
hotel's language. Now each hotel gets its notifications in its own `default_language`
(falling back to English for languages we don't have strings for).

Usage:
    lang = notif_lang(hotel)              # 'en' | 'ru' | 'tr' | 'uz'
    text = nt(lang, "checkin", name=..., room=...)
"""

SUPPORTED = ("en", "ru", "tr", "uz")

NOTIF_I18N = {
    "en": {
        "checkin": ("🏨 <b>New check-in!</b>\n"
                    "👤 {name} ({nat})\n"
                    "🚪 Room: {room}\n"
                    "📅 {ci} → {co}\n"
                    "🪪 Passport: {passport}"),
        "new_msg": ("💬 <b>{hotel}</b>\n"
                    "🚪 Room {room} · {time}\n"
                    "{message}\n\n"
                    "<i>↩️ Reply to this message to answer the guest.</i>"),
        "urgent": ("🔴 <b>URGENT!</b>\n"
                   "🏨 Hotel: {hotel}\n"
                   "🚪 Room: {room}\n"
                   "💬 Message: {message}\n"
                   "⏰ Time: {time}\n\n"
                   "<i>↩️ Reply to this message to write to the guest.</i>"),
        "low_rating": ("⚠️ <b>Low rating received!</b>\n"
                       "🏨 Hotel: {hotel}\n"
                       "🚪 Room: {room}\n"
                       "⭐ Rating: {stars} ({rating}/5)\n"
                       "⏰ Act now — fix it before the guest leaves!"),
        "staff_reply": ("📤 <b>Staff reply</b> — {hotel}\n"
                        "🚪 Room {room} · {time}\n"
                        "{message}"),
        "auto_checkout": ("🔄 <b>Auto check-out</b> — {hotel}\n"
                          "{n} guest(s) were checked out automatically (check-out date passed)."),
        "checkout_reminder": ("⏰ <b>Check-out reminder</b>\n"
                              "👤 {name}\n"
                              "🚪 Room: {room}\n"
                              "📅 Checking out today — please make the arrangements."),
        "digest_title": "☀️ <b>Daily summary — {date}</b>",
        "digest_active": "🛎️ Active guests: <b>{n}</b>",
        "digest_checkin": "📥 Check-ins today: <b>{n}</b>",
        "digest_checkout": "📤 Check-outs today: <b>{n}</b>",
        "digest_unread": "📬 Unread messages: <b>{n}</b>",
        "digest_rating": "⭐ Average rating: <b>{r}</b>",
        "rating_none": "— no reviews",
        "reviews_word": "reviews",
    },
    "ru": {
        "checkin": ("🏨 <b>Новый заезд!</b>\n"
                    "👤 {name} ({nat})\n"
                    "🚪 Номер: {room}\n"
                    "📅 {ci} → {co}\n"
                    "🪪 Паспорт: {passport}"),
        "new_msg": ("💬 <b>{hotel}</b>\n"
                    "🚪 Номер {room} · {time}\n"
                    "{message}\n\n"
                    "<i>↩️ Ответьте на это сообщение, чтобы написать гостю.</i>"),
        "urgent": ("🔴 <b>СРОЧНО!</b>\n"
                   "🏨 Отель: {hotel}\n"
                   "🚪 Номер: {room}\n"
                   "💬 Сообщение: {message}\n"
                   "⏰ Время: {time}\n\n"
                   "<i>↩️ Ответьте на это сообщение, чтобы написать гостю.</i>"),
        "low_rating": ("⚠️ <b>Низкая оценка!</b>\n"
                       "🏨 Отель: {hotel}\n"
                       "🚪 Номер: {room}\n"
                       "⭐ Оценка: {stars} ({rating}/5)\n"
                       "⏰ Действуйте сейчас — решите проблему до отъезда гостя!"),
        "staff_reply": ("📤 <b>Ответ персонала</b> — {hotel}\n"
                        "🚪 Номер {room} · {time}\n"
                        "{message}"),
        "auto_checkout": ("🔄 <b>Автоматический выезд</b> — {hotel}\n"
                          "{n} гость(ей) выписан(ы) автоматически (дата выезда прошла)."),
        "checkout_reminder": ("⏰ <b>Напоминание о выезде</b>\n"
                              "👤 {name}\n"
                              "🚪 Номер: {room}\n"
                              "📅 Сегодня выезд — подготовьте всё необходимое."),
        "digest_title": "☀️ <b>Ежедневная сводка — {date}</b>",
        "digest_active": "🛎️ Активных гостей: <b>{n}</b>",
        "digest_checkin": "📥 Заездов сегодня: <b>{n}</b>",
        "digest_checkout": "📤 Выездов сегодня: <b>{n}</b>",
        "digest_unread": "📬 Непрочитанных сообщений: <b>{n}</b>",
        "digest_rating": "⭐ Средняя оценка: <b>{r}</b>",
        "rating_none": "— отзывов нет",
        "reviews_word": "отзывов",
    },
    "tr": {
        "checkin": ("🏨 <b>Yeni Check-in!</b>\n"
                    "👤 {name} ({nat})\n"
                    "🚪 Oda: {room}\n"
                    "📅 {ci} → {co}\n"
                    "🪪 Pasaport: {passport}"),
        "new_msg": ("💬 <b>{hotel}</b>\n"
                    "🚪 Oda {room} · {time}\n"
                    "{message}\n\n"
                    "<i>↩️ Yanıt vermek için bu mesaja cevap verin.</i>"),
        "urgent": ("🔴 <b>ACİL!</b>\n"
                   "🏨 Otel: {hotel}\n"
                   "🚪 Oda: {room}\n"
                   "💬 Mesaj: {message}\n"
                   "⏰ Saat: {time}\n\n"
                   "<i>↩️ Misafire yazmak için bu mesaja cevap verin.</i>"),
        "low_rating": ("⚠️ <b>Düşük Puan Alındı!</b>\n"
                       "🏨 Otel: {hotel}\n"
                       "🚪 Oda: {room}\n"
                       "⭐ Puan: {stars} ({rating}/5)\n"
                       "⏰ Şimdi harekete geçin — misafir ayrılmadan sorunu çözün!"),
        "staff_reply": ("📤 <b>Personel yanıtı</b> — {hotel}\n"
                        "🚪 Oda {room} · {time}\n"
                        "{message}"),
        "auto_checkout": ("🔄 <b>Otomatik Check-out</b> — {hotel}\n"
                          "{n} misafir check-out tarihi geçtiği için otomatik çıkış yapıldı."),
        "checkout_reminder": ("⏰ <b>Check-out Hatırlatması</b>\n"
                              "👤 {name}\n"
                              "🚪 Oda: {room}\n"
                              "📅 Bugün çıkış yapacak — gerekli düzenlemeleri yapın."),
        "digest_title": "☀️ <b>Günlük Özet — {date}</b>",
        "digest_active": "🛎️ Aktif misafir: <b>{n}</b>",
        "digest_checkin": "📥 Bugün check-in: <b>{n}</b>",
        "digest_checkout": "📤 Bugün check-out: <b>{n}</b>",
        "digest_unread": "📬 Okunmamış mesaj: <b>{n}</b>",
        "digest_rating": "⭐ Ortalama puan: <b>{r}</b>",
        "rating_none": "— yorum yok",
        "reviews_word": "yorum",
    },
    "uz": {
        "checkin": ("🏨 <b>Yangi check-in!</b>\n"
                    "👤 {name} ({nat})\n"
                    "🚪 Xona: {room}\n"
                    "📅 {ci} → {co}\n"
                    "🪪 Pasport: {passport}"),
        "new_msg": ("💬 <b>{hotel}</b>\n"
                    "🚪 Xona {room} · {time}\n"
                    "{message}\n\n"
                    "<i>↩️ Mehmonga javob berish uchun shu xabarga javob yozing.</i>"),
        "urgent": ("🔴 <b>SHOSHILINCH!</b>\n"
                   "🏨 Mehmonxona: {hotel}\n"
                   "🚪 Xona: {room}\n"
                   "💬 Xabar: {message}\n"
                   "⏰ Vaqt: {time}\n\n"
                   "<i>↩️ Mehmonga yozish uchun shu xabarga javob bering.</i>"),
        "low_rating": ("⚠️ <b>Past baho olindi!</b>\n"
                       "🏨 Mehmonxona: {hotel}\n"
                       "🚪 Xona: {room}\n"
                       "⭐ Baho: {stars} ({rating}/5)\n"
                       "⏰ Hozir choralar ko‘ring — mehmon ketishidan oldin muammoni hal qiling!"),
        "staff_reply": ("📤 <b>Xodim javobi</b> — {hotel}\n"
                        "🚪 Xona {room} · {time}\n"
                        "{message}"),
        "auto_checkout": ("🔄 <b>Avtomatik check-out</b> — {hotel}\n"
                          "{n} mehmon check-out sanasi o‘tgani uchun avtomatik chiqarildi."),
        "checkout_reminder": ("⏰ <b>Check-out eslatmasi</b>\n"
                              "👤 {name}\n"
                              "🚪 Xona: {room}\n"
                              "📅 Bugun chiqib ketadi — kerakli tayyorgarlikni ko‘ring."),
        "digest_title": "☀️ <b>Kunlik hisobot — {date}</b>",
        "digest_active": "🛎️ Faol mehmonlar: <b>{n}</b>",
        "digest_checkin": "📥 Bugun check-in: <b>{n}</b>",
        "digest_checkout": "📤 Bugun check-out: <b>{n}</b>",
        "digest_unread": "📬 O‘qilmagan xabarlar: <b>{n}</b>",
        "digest_rating": "⭐ O‘rtacha baho: <b>{r}</b>",
        "rating_none": "— sharhlar yo‘q",
        "reviews_word": "sharh",
    },
}


def notif_lang(hotel: dict) -> str:
    """Pick the notification language for a hotel: its setting, or English fallback."""
    lang = (hotel.get("default_language") or "auto")
    return lang if lang in NOTIF_I18N else "en"


def nt(lang: str, key: str, **kw) -> str:
    """Return a localized notification string, formatted with kw."""
    table = NOTIF_I18N.get(lang, NOTIF_I18N["en"])
    template = table.get(key) or NOTIF_I18N["en"].get(key, "")
    try:
        return template.format(**kw)
    except (KeyError, IndexError):
        return template
