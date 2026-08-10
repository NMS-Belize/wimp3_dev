import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from forecasts.models import ForescastGeneralCategory

class Command(BaseCommand):
    help = "Import General Weather Forecast Categories from JSON"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        try:
            system_user = User.objects.get(username="smatura")
        except User.DoesNotExist:
            self.stderr.write(
                self.style.ERROR('User "smatura" does not exist. Create the user or change the username.')
            )
            return

        file_path = (settings.BASE_DIR / "forecasts" / "data" / "forecast_general_category.json")

        try:
            with open(file_path, encoding="utf-8") as file:
                categories = json.load(file)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"JSON file not found: {file_path}"))
            return
        except json.JSONDecodeError as error:
            self.stderr.write(self.style.ERROR(f"Invalid JSON: {error}"))
            return

        created_count = 0
        updated_count = 0

        for item in categories:
            obj, created = ForescastGeneralCategory.objects.update_or_create(
                id=item["id"],
                defaults={
                    "description": item["description"],
                    "updated_by": system_user,
                },
            )

            if created:
                obj.created_by = system_user
                obj.save(update_fields=["created_by"])
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                "General Weather Forecast Categories imported successfully. "
                f"Created: {created_count}, Updated: {updated_count}."
            )
        )