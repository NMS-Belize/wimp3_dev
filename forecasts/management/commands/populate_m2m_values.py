from django.core.management.base import BaseCommand
from django.db import transaction

from forecasts.models import (
    ForecastMarineDetails,
    WindDirection,
    SeaState,
)


class Command(BaseCommand):

    help = (
        "Populate ForecastMarineDetails wind_direction_m2m and "
        "sea_state_m2m from legacy fields."
    )

    # ============================================================
    # WIND DIRECTION
    # ============================================================

    def match_wind_directions(self, legacy_value):
        """
        Convert legacy wind direction values to WindDirection objects.

        Examples:

            E       -> E
            SE      -> SE
            E-SE    -> E, SE
            NE-E    -> NE, E
            S-SW    -> S, SW
            W-NW    -> W, NW

        WindDirection table contains:
            N, NE, E, SE, S, SW, W, NW
        """

        if not legacy_value:
            return [], []

        legacy_value = str(legacy_value).strip().upper()

        if not legacy_value:
            return [], []

        # Legacy compound wind directions are separated by "-"
        parts = [
            part.strip()
            for part in legacy_value.split("-")
            if part.strip()
        ]

        matches = []
        unmatched = []

        for part in parts:

            obj = WindDirection.objects.filter(
                description__iexact=part
            ).first()

            if obj:
                # Prevent duplicates
                if obj.pk not in [item.pk for item in matches]:
                    matches.append(obj)

            else:
                unmatched.append(part)

        return matches, unmatched

    # ============================================================
    # SEA STATE
    # ============================================================

    def match_sea_states(self, legacy_value):
        """
        Convert legacy sea state values to SeaState objects.

        Examples:

            Choppy
                -> Choppy

            Light Chop - Choppy
                -> Light Chop, Choppy

            Choppy - Moderate
                -> Choppy, Moderate

        IMPORTANT:
        Sea State uses " - " as the separator rather than simply "-".
        """

        if not legacy_value:
            return [], []

        legacy_value = str(legacy_value).strip()

        if not legacy_value:
            return [], []

        # --------------------------------------------------------
        # Try the complete value first
        # --------------------------------------------------------

        exact_match = SeaState.objects.filter(
            description__iexact=legacy_value
        ).first()

        if exact_match:
            return [exact_match], []

        # --------------------------------------------------------
        # Compound Sea State
        #
        # Light Chop - Choppy
        # becomes:
        # Light Chop
        # Choppy
        # --------------------------------------------------------

        parts = [
            part.strip()
            for part in legacy_value.split(" - ")
            if part.strip()
        ]

        matches = []
        unmatched = []

        for part in parts:

            obj = SeaState.objects.filter(
                description__iexact=part
            ).first()

            if obj:

                # Prevent duplicates
                if obj.pk not in [item.pk for item in matches]:
                    matches.append(obj)

            else:
                unmatched.append(part)

        return matches, unmatched

    # ============================================================
    # HANDLE
    # ============================================================

    def handle(self, *args, **options):

        records = ForecastMarineDetails.objects.all().order_by("id")

        total_records = records.count()

        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write("POPULATE MARINE FORECAST M2M VALUES")
        self.stdout.write("=" * 70)

        self.stdout.write(
            f"Found {total_records} ForecastMarineDetails records."
        )

        self.stdout.write("")

        # --------------------------------------------------------
        # Counters
        # --------------------------------------------------------

        processed = 0

        wind_updated = 0
        sea_updated = 0

        wind_unmatched_count = 0
        sea_unmatched_count = 0

        wind_unmatched_values = set()
        sea_unmatched_values = set()

        # ========================================================
        # PROCESS RECORDS
        # ========================================================

        for record in records:

            # ----------------------------------------------------
            # WIND DIRECTION
            # ----------------------------------------------------

            wind_objects, wind_unmatched = self.match_wind_directions(
                record.wind_direction
            )

            # ----------------------------------------------------
            # SEA STATE
            # ----------------------------------------------------

            sea_objects, sea_unmatched = self.match_sea_states(
                record.sea_state
            )

            # ----------------------------------------------------
            # UPDATE M2M
            # ----------------------------------------------------

            with transaction.atomic():

                record.wind_direction_m2m.set(wind_objects)

                record.sea_state_m2m.set(sea_objects)

            # ----------------------------------------------------
            # COUNTERS
            # ----------------------------------------------------

            if wind_objects:
                wind_updated += 1

            if sea_objects:
                sea_updated += 1

            if wind_unmatched:

                wind_unmatched_count += 1

                for value in wind_unmatched:
                    wind_unmatched_values.add(value)

            if sea_unmatched:

                sea_unmatched_count += 1

                for value in sea_unmatched:
                    sea_unmatched_values.add(value)

            processed += 1

            # ----------------------------------------------------
            # DISPLAY RESULT
            # ----------------------------------------------------

            wind_values = [
                obj.description
                for obj in wind_objects
            ]

            sea_values = [
                obj.description
                for obj in sea_objects
            ]

            self.stdout.write(
                f"ID {record.id}: "
                f"WIND '{record.wind_direction}' -> {wind_values} | "
                f"SEA '{record.sea_state}' -> {sea_values}"
            )

            # ----------------------------------------------------
            # DISPLAY WARNINGS
            # ----------------------------------------------------

            if wind_unmatched:

                self.stdout.write(
                    self.style.WARNING(
                        f"    WindDirection not matched: "
                        f"{wind_unmatched}"
                    )
                )

            if sea_unmatched:

                self.stdout.write(
                    self.style.WARNING(
                        f"    SeaState not matched: "
                        f"{sea_unmatched}"
                    )
                )

        # ========================================================
        # SUMMARY
        # ========================================================

        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write("SUMMARY")
        self.stdout.write("=" * 70)

        self.stdout.write(
            f"Records processed: {processed}"
        )

        self.stdout.write(
            f"Wind Direction M2M populated: {wind_updated}"
        )

        self.stdout.write(
            f"Sea State M2M populated: {sea_updated}"
        )

        self.stdout.write(
            f"Records with unmatched wind values: "
            f"{wind_unmatched_count}"
        )

        self.stdout.write(
            f"Records with unmatched sea-state values: "
            f"{sea_unmatched_count}"
        )

        # --------------------------------------------------------
        # UNIQUE UNMATCHED WIND VALUES
        # --------------------------------------------------------

        if wind_unmatched_values:

            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    "UNMATCHED WIND DIRECTION VALUES:"
                )
            )

            for value in sorted(wind_unmatched_values):
                self.stdout.write(
                    self.style.WARNING(
                        f"  - {value}"
                    )
                )

        # --------------------------------------------------------
        # UNIQUE UNMATCHED SEA STATE VALUES
        # --------------------------------------------------------

        if sea_unmatched_values:

            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    "UNMATCHED SEA STATE VALUES:"
                )
            )

            for value in sorted(sea_unmatched_values):
                self.stdout.write(
                    self.style.WARNING(
                        f"  - {value}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "M2M population completed."
            )
        )