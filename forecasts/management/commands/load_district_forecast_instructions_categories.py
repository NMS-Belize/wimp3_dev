import json

from django.conf import settings
from django.core.management.base import BaseCommand

from agro.models import PestRiskAction

class Command(BaseCommand):
    
    help = "Import Pest Risk Actions from JSON"

    def handle(self, *args, **kwargs):

        results = []

        # Load Actions from JSON file and create/update Actions objects
        with open(settings.BASE_DIR / "agro" / "data" / "actions.json", encoding="utf-8") as f:
            alert_levels = json.load(f)

        for item in alert_levels:
            PestRiskAction.objects.update_or_create(
                id = item["id"],
                defaults={
                    "action_description": item["action_description"]
                },
            )

        results.append("Agro Data [Pest Risk Actions] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Agro Data [Pest Risk Actions] imported successfully."))