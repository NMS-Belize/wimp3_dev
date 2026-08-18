import json

from django.conf import settings
from django.core.management.base import BaseCommand

from agro.models import PestRiskAction, Commodity

class Command(BaseCommand):
    
    help = "Import Pest Risk Actions from JSON"

    def handle(self, *args, **kwargs):

        results = []

        # Load Actions from JSON file and create/update Actions objects
        with open(settings.BASE_DIR / "agro" / "data" / "actions.json", encoding="utf-8") as f:
            alert_levels = json.load(f)

        for item in alert_levels:

            commodity_id = item.get("commodity")
                        
            if not Commodity.objects.filter(pk=commodity_id).exists():
                self.stdout.write(self.style.WARNING(f'Skipping pest-risk ID {item["id"]}: Commodity ID {commodity_id} does not exist.'))
                continue
            
            PestRiskAction.objects.update_or_create(
                id = item["id"],
                defaults={
                    "action_description": item["action_description"],
                    "commodity_id": commodity_id,
                },
            )

        #results.append("Agro Data [Pest Risk Actions] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Agro Data [Pest Risk Actions] imported successfully."))