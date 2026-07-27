import json

from distro import name
from django.conf import settings
from django.core.management.base import BaseCommand

from agro.models import Sector, Commodity

class Command(BaseCommand):
    help = "Import sectors from JSON"

    def handle(self, *args, **kwargs):

        # Load Sector from JSON file and create/update Sector objects
        with open(
            settings.BASE_DIR / "agro" / "data" / "sectors.json",
            encoding="utf-8"
        ) as f:
            sectors = json.load(f)

        for item in sectors:
            Sector.objects.update_or_create(
                id = item["id"],
                defaults={
                    "description": item["description"],
                },
            )

        # Load Commodity from JSON file and create/update Commodity objects
        with open(
            settings.BASE_DIR / "agro" / "data" / "commodity.json",
            encoding="utf-8"
        ) as f:
            commodities = json.load(f)

        for item in commodities:
            Commodity.objects.update_or_create(
                id = item["id"],
                defaults={
                    "description": item["description"],
                    "sector_id": item["sector"],
                },
            )

        self.stdout.write(
            self.style.SUCCESS("System data imported successfully.")
        )