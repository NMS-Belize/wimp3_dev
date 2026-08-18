import json

from django.conf import settings
from django.core.management.base import BaseCommand

from agro.models import PestRiskEffect, Commodity

class Command(BaseCommand):

    help = "Import Effects from JSON"

    def handle(self, *args, **kwargs):

        results = []

        # Load Effects from JSON file and create/update Effects objects
        with open(settings.BASE_DIR / "agro" / "data" / "effects.json", encoding="utf-8") as f:
            effects = json.load(f)

        for item in effects:

            commodity_id = item.get("commodity")
            
            if not Commodity.objects.filter(pk=commodity_id).exists():
                self.stdout.write(self.style.WARNING(f'Skipping pest-risk ID {item["id"]}: Commodity ID {commodity_id} does not exist.'))
                continue
            
            PestRiskEffect.objects.update_or_create(
                id = item["id"],
                defaults={
                    "effect_description": item["effect_description"],
                    "commodity_id": commodity_id,
                },
            )

        #results.append("Agro Data [Pest Risk Effects] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Agro Data [Pest Risk Effects] imported successfully."))