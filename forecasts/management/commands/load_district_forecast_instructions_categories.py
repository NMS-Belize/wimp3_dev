import json

from django.conf import settings
from django.core.management.base import BaseCommand

from forecasts.models import DistrictForecastInstructionsCategory

class Command(BaseCommand):
    
    help = "Import Pest Risk Actions from JSON"

    def handle(self, *args, **kwargs):

        results = []

        # Load Actions from JSON file and create/update Actions objects
        with open(settings.BASE_DIR / "forecasts" / "data" / "forecast_district_instructions_categories.json", encoding="utf-8") as f:

            categories = json.load(f)

        for item in categories:
            DistrictForecastInstructionsCategory.objects.update_or_create(
                id = item["id"],
                defaults={
                    "category_name": item["category_name"]
                },
            )

        results.append("District Forecast [Instructions Categories] imported successfully.")
        self.stdout.write(self.style.SUCCESS("District Forecast [Instructions Categories] imported successfully."))