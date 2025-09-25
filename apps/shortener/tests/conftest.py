import pytest
from rest_framework.test import APIClient


@pytest.fixture
def original_url() -> str:
    return "https://example.com"


@pytest.fixture
def client() -> APIClient:
    return APIClient()
