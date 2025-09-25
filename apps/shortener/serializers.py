from rest_framework import serializers

from apps.shortener.models import ShortenedURL


class ShortenedURLCreateViewRequestSerializer(serializers.Serializer):
    original_url = serializers.URLField(
        required=True,
        write_only=True,
        allow_blank=False,
    )


class ShortenedURLCreateViewResponseSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortenedURL
        fields = (
            "id",
            "original_url",
            "short_code",
            "short_url",
        )
        read_only_fields = fields

    def get_short_url(self, obj) -> str:
        request = self.context["request"]
        return request.build_absolute_uri(f"/{obj.short_code}")


class ShortenedURLRetrieveViewResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = (
            "id",
            "original_url",
            "short_code",
        )
        read_only_fields = fields
