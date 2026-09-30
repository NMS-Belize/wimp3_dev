import json

from django.core.management.base import BaseCommand

from forecasts.models import (
    ForecastGeneral,
    ForecastMarineDetails,
    WindDirection,
    WindCondition,
    SeaState,
)


class Command(BaseCommand):

    help = (
        "Clear and repopulate ForecastGeneral and ForecastMarineDetails "
        "M2M fields from legacy fields"
    )

    def handle(self, *args, **options):

        # ============================================================
        # FIELD MAPPINGS
        # ============================================================

        general_field_map = [
            ("wind_direction", "wind_direction_m2m", WindDirection),
            ("wind_condition", "wind_condition_m2m", WindCondition),
            ("wind_shift_direction", "wind_shift_direction_m2m", WindDirection),
            ("wind_shift_condition", "wind_shift_condition_m2m", WindCondition),
            ("sea_state", "sea_state_m2m", SeaState),
            ("sea_state_shift", "sea_state_shift_m2m", SeaState),
        ]

        marine_details_field_map = [
            ("wind_direction", "wind_direction_m2m", WindDirection),
            ("sea_state", "sea_state_m2m", SeaState),
        ]

        # ============================================================
        # PARSE LEGACY IDS
        # ============================================================

        def parse_ids(value):
            """
            Convert legacy field values into a list of integer IDs.

            Supported examples:

                [1, 2, 3]
                ["1", "2", "3"]
                1
                "1"
                "1,2,3"
                "1, 2, 3"
                "[1,2,3]"
            """

            if value is None:
                return []

            value = str(value).strip()

            if not value:
                return []

            # --------------------------------------------------------
            # Try JSON
            # --------------------------------------------------------

            try:
                result = json.loads(value)

                if isinstance(result, list):

                    ids = []

                    for item in result:
                        try:
                            ids.append(int(item))
                        except (TypeError, ValueError):
                            pass

                    return ids

                if isinstance(result, int):
                    return [result]

                if isinstance(result, str):
                    try:
                        return [int(result)]
                    except ValueError:
                        pass

            except (json.JSONDecodeError, TypeError, ValueError):
                pass

            # --------------------------------------------------------
            # Try comma-separated values
            # --------------------------------------------------------

            try:
                return [
                    int(item.strip())
                    for item in value.split(",")
                    if item.strip()
                ]

            except (TypeError, ValueError):
                return []

        # ============================================================
        # PROCESS MODEL
        # ============================================================

        def process_model(model, field_map, model_name):
            """
            Clear existing M2M relationships and repopulate them
            from their corresponding legacy fields.
            """

            self.stdout.write("")
            self.stdout.write("=" * 70)

            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    f"PROCESSING {model_name}"
                )
            )

            self.stdout.write("=" * 70)

            queryset = model.objects.all()

            total_records = queryset.count()

            self.stdout.write(
                f"Found {total_records} {model_name} records."
            )

            # ========================================================
            # STEP 1
            # CLEAR EXISTING M2M RELATIONSHIPS
            # ========================================================

            self.stdout.write("")
            self.stdout.write(
                f"Clearing existing {model_name} M2M relationships..."
            )

            cleared_count = 0

            for record in queryset:

                for legacy_field, m2m_field, related_model in field_map:

                    manager = getattr(record, m2m_field, None)

                    if manager is None:

                        self.stdout.write(
                            self.style.ERROR(
                                f"{model_name} ID={record.id} | "
                                f"M2M field '{m2m_field}' not found."
                            )
                        )

                        continue

                    manager.clear()

                    cleared_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"{model_name}: M2M relationships cleared."
                )
            )

            # ========================================================
            # STEP 2
            # REPOPULATE M2M RELATIONSHIPS
            # ========================================================

            self.stdout.write("")
            self.stdout.write(
                f"Repopulating {model_name} M2M relationships..."
            )

            updated_count = 0
            skipped_count = 0
            missing_ids_count = 0

            for record in queryset:

                for legacy_field, m2m_field, related_model in field_map:

                    # ------------------------------------------------
                    # Get legacy value
                    # ------------------------------------------------

                    raw_value = getattr(
                        record,
                        legacy_field,
                        None
                    )

                    if raw_value is None:
                        continue

                    raw_value_string = str(raw_value).strip()

                    if not raw_value_string:
                        continue

                    # ------------------------------------------------
                    # Parse IDs
                    # ------------------------------------------------

                    ids = parse_ids(raw_value)

                    if not ids:

                        skipped_count += 1

                        self.stdout.write(
                            self.style.WARNING(
                                f"SKIPPED | "
                                f"{model_name} ID={record.id} | "
                                f"{legacy_field}={raw_value}"
                            )
                        )

                        continue

                    # ------------------------------------------------
                    # Remove duplicate IDs
                    # ------------------------------------------------

                    ids = list(dict.fromkeys(ids))

                    # ------------------------------------------------
                    # Find related objects
                    # ------------------------------------------------

                    objects = related_model.objects.filter(
                        id__in=ids
                    )

                    found_ids = list(
                        objects.values_list(
                            "id",
                            flat=True
                        )
                    )

                    # ------------------------------------------------
                    # Check for IDs that do not exist
                    # ------------------------------------------------

                    missing_ids = [
                        item_id
                        for item_id in ids
                        if item_id not in found_ids
                    ]

                    if missing_ids:

                        missing_ids_count += len(missing_ids)

                        self.stdout.write(
                            self.style.WARNING(
                                f"MISSING IDs | "
                                f"{model_name} ID={record.id} | "
                                f"{legacy_field} | "
                                f"{related_model.__name__} IDs "
                                f"{missing_ids}"
                            )
                        )

                    # ------------------------------------------------
                    # Set M2M relationship
                    # ------------------------------------------------

                    manager = getattr(
                        record,
                        m2m_field
                    )

                    manager.set(objects)

                    updated_count += 1

                    # ------------------------------------------------
                    # Console output
                    # ------------------------------------------------

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"UPDATED | "
                            f"{model_name} ID={record.id} | "
                            f"{legacy_field}={raw_value} | "
                            f"{m2m_field} -> {found_ids}"
                        )
                    )

            # ========================================================
            # MODEL SUMMARY
            # ========================================================

            self.stdout.write("")
            self.stdout.write("-" * 70)

            self.stdout.write(
                self.style.SUCCESS(
                    f"{model_name} COMPLETE"
                )
            )

            self.stdout.write(
                f"Records:       {total_records}"
            )

            self.stdout.write(
                f"M2M Updated:   {updated_count}"
            )

            self.stdout.write(
                f"Skipped:       {skipped_count}"
            )

            self.stdout.write(
                f"Missing IDs:   {missing_ids_count}"
            )

            self.stdout.write("-" * 70)

        # ============================================================
        # PROCESS FORECAST GENERAL
        # ============================================================

        process_model(
            model=ForecastGeneral,
            field_map=general_field_map,
            model_name="ForecastGeneral",
        )

        # ============================================================
        # PROCESS MARINE FORECAST DETAILS
        # ============================================================

        process_model(
            model=ForecastMarineDetails,
            field_map=marine_details_field_map,
            model_name="ForecastMarineDetails",
        )

        # ============================================================
        # FINISHED
        # ============================================================

        self.stdout.write("")
        self.stdout.write("=" * 70)

        self.stdout.write(
            self.style.SUCCESS(
                "ALL M2M RELATIONSHIPS SUCCESSFULLY REPOPULATED"
            )
        )

        self.stdout.write("=" * 70)