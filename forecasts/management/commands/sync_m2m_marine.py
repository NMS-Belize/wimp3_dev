from django.core.management.base import BaseCommand

from forecasts.models import (
    ForecastMarineDetails,
    WindDirection,
    SeaState,
)


class Command(BaseCommand):

    help = (
        "Clear and repopulate ForecastMarineDetails "
        "M2M fields from legacy description fields"
    )

    def handle(self, *args, **options):

        # ---------------------------------------------------------
        # FIELD CONFIGURATION
        # ---------------------------------------------------------

        field_map = [
            ("wind_direction","wind_direction_m2m",WindDirection,"-"),
            ("sea_state","sea_state_m2m",SeaState," - ")
        ]

        # ---------------------------------------------------------
        # BUILD LOOKUPS
        # ---------------------------------------------------------
        # This prevents querying the database repeatedly for
        # every ForecastMarineDetails record.
        #
        # Example:
        #
        # wind_lookup:
        # {
        #     "E": WindDirection(E),
        #     "SE": WindDirection(SE),
        # }
        #
        # sea_lookup:
        # {
        #     "LIGHT CHOP": SeaState(Light Chop),
        #     "CHOPPY": SeaState(Choppy),
        # }

        lookups = {
            WindDirection: {
                obj.description.strip().upper(): obj
                for obj in WindDirection.objects.all()
                if obj.description
            },

            SeaState: {
                obj.description.strip().upper(): obj
                for obj in SeaState.objects.all()
                if obj.description
            },
        }

        # ---------------------------------------------------------
        # PARSE DESCRIPTION VALUES
        # ---------------------------------------------------------

        def parse_descriptions(value, separator, related_model):

            if not value:
                return [], []

            value = str(value).strip()

            lookup = lookups[related_model]

            # -----------------------------------------------------
            # FIRST TRY EXACT MATCH
            # -----------------------------------------------------
            #
            # Important for values such as:
            #
            # Light Chop
            # Slight
            # Choppy
            # Moderate
            # Rough
            # E
            # SE
            #
            # If the entire value exists in the lookup table,
            # don't split it.

            normalized_value = value.upper()

            if normalized_value in lookup:
                return [lookup[normalized_value]], []

            # SPLIT COMBINATION VALUE
            parts = [
                part.strip()
                for part in value.split(separator)
                if part.strip()
            ]

            objects = []
            missing = []

            for part in parts:

                normalized_part = part.upper()

                obj = lookup.get(normalized_part)

                if obj:
                    objects.append(obj)
                else:
                    missing.append(part)

            return objects, missing

        # STEP 1: CLEAR ALL M2M RELATIONSHIPS
        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write("FORECAST MARINE DETAILS M2M SYNC")
        self.stdout.write("=" * 70)

        queryset = ForecastMarineDetails.objects.all()

        total_records = queryset.count()

        self.stdout.write(f"Records found: {total_records}")
        self.stdout.write("")
        self.stdout.write("Clearing all M2M relationships...")

        for forecast in queryset.iterator():
            forecast.wind_direction_m2m.clear()
            forecast.sea_state_m2m.clear()

        self.stdout.write(self.style.SUCCESS("All M2M relationships cleared."))

        # STEP 2: REPOPULATE FROM LEGACY FIELDS
        self.stdout.write("")
        self.stdout.write("Repopulating M2M relationships...")
        self.stdout.write("")

        updated = 0
        skipped = 0
        missing_count = 0

        for forecast in queryset.iterator():

            for (legacy_field, m2m_field, related_model, separator) in field_map:

                raw_value = getattr(forecast, legacy_field, None)

                if not raw_value:
                    continue

                # PARSE DESCRIPTION
                objects, missing = parse_descriptions(raw_value, separator, related_model)

                # REPORT MISSING VALUES
                if missing:
                    missing_count += len(missing)
                    self.stdout.write(
                        self.style.WARNING(
                            f"MISSING | ForecastMarineDetails ID={forecast.id} | {legacy_field}={raw_value} | Not found={missing} MID: {forecast.marine_forecast}"
                        )
                    )

                # SET M2M
                if objects:

                    manager = getattr(forecast, m2m_field)
                    manager.set(objects)

                    descriptions = [
                        obj.description
                        for obj in objects
                    ]

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"UPDATED | "
                            f"ForecastMarineDetails ID={forecast.id} | "
                            f"{legacy_field}={raw_value} -> "
                            f"{descriptions}"
                        )
                    )
                    updated += 1

                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"SKIPPED | "
                            f"ForecastMarineDetails ID={forecast.id} | "
                            f"{legacy_field}={raw_value}"
                        )
                    )
                    skipped += 1

        # SUMMARY

        self.stdout.write("")
        self.stdout.write("-" * 70)

        self.stdout.write("ForecastMarineDetails COMPLETE")

        self.stdout.write(f"Records:       {total_records}")

        self.stdout.write(
            f"M2M Updated:   {updated}"
        )

        self.stdout.write(
            f"Skipped:       {skipped}"
        )

        self.stdout.write(
            f"Missing:       {missing_count}"
        )

        self.stdout.write("-" * 70)

        if skipped == 0 and missing_count == 0:

            self.stdout.write(
                self.style.SUCCESS(
                    "ALL M2M RELATIONSHIPS SUCCESSFULLY REPOPULATED"
                )
            )

        else:

            self.stdout.write(
                self.style.WARNING(
                    "M2M SYNC COMPLETED WITH SKIPPED/MISSING VALUES"
                )
            )

        self.stdout.write("=" * 70)