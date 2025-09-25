from unittest.mock import patch

import pytest

from apps.shortener.models import ShortenedURL
from apps.shortener.services import ShortenedURLService

pytestmark = pytest.mark.django_db


class TestShortenedURLService:
    @pytest.fixture
    def service(self, original_url: str) -> ShortenedURLService:
        return ShortenedURLService(original_url=original_url)

    def test_get_or_create_shortened_url_creates_new_object(
        self,
        original_url: str,
        service: ShortenedURLService,
    ):
        assert ShortenedURL.objects.count() == 0
        created, shortened_url = service.get_or_create_shortened_url()

        assert created is True
        assert ShortenedURL.objects.count() == 1
        assert shortened_url.original_url == original_url
        assert shortened_url.short_code

    @patch("apps.shortener.services.blake2s_encrypt")
    def test_get_or_create_shortened_url_creates_new_object_using_blake2s_encryption(
        self,
        mock_encrypt,
        original_url: str,
        service: ShortenedURLService,
    ):
        expected_short_code = "mockedhash"
        mock_encrypt.return_value = expected_short_code

        created, shortened_url = service.get_or_create_shortened_url()

        assert created is True
        assert shortened_url.short_code == expected_short_code
        mock_encrypt.assert_called_once_with(url=original_url)

    def test_get_or_create_shortened_url_returns_existing_object(
        self,
        original_url: str,
        service: ShortenedURLService,
    ):
        shortened_url = ShortenedURL.objects.create(
            original_url=original_url, short_code="abc123"
        )

        created, service_shortened_url = service.get_or_create_shortened_url()

        assert created is False
        assert shortened_url.pk == service_shortened_url.pk
