from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from apps.shortener.models import ShortenedURL
from apps.shortener.serializers import (
    ShortenedURLCreateViewRequestSerializer,
    ShortenedURLCreateViewResponseSerializer,
    ShortenedURLRetrieveViewResponseSerializer,
)
from apps.shortener.services import ShortenedURLService


@extend_schema(
    summary="Create a shortened URL object",
    description="Create a shortened URL object based on the full URL and "
    "return its shortened code with short URL.",
    request=ShortenedURLCreateViewRequestSerializer,
    responses={
        200: OpenApiResponse(
            response=ShortenedURLCreateViewResponseSerializer,
            description="Short URL already exists (idempotent).",
        ),
        201: OpenApiResponse(
            response=ShortenedURLCreateViewResponseSerializer,
            description="Short URL created.",
        ),
        400: OpenApiResponse(description="Invalid URL"),
    },
)
class ShortenedURLCreateView(CreateAPIView):
    serializer_class = ShortenedURLCreateViewRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = ShortenedURLService(
            original_url=serializer.validated_data["original_url"]
        )
        created, shortened_url = service.get_or_create_shortened_url()

        data = ShortenedURLCreateViewResponseSerializer(
            shortened_url, context={"request": request}
        ).data

        return Response(
            data=data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


@extend_schema(
    summary="Resolve a short code",
    description="Given a short code, returns the original full URL.",
    responses={
        200: OpenApiResponse(
            response=ShortenedURLRetrieveViewResponseSerializer,
            description="Original URL found",
        ),
        404: OpenApiResponse(description="Code not found"),
    },
)
class ShortenedURLRetrieveView(RetrieveAPIView):
    queryset = ShortenedURL.objects.all()
    lookup_field = "short_code"
    serializer_class = ShortenedURLRetrieveViewResponseSerializer
