from django.urls import path

from apps.shortener.views import ShortenedURLCreateView, ShortenedURLRetrieveView

app_name = "shortener"

urlpatterns = [
    path("", ShortenedURLCreateView.as_view(), name="shorten"),
    # keep this at the end to avoid conflicts with other paths
    path("<str:short_code>/", ShortenedURLRetrieveView.as_view(), name="resolve"),
]
