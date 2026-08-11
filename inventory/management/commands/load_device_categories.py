# forecasts/management/commands/load_device_categories.py

from django.core.management.base import BaseCommand
from django.conf import settings

from ...models import InventoryCategory
from pathlib import Path
import json

class Command(BaseCommand):
    help = "Load Device Categories from a JSON file"

    def handle(self, *args, **kwargs):

        # Load Device Category from JSON file and create/update Sector objects
        with open(
            settings.BASE_DIR / "inventory" / "data" / "device_categories.json",
            encoding="utf-8"
        ) as f:
            items = json.load(f)

        for item in items:
            InventoryCategory.objects.update_or_create(
                id = item["id"],
                defaults={
                    "name": item["name"],
                    "description": item["description"],
                },
            )

        self.stdout.write(self.style.SUCCESS("Inventory Data [Device Categories] imported successfully."))