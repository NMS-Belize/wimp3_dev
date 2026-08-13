import json

from django.conf import settings
from django.core.management.base import BaseCommand

from agro.models import Commodity

class Command(BaseCommand):
    help = "Import Commodities from JSON"

    def handle(self, *args, **kwargs):

        results = []

        # Load Commodities from JSON file and create/update Commodity objects
        with open(settings.BASE_DIR / "agro" / "data" / "commodity.json", encoding="utf-8") as f:
            commodities = json.load(f)

        for item in commodities:
            Commodity.objects.update_or_create(
                id = item["id"],
                defaults={
                    "description": item["description"],
                    "sector_id": item["sector"],
                },
            )

        results.append("Agro Data [Commodities] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Agro Data [Commodities] imported successfully."))