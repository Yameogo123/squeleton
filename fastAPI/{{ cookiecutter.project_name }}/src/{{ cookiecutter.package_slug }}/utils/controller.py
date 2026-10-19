import hashlib
import hmac

import httpx
from cryptography.fernet import Fernet, InvalidToken
from fastapi import HTTPException
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

from {{ cookiecutter.package_slug }}.core.config import settings

# Argon2 for new hashes, bcrypt still accepted to verify hashes created by older versions
password_hash = PasswordHash((Argon2Hasher(), BcryptHasher()))
# pre-computed hash used to keep login timing identical whether the user exists or not
DUMMY_HASH = password_hash.hash("dummy-password-for-timing")

fernet = Fernet(settings.FERNET_KEY.encode())
_blind_key = settings.BLIND_INDEX_KEY.encode()

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"


def from_model_to_dict(model) -> dict:
    return model.model_dump()


def serialize_model(model: dict) -> dict:
    if model and "_id" in model:
        model["_id"] = str(model["_id"])
    return model


def hash_pwd(pwd: str) -> str:
    return password_hash.hash(pwd)


def verify_password(plain_password: str, hashed_password: str | None) -> bool:
    if not hashed_password:
        password_hash.verify(plain_password, DUMMY_HASH)
        return False
    try:
        return password_hash.verify(plain_password, hashed_password)
    except Exception:
        return False


def http_error(e, status: int = 400):
    raise HTTPException(status_code=status, detail={"error": str(e)})


async def send_push_notification(expo_token: str, title: str, body: str, data: dict | None = None) -> dict:
    """Send a push notification through Expo."""
    message = {"to": expo_token, "sound": "default", "title": title, "body": body, "data": data or {}}
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(EXPO_PUSH_URL, json=message)
        response.raise_for_status()
        return response.json()


def encrypt_text(text: str | None) -> str | None:
    """Fernet encryption (random IV: the same input never gives the same output -> not searchable)."""
    if not text:
        return text
    return fernet.encrypt(text.encode("utf-8")).decode("ascii")


def decrypt_text(token: str | bytes | None) -> str | None:
    if not token:
        return token
    raw = token if isinstance(token, bytes) else token.encode("ascii", errors="ignore")
    try:
        return fernet.decrypt(raw).decode("utf-8")
    except InvalidToken:
        # value was stored in clear (legacy data): return it as is
        return token.decode() if isinstance(token, bytes) else token


def blind_index(value: str | None) -> str | None:
    """Deterministic keyed hash, stored next to an encrypted field to allow exact-match lookups."""
    if not value:
        return None
    return hmac.new(_blind_key, value.strip().lower().encode("utf-8"), hashlib.sha256).hexdigest()
