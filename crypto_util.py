"""
Field-level encryption for sensitive guest PII (passport, names).

Data is encrypted at rest in the SQLite database, so a stolen DB file or backup
is useless without the key. The key lives ONLY in an environment variable
(DATA_ENCRYPTION_KEY), never in the database — keep them separate.

- encrypt(text) -> "enc:..."  (or "" for empty input)
- decrypt(token) -> plaintext (transparently passes through legacy plaintext,
  so existing rows keep working and get encrypted on next write).

If DATA_ENCRYPTION_KEY is not set it falls back to GUEST_TOKEN_SECRET so the
app still works, but a dedicated key is recommended. NOTE: changing the key
makes already-encrypted data unreadable — set it once and keep it stable.
"""

import os
import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken
from config import GUEST_TOKEN_SECRET

_secret = os.getenv("DATA_ENCRYPTION_KEY") or GUEST_TOKEN_SECRET or "smartstay-data"
# Derive a valid 32-byte urlsafe Fernet key from whatever secret string we have.
_key = base64.urlsafe_b64encode(hashlib.sha256(_secret.encode()).digest())
_fernet = Fernet(_key)

_PREFIX = "enc:"


def encrypt(text) -> str:
    """Encrypt a value for storage. Empty/None -> ''."""
    if text is None:
        return ""
    text = str(text)
    if text == "":
        return ""
    return _PREFIX + _fernet.encrypt(text.encode("utf-8")).decode("ascii")


def decrypt(token) -> str:
    """Decrypt a stored value. Legacy plaintext (no prefix) is returned as-is."""
    if not token:
        return ""
    token = str(token)
    if not token.startswith(_PREFIX):
        return token  # legacy plaintext row — return unchanged
    try:
        return _fernet.decrypt(token[len(_PREFIX):].encode("ascii")).decode("utf-8")
    except (InvalidToken, Exception):
        return ""
