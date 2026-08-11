# forecasts/management/commands/load_device_categories.py

from django.core.management.base import BaseCommand
from django.conf import settings

from ...models import DeviceType
from pathlib import Path
import json

class Command(BaseCommand):
    help = "Load Device Types from a JSON file"

    def handle(self, *args, **kwargs):

        results = []

        # Load Sector from JSON file and create/update Sector objects
        with open(
            settings.BASE_DIR / "inventory" / "data" / "device_types.json",
            encoding="utf-8"
        ) as f:
            items = json.load(f)

        for item in items:
            DeviceType.objects.update_or_create(
                id = item["id"],
                defaults={
                    "name": item["name"],
                    "inventory_category_id": item["inventory_category"],
                },
            )

        #results.append("Inventory Data [Device Types] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Inventory Data [Device Types] imported successfully."))