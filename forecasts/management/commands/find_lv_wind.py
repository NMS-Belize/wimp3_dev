from django.core.management.base import BaseCommand
from django.db import transaction

from forecasts.models import ForecastMarineDetails


class Command(BaseCommand):

    help = (
        "Set wind_condition='Light + Variable' for ForecastMarineDetails "
        "where legacy wind_direction contains 'Light + Va'"
    )

    def handle(self, *args, **options):

        search_value = "Light + Va"
        condition_value = "Light + Variable"

        records = (
            ForecastMarineDetails.objects
            .filter(
                wind_direction__icontains=search_value
            )
            .select_related(
                "marine_forecast",
                "marine_category",
            )
            .order_by(
                "marine_forecast_id",
                "marine_category_id",
            )
        )

        total = records.count()

        self.stdout.write("")
        self.stdout.write("=" * 75)
        self.stdout.write("LIGHT + VARIABLE WIND CONDITION UPDATE")
        self.stdout.write("=" * 75)

        self.stdout.write(
            f"Search wind_direction for : {search_value}"
        )

        self.stdout.write(
            f"Set wind_condition to      : {condition_value}"
        )

        self.stdout.write(
            f"Matching records           : {total}"
        )

        if total == 0:
            self.stdout.write(
                self.style.WARNING(
                    "\nNo matching records found."
                )
            )
            return

        updated = 0
        skipped = 0

        with transaction.atomic():

            for record in records:

                self.stdout.write("")
                self.stdout.write("-" * 75)

                self.stdout.write(
                    f"ID                : {record.id}"
                )

                self.stdout.write(
                    f"Marine Forecast   : {record.marine_forecast_id}"
                )

                self.stdout.write(
                    f"Category          : {record.marine_category}"
                )

                self.stdout.write(
                    f"Wind Direction    : {record.wind_direction}"
                )

                self.stdout.write(
                    f"Old Wind Condition: {record.wind_condition}"
                )

                # Already correct
                if (
                    record.wind_condition
                    and record.wind_condition.strip().lower()
                    == condition_value.lower()
                ):

                    skipped += 1

                    self.stdout.write(
                        self.style.WARNING(
                            "SKIPPED: Already set to Light + Variable"
                        )
                    )

                    continue

                # Set actual text value
                record.wind_condition = condition_value

                record.save(
                    update_fields=[
                        "wind_condition",
                        "updated_datetime",
                    ]
                )

                updated += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        "UPDATED: wind_condition = Light + Variable"
                    )
                )

        self.stdout.write("")
        self.stdout.write("=" * 75)
        self.stdout.write("SUMMARY")
        self.stdout.write("=" * 75)

        self.stdout.write(
            f"Found   : {total}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Updated : {updated}"
            )
        )

        self.stdout.write(
            f"Skipped : {skipped}"
        )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Update completed successfully."
            )
        )