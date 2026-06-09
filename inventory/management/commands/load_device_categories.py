# forecasts/management/commands/load_device_categories.py

from django.core.management.base import BaseCommand
from ...models import InventoryCategory
from pathlib import Path
import json

class Command(BaseCommand):
    help = "Load Device Categories from a JSON file"

    def handle(self, *args, **kwargs):

    # Build absolute path safely
        json_path = Path("data/device_categories.json")

        # Check file exists
        if not json_path.exists():
            self.stdout.write(
                self.style.ERROR(f"File not found: {json_path}")
            )
            return

        # Load JSON
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        created_count = 0
        updated_count = 0

        for item in data:

            obj, created = InventoryCategory.objects.update_or_create(
                name=item["name"],
                defaults={
                    "name": item["name"]
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Device Categories loaded "
                f"(Created: {created_count}, Updated: {updated_count})"
            )
        )