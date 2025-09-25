from __future__ import annotations

from apps.shortener.models import ShortenedURL
from apps.shortener.utils import blake2s_encrypt


class ShortenedURLService:
    def __init__(self, original_url: str):
        self.original_url = original_url

    def get_or_create_shortened_url(self) -> tuple[bool, ShortenedURL]:
        """Get an existing ShortenedURL based on its original_url
        or create a new one with encrypting its original_url if it doesn't exist."""

        created = False
        shortened_url = self._get_shortened_url()
        if not shortened_url:
            created = True
            shortened_url = self._create_shortened_url()

        return created, shortened_url

    def _get_shortened_url(self) -> ShortenedURL | None:
        """Retrieve an existing ShortenedURL entry from the database."""

        try:
            return ShortenedURL.objects.get(original_url=self.original_url)
        except ShortenedURL.DoesNotExist:
            return None

    def _create_shortened_url(self) -> ShortenedURL:
        """Create a new ShortenedURL entry in the database."""

        short_code = blake2s_encrypt(url=self.original_url)
        return ShortenedURL.objects.create(
            original_url=self.original_url, short_code=short_code
        )
