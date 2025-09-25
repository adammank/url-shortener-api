import base64
import hashlib

from django.conf import settings


def blake2s_encrypt(url: str, key: bytes | None = None, length: int = 10) -> str:
    """Generate a short, URL-safe hash from the given URL using the BLAKE2s algorithm."""

    if key is None:
        key = settings.BLAKE2S_KEY.encode("utf-8")

    url_hash = hashlib.blake2s(
        url.encode("utf-8"),
        key=key,
        digest_size=16,
    ).digest()

    url_b64 = base64.urlsafe_b64encode(url_hash).decode("ascii").rstrip("=")

    return url_b64[::2][:length]
