import json

from datetime import datetime
from email.utils import parsedate_to_datetime

from django.core.management.base import BaseCommand
from alerts.models import CAPAlerts, CAPAlertDetails


class Command(BaseCommand):
    help = "Restore CAP alert dates after migration"

    def handle(self, *args, **kwargs):

        filename = "cap_dates_backup.json"

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        pubdate_count = 0
        expires_count = 0

        # ---------------------------------------
        # Restore pubdate
        # ---------------------------------------
        for item in data.get("alerts", []):

            value = item.get("pubdate")

            if not value:
                continue

            try:
                dt = parsedate_to_datetime(value)

                updated = CAPAlerts.objects.filter(
                    guid=item["guid"]
                ).update(
                    pubdate=dt
                )

                pubdate_count += updated

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"Could not restore pubdate "
                        f"{item['guid']}: {value} - {e}"
                    )
                )

        # ---------------------------------------
        # Restore expires
        # ---------------------------------------
        for item in data.get("details", []):

            value = item.get("expires")

            if not value:
                continue

            try:
                dt = datetime.fromisoformat(value)

                updated = CAPAlertDetails.objects.filter(
                    identifier_id=item["identifier"]
                ).update(
                    expires=dt
                )

                expires_count += updated

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"Could not restore expires "
                        f"{item['identifier']}: {value} - {e}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Restored {pubdate_count} pubdates and "
                f"{expires_count} expiration dates."
            )
        )