import json

from distro import name
from django.conf import settings
from django.core.management.base import BaseCommand

from system_core.models import District, AlertLevel, JobTitle, Months, RiskLevel, Zone, DepartmentSection, OfficeLocation

class Command(BaseCommand):
    help = "Import districts from JSON"

    def handle(self, *args, **kwargs):

        # Load AlertLevel from JSON file and create/update AlertLevel objects
        with open(
            settings.BASE_DIR / "system_core" / "data" / "months.json",
            encoding="utf-8"
        ) as f:
            alert_levels = json.load(f)

        for item in alert_levels:
            Months.objects.update_or_create(
                id = item["id"],
                defaults={
                    "month_name": item["month_name"],
                    "short_name": item["short_name"],
                },
            )

        self.stdout.write(
            self.style.SUCCESS("System Data [Months] imported successfully.")
        )

        # Load AlertLevel from JSON file and create/update AlertLevel objects
        with open(
            settings.BASE_DIR / "system_core" / "data" / "zones.json",
            encoding="utf-8"
        ) as f:
            alert_levels = json.load(f)

        for item in alert_levels:
            Zone.objects.update_or_create(
                id = item["id"],
                defaults={
                    "zone_name": item["zone_name"],
                },
            )

        self.stdout.write(
            self.style.SUCCESS("System Data [Zones] imported successfully.")
        )

        # Load districts from JSON file and create/update District objects
        with open(
            settings.BASE_DIR / "system_core" / "data" / "districts.json",
            encoding="utf-8"
        ) as f:
            districts  = json.load(f)

        for item in districts :
            District.objects.update_or_create(
                id = item["id"],
                defaults={
                    "district_name": item["district_area"],
                },
            )

        self.stdout.write(
            self.style.SUCCESS("System Data [Districts] imported successfully.")
        )

        # Load RiskLevel from JSON file and create/update RiskLevel objects
        with open(
            settings.BASE_DIR / "system_core" / "data" / "risk_levels.json",
            encoding="utf-8"
        ) as f:
            risk_levels = json.load(f)

        for item in risk_levels:
            RiskLevel.objects.update_or_create(
                id = item["id"],
                defaults={
                    "description": item["description"],
                    "color": item["color"],
                },
            )

        self.stdout.write(
            self.style.SUCCESS("System Data [Risk Levels] imported successfully.")
        )

        # Load AlertLevel from JSON file and create/update AlertLevel objects
        with open(
            settings.BASE_DIR / "system_core" / "data" / "alert_levels.json",
            encoding="utf-8"
        ) as f:
            alert_levels = json.load(f)

        for item in alert_levels:
            AlertLevel.objects.update_or_create(
                id = item["id"],
                defaults={
                    "description": item["description"],
                    "color": item["color"],
                },
            )

        self.stdout.write(
            self.style.SUCCESS("System Data [Alert Levels] imported successfully.")
        )

        # Load AlertLevel from JSON file and create/update AlertLevel objects
        with open(
            settings.BASE_DIR / "system_core" / "data" / "departments.json",
            encoding="utf-8"
        ) as f:
            dept = json.load(f)

        for item in dept:
            DepartmentSection.objects.update_or_create(
                id = item["id"],
                defaults={
                    "name": item["name"],
                    "short_name": item["short_name"],
                },
            )

        self.stdout.write(
            self.style.SUCCESS("System Data [Departments] imported successfully.")
        )

        # Load Job Titles from JSON file and create/update JobTitle objects
        with open(
            settings.BASE_DIR / "system_core" / "data" / "job_titles.json",
            encoding="utf-8"
        ) as f:
            job_titles = json.load(f)

        for item in job_titles:
            JobTitle.objects.update_or_create(
                id = item["id"],
                defaults={
                    "description": item["description"]
                },
            )

        self.stdout.write(
            self.style.SUCCESS("System Data [Job Titles] imported successfully.")
        )

        # Load Office Locations from JSON file and create/update OfficeLocation objects
        with open(
            settings.BASE_DIR / "system_core" / "data" / "office_location.json",
            encoding="utf-8"
        ) as f:
            office_locations = json.load(f)

        for item in office_locations:
            OfficeLocation.objects.update_or_create(
                id = item["id"],
                defaults={
                    "name": item["name"],
                    "floor": item.get("floor"),
                    "description": item.get("description", "")
                },
            )

        self.stdout.write(
            self.style.SUCCESS("System Data [Office Locations] imported successfully.")
        )