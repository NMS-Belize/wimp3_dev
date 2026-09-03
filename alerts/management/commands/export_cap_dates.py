import json

from django.core.management.base import BaseCommand
from alerts.models import CAPAlerts, CAPAlertDetails


class Command(BaseCommand):
    help = "Export CAP alert date values before migration"

    def handle(self, *args, **kwargs):

        data = {
            "alerts": [],
            "details": [],
        }

        for alert in CAPAlerts.objects.all():
            data["alerts"].append({
                "guid": alert.guid,
                "pubdate": alert.pubdate,
            })

        for detail in CAPAlertDetails.objects.all():
            data["details"].append({
                "identifier": detail.identifier_id,
                "expires": detail.expires,
            })

        filename = "cap_dates_backup.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=str)

        self.stdout.write(
            self.style.SUCCESS(
                f"CAP dates exported to {filename}"
            )
        )