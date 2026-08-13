import json

from django.conf import settings
from django.core.management.base import BaseCommand

from agro.models import DroughtAlertLevel

class Command(BaseCommand):
    help = "Import sectors from JSON"

    def handle(self, *args, **kwargs):

        results = []

        # Load Drought Alert Levels from JSON file and create/update Drought Alert Levels objects
        with open(settings.BASE_DIR / "agro" / "data" / "drought_alert_levels.json", encoding="utf-8") as f:
            alert_levels = json.load(f)

        for item in alert_levels:
            DroughtAlertLevel.objects.update_or_create(
                id = item["id"],
                defaults={
                    "description": item["description"],
                    "color_hex": item["color_hex"],
                },
            )

        results.append("Agro Data [Drought Alert Levels] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Agro Data [Drought Alert Levels] imported successfully."))