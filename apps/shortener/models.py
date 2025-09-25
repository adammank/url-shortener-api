from django.db import models

from apps.utils.models import TimeStampedModelMixin


class ShortenedURL(TimeStampedModelMixin):
    original_url = models.URLField(unique=True)
    short_code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Unique code for the shortened URL",
    )

    class Meta:
        ordering = ("-created_date",)
        verbose_name = "Shortened URL"
        verbose_name_plural = "Shortened URLs"

    def __str__(self) -> str:
        return self.short_code
