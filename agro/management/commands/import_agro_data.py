import json

from distro import name
from django.conf import settings
from django.contrib import messages
from django.core.management.base import BaseCommand

from agro.models import Sector, Commodity, PestRiskEntryMainListing, PestRisk, PestRiskEntryDetails, DroughtAlertLevel, PestRiskAction, PestRiskEffect
from system_core.models import District

class Command(BaseCommand):
    help = "Import sectors from JSON"

    def handle(self, *args, **kwargs):

        results = []

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

        results.append("Agro Data [Sectors] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Agro Data [Sectors] imported successfully."))

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

        results.append("Agro Data [Commodities] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Agro Data [Commodities] imported successfully."))

        # Load AlertLevel from JSON file and create/update AlertLevel objects
        with open(
            settings.BASE_DIR / "agro" / "data" / "drought_alert_levels.json",
            encoding="utf-8"
        ) as f:
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

        # Load AlertLevel from JSON file and create/update AlertLevel objects
        with open(
            settings.BASE_DIR / "agro" / "data" / "actions.json",
            encoding="utf-8"
        ) as f:
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

        # Load AlertLevel from JSON file and create/update AlertLevel objects
        with open(
            settings.BASE_DIR / "agro" / "data" / "effects.json",
            encoding="utf-8"
        ) as f:
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

        # Load Commodity from JSON file and create/update Commodity objects
        with open(
            settings.BASE_DIR / "agro" / "data" / "pest_risk.json",
            encoding="utf-8"
        ) as f:
            pr = json.load(f)

        for item in pr:
            commodity_id = item.get("commodity")

            if not Commodity.objects.filter(pk=commodity_id).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f'Skipping pest-risk ID {item["id"]}: '
                        f"Commodity ID {commodity_id} does not exist."
                    )
                )
                continue

            PestRiskEntryMainListing.objects.update_or_create(
                id=item["id"],
                defaults={
                    "commodity_id": commodity_id,
                    "months": ["1", "2", "3"],
                    "year": "2026"
                },
            )

        results.append("Agro Data [Pest Risk Main Listings] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Agro Data [Pest Risk Main Listings] imported successfully."))

        # Load District Entries from JSON file and create/update PestRiskDeatils objects
        with open(
            settings.BASE_DIR / "agro" / "data" / "pest_risk_details.json",
            encoding="utf-8"
        ) as f:
            pr = json.load(f)

        for item in pr:
            commodity_id = item.get("commodity")
            district_id = item.get("district")
            pest_risk_id = item.get("pest_risk_id")

            if not Commodity.objects.filter(pk=commodity_id).exists():
                self.stdout.write(
                    self.style.WARNING(f'Skipping Commodity ID {item["id"]}: 'f"Commodity ID {commodity_id} does not exist.")
                )
                continue

            if not District.objects.filter(pk=district_id).exists():
                self.stdout.write(
                    self.style.WARNING(f'Skipping District ID {item["id"]}: 'f"District ID {district_id} does not exist.")
                )
                continue

            if not PestRisk.objects.filter(pk=pest_risk_id).exists():
                self.stdout.write(
                    self.style.WARNING(f'Skipping pest-risk ID {item["id"]}: 'f"Pest Risk ID {pest_risk_id} does not exist.")
                )
                continue

            PestRiskEntryDetails.objects.update_or_create(
                id=item["id"],
                defaults={
                    "pest_risk_id_id": pest_risk_id,
                    "commodity_id_id": commodity_id,
                    "district_id_id": district_id,
                },
            )

        results.append("Agro Data [Pest Risk Details] imported successfully.")
        self.stdout.write(self.style.SUCCESS("Agro Data [Pest Risk Details] imported successfully."))