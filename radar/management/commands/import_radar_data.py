import json

from distro import name
from django.conf import settings
from django.contrib import messages
from django.core.management.base import BaseCommand

from radar.models import RadarImages
from system_core.models import District

class Command(BaseCommand):
    help = "Import radar images from JSON"

    def handle(self, *args, **kwargs):

        results = []

        # Load RadarImages from JSON file and create/update RadarImages objects
        with open(
            settings.BASE_DIR / "radar" / "data" / "radar_images.json",
            encoding="utf-8"
        ) as f:
            radar_images = json.load(f)

        for item in radar_images:
            RadarImages.objects.update_or_create(
                id = item["id"],
                defaults={
                    "image_url": item["image_url"],
                    "web_directory": item["web_directory"],
                    "image_title": item["image_title"]
                },
            )

        results.append("Radar Images imported successfully.")
        self.stdout.write(self.style.SUCCESS("Radar Images imported successfully."))

        