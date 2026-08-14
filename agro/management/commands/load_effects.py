import json

from django.conf import settings
from django.core.management.base import BaseCommand

from agro.models import PestRiskEffect, Sector

class Command(BaseCommand):

    help = "Import Effects from JSON"

    def handle(self, *args, **kwargs):

        results = []

        # Load Effects from JSON file and create/update Effects objects
        with open(settings.BASE_DIR / "agro" / "data" / "effects.json", encoding="utf-8") as f:
            effects = json.load(f)

        for item in effects:

            sector_id = item.get("sector")
            
            if not Sector.objects.filter(pk=sector_id).exists():
                self.stdout.write(self.style.WARNING(f'Skipping pest-risk ID {item["id"]}: Sector ID {sector_id} does not exist.'))
                continue
            
            PestRiskEffect.objects.update_or_create(
                id = item["id"],
                defaults={
                    "effect_description": item["effect_description"],
                    "sector_id": sector_id,
                },
            )

        results.append("Agro Data [Pest Risk Effects] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Agro Data [Pest Risk Effects] imported successfully."))