from typing import Any

from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.shortener.models import ShortenedURL

pytestmark = pytest.mark.django_db


class TestShortenedURLCreateView:
    @pytest.fixture
    def view_url(self) -> str:
        return reverse("shortener:shorten")

    @pytest.fixture
    def request_data(self, original_url: str) -> dict[str, str]:
        return {"original_url": original_url}

    def test_create_new_shortened_url(
        self,
        client: APIClient,
        view_url: str,
        request_data: dict[str, str],
    ):
        assert ShortenedURL.objects.all().count() == 0
        response = client.post(view_url, data=request_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert ShortenedURL.objects.all().count() == 1
        shortened_url = ShortenedURL.objects.get(
            original_url=request_data["original_url"]
        )

        scheme = response.wsgi_request.scheme
        host = response.wsgi_request.get_host()
        expected_response_data = {
            "id": shortened_url.id,
            "original_url": shortened_url.original_url,
            "short_code": shortened_url.short_code,
            "short_url": f"{scheme}://{host}/{shortened_url.short_code}",
        }
        assert response.data == expected_response_data

    def test_retrieve_existing_shortened_url(
        self,
        client: APIClient,
        view_url: str,
        request_data: dict[str, str],
    ):
        shortened_url = ShortenedURL.objects.create(
            original_url=request_data["original_url"], short_code="xy789fuoAB"
        )
        assert ShortenedURL.objects.all().count() == 1

        response = client.post(view_url, data=request_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert ShortenedURL.objects.all().count() == 1

        scheme = response.wsgi_request.scheme
        host = response.wsgi_request.get_host()
        expected_response_data = {
            "id": shortened_url.id,
            "original_url": shortened_url.original_url,
            "short_code": shortened_url.short_code,
            "short_url": f"{scheme}://{host}/{shortened_url.short_code}",
        }
        assert response.data == expected_response_data

    @pytest.mark.parametrize(
        ("original_url", "response_field_validation_message"),
        [
            ("not-a-valid-url", "Enter a valid URL."),
            ("", "This field may not be blank."),
            (12345, "Enter a valid URL."),
            (None, "This field may not be null."),
        ],
    )
    def test_return_400_when_invalid_original_url_passed(
        self,
        original_url: Any,
        response_field_validation_message: str,
        client: APIClient,
        view_url: str,
    ):
        request_data = {"original_url": original_url}

        response = client.post(view_url, data=request_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert ShortenedURL.objects.count() == 0
        assert response.json() == {"original_url": [response_field_validation_message]}


class TestShortenedURLRetrieveView:
    @pytest.fixture
    def view_url_name(self) -> str:
        return "shortener:resolve"

    @pytest.fixture
    def shortened_url(self, original_url: str) -> ShortenedURL:
        return ShortenedURL.objects.create(
            original_url=original_url, short_code="abc123"
        )

    def test_resolve_existing_code(
        self,
        client: APIClient,
        shortened_url: ShortenedURL,
        view_url_name: str,
    ):
        # Given
        url = reverse(view_url_name, kwargs={"short_code": shortened_url.short_code})

        # When
        response = client.get(url)

        # Then
        assert response.status_code == 200
        assert response.data["original_url"] == shortened_url.original_url

    def test_resolve_nonexistent_code(
        self,
        client: APIClient,
        shortened_url: ShortenedURL,
        view_url_name: str,
    ):
        # Given
        url = reverse(view_url_name, kwargs={"short_code": "notfound"})

        # When
        response = client.get(url)

        # Then
        assert response.status_code == 404
