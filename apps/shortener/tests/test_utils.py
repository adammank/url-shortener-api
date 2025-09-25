from django.conf import settings

from apps.shortener.utils import blake2s_encrypt


def test_blake2s_encrypt_default_key(monkeypatch, original_url):
    # Arrange
    monkeypatch.setattr(settings, "BLAKE2S_KEY", "testkey")

    # Act
    result = blake2s_encrypt(original_url)

    # Assert
    assert result == "qvJX1C9PpR"


def test_blake2s_encrypt_custom_key(original_url):
    # Arrange
    key = b"customkey"

    # Act
    result = blake2s_encrypt(original_url, key=key, length=8)

    # Assert
    assert result == "6CZjJ8nM"


def test_blake2s_encrypt_different_urls(monkeypatch, original_url):
    # Arrange
    monkeypatch.setattr(settings, "BLAKE2S_KEY", "testkey")
    url_2 = "https://example.com/2"

    # Act
    hash1 = blake2s_encrypt(original_url)
    hash2 = blake2s_encrypt(url_2)

    # Assert
    assert hash1 != hash2
