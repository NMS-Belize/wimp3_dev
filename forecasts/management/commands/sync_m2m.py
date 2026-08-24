import json

from django.core.management.base import BaseCommand
from forecasts.models import (ForecastGeneral, WindDirection, WindCondition, SeaState)

class Command(BaseCommand):

    help = "Clear and repopulate ForecastGeneral M2M fields from legacy fields"

    def handle(self, *args, **options):

        field_map = [
            ("wind_direction", "wind_direction_m2m", WindDirection),
            ("wind_condition", "wind_condition_m2m", WindCondition),
            ("wind_shift_direction", "wind_shift_direction_m2m", WindDirection),
            ("wind_shift_condition", "wind_shift_condition_m2m", WindCondition),
            ("sea_state", "sea_state_m2m", SeaState),
            ("sea_state_shift", "sea_state_shift_m2m", SeaState),
        ]

        def parse_ids(value):
            if not value:
                return []

            value = str(value).strip()

            try:
                result = json.loads(value)

                if isinstance(result, list):
                    return result

                if isinstance(result, int):
                    return [result]

            except (json.JSONDecodeError, TypeError):
                pass

            try:
                return [
                    int(x.strip())
                    for x in value.split(",")
                    if x.strip()
                ]
            except ValueError:
                return []

        # STEP 1: CLEAR ALL M2M RELATIONSHIPS
        self.stdout.write("Clearing all M2M relationships...")

        for forecast in ForecastGeneral.objects.all():
            forecast.wind_direction_m2m.clear()
            forecast.wind_condition_m2m.clear()
            forecast.wind_shift_direction_m2m.clear()
            forecast.wind_shift_condition_m2m.clear()
            forecast.sea_state_m2m.clear()
            forecast.sea_state_shift_m2m.clear()

        self.stdout.write(self.style.SUCCESS("All M2M relationships cleared."))

        # STEP 2: REPOPULATE FROM LEGACY FIELDS
        self.stdout.write("Repopulating M2M relationships...")

        for forecast in ForecastGeneral.objects.all():

            for legacy_field, m2m_field, related_model in field_map:

                raw_value = getattr(forecast, legacy_field)

                if not raw_value:
                    continue

                ids = parse_ids(raw_value)

                if not ids:
                    self.stdout.write(
                        self.style.WARNING(
                            f"SKIPPED {forecast.id} | "
                            f"{legacy_field}={raw_value}"
                        )
                    )
                    continue

                objects = related_model.objects.filter(id__in=ids)

                manager = getattr(forecast, m2m_field)
                manager.set(objects)

                self.stdout.write(
                    f"{forecast.id} | "
                    f"{m2m_field} -> "
                    f"{list(objects.values_list('id', flat=True))}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Finished repopulating all M2M fields."
            )
        )