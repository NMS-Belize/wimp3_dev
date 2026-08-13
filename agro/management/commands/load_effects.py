import json

from django.conf import settings
from django.core.management.base import BaseCommand

from agro.models import PestRiskEffect

class Command(BaseCommand):

    help = "Import Effects from JSON"

    def handle(self, *args, **kwargs):

        results = []

        # Load Effects from JSON file and create/update Effects objects
        with open(settings.BASE_DIR / "agro" / "data" / "effects.json", encoding="utf-8") as f:
            alert_levels = json.load(f)

        for item in alert_levels:
            PestRiskEffect.objects.update_or_create(
                id = item["id"],
                defaults={
                    "effect_description": item["effect_description"]
                },
            )

        results.append("Agro Data [Pest Risk Effects] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Agro Data [Pest Risk Effects] imported successfully."))