# forecasts/management/commands/load_device_categories.py

from django.core.management.base import BaseCommand
from django.conf import settings

from ...models import TropicalWeatherAlertsCategory
from pathlib import Path
import json

class Command(BaseCommand):
    help = "Tropical Weather Alert Categories from a JSON file"

    def handle(self, *args, **kwargs):

        # Load Tropical Weather Alert Categories from JSON file and create/update Sector objects
        with open(
            settings.BASE_DIR / "alerts" / "data" / "tropical_alerts_categories.json",
            encoding="utf-8"
        ) as f:
            items = json.load(f)

        for item in items:
            TropicalWeatherAlertsCategory.objects.update_or_create(
                id = item["id"],
                defaults={
                    "category_name": item["category_name"],
                },
            )

        self.stdout.write(self.style.SUCCESS("Alert Data [Tropical Weather Alert Categories] imported successfully."))