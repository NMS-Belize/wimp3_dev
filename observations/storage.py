# observations/storage.py

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pathlib import Path

weather_icon_storage = FileSystemStorage(
    location=Path(settings.BASE_DIR) / "static",
    base_url=settings.STATIC_URL,
)