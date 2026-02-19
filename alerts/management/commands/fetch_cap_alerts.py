from django.core.management.base import BaseCommand
from alerts.utils.cap_rss import fetch_cap_alerts

class Command(BaseCommand):
    help = "Fetch CAP alerts from Belize NMS RSS feed"

    def handle(self, *args, **kwargs):
        fetch_cap_alerts()
        self.stdout.write(self.style.SUCCESS("CAP alerts fetched successfully"))