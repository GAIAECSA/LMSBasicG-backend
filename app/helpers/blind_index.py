import hashlib
import hmac
import os

SECRET_KEY = os.getenv("ENCRYPTION_KEY")


def generate_blind_index(value: str) -> str | None:
    if not value:
        return None
    return hmac.new(
        SECRET_KEY.encode("utf-8"), value.strip().encode("utf-8"), hashlib.sha256
    ).hexdigest()
