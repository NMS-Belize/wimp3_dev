import json

from django.conf import settings
from django.core.management.base import BaseCommand

from agro.models import PestRiskInfo, Sector

class Command(BaseCommand):
    
    help = "Import Pest Risk Info from JSON"

    def handle(self, *args, **kwargs):

        results = []

        # Load Info from JSON file and create/update Info objects
        with open(settings.BASE_DIR / "agro" / "data" / "additional_info.json", encoding="utf-8") as f:
            alert_levels = json.load(f)

        for item in alert_levels:

            sector_id = item.get("sector")
                        
            if not Sector.objects.filter(pk=sector_id).exists():
                self.stdout.write(self.style.WARNING(f'Skipping pest-risk ID {item["id"]}: Sector ID {sector_id} does not exist.'))
                continue
            
            PestRiskInfo.objects.update_or_create(
                id = item["id"],
                defaults={
                    "info_description": item["info_description"],
                    "sector_id": sector_id,
                }
            )

        results.append("Agro Data [Pest Risk Info] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Agro Data [Pest Risk Info] imported successfully."))