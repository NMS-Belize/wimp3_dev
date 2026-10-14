from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.contrib.auth import get_user_model

from forecasts.models import (
    MunicipalityForecast,
    MunicipalityForecastDetails, MunicipalityZone,
    WindDirection,
    SeaState,
)


User = get_user_model()


# ============================================================
# HELPERS
# ============================================================

def get_user(value):
    """Convert legacy usernames to WIMP3 users."""

    if value == 0 or value == "0":
        value = "forecaster"

    elif value == "admin":
        value = "smatura"

    elif value == "msmith":
        value = "maugustine"

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    return User.objects.filter(
        username=value
    ).first()


def split_values(value):
    """
    Split legacy comma-separated values.

    Example:
        "N, NE, E"

    becomes:
        ["N", "NE", "E"]
    """

    if value is None:
        return []

    return [
        item.strip()
        for item in str(value).split(",")
        if item.strip()
    ]


def clean_optional_text(value):

    if value is None:
        return None

    value = str(value).strip()

    return value if value else None


def get_category(value):
    """
    Resolve MunicipalityForecastDetailsCategory.

    Legacy value may be:
        ID
        numeric string
        description text
    """

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    # Try ID first
    if value.isdigit():

        obj = MunicipalityForecastDetailsCategory.objects.filter(
            id=int(value)
        ).first()

        if obj:
            return obj

    # Try description
    return MunicipalityForecastDetailsCategory.objects.filter(
        description__iexact=value
    ).first()


# ============================================================
# COMMAND
# ============================================================

class Command(BaseCommand):

    help = "Sync MunicipalityForecastDetails records from legacy WIMP2."

    def add_arguments(self, parser):

        parser.add_argument(
            "--replace",
            action="store_true",
            help="Delete existing MunicipalityForecastDetails before importing.",
        )

        parser.add_argument(
            "--batch-size",
            type=int,
            default=500,
            help="Number of records processed per batch.",
        )

    def handle(self, *args, **options):

        # READ LEGACY DATA
        with connections["legacy"].cursor() as cursor:

            cursor.execute("""
                SELECT
                    id,
                    zone_id,
                    temp_max,
                    temp_min,
                    forecast_id,
                    wind_speed,
                    wind_direction,
                    wind_condition,
                    icon_day,
                    icon_night,
                    weather_condition,
                    auto_update
                FROM tbl_forecast_area_zone
            """)

            columns = [
                column[0]
                for column in cursor.description
            ]

            rows = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        self.stdout.write(f"Legacy marine detail rows read: {len(rows)}")

        # BUILD RECORDS
        records = []

        skipped = 0

        for data in rows:

            # USER MAPPING
            created_user = get_user(data["created_by"])
            updated_user = get_user(data["updated_by"])

            # MARINE FORECAST FK

            municipality_forecast_entry = None

            if data["forecast_id"]:
                municipality_forecast_entry = MunicipalityForecast.objects.filter(id=data["forecast_id"]).first()

            if data["zone_id"]:
                zone_id = MunicipalityZone.objects.filter(id=data["zone_id"]).first()

            # MARINE CATEGORY
            marine_category = None

            # First try marine_type. If your category mapping actually depends on marine_date_type instead, this can be adjusted.
            if data["marine_type"] is not None:
                marine_category = get_category(data["marine_type"])

            # CREATE MODEL OBJECT
            record = MunicipalityForecastDetails(
                legacy_id=data["id"],   # Preserve WIMP2 primary key
                municipality_forecast=municipality_forecast_entry,
                municipality_area=zone_id,
                wind_speed=clean_optional_text(data["wind_speed"]),
                wind_direction=clean_optional_text(data["wind_direction"]),
                wind_condition=clean_optional_text(data["wind_condition"]),
                sea_state=clean_optional_text(data["sea_state"]),
                weather_condition=clean_optional_text(data["weather_condition"]),
                created_by=created_user,
                created_datetime=data["created_time"],
                updated_by=updated_user,
                updated_datetime=data["updated_time"],
            )
            records.append(record)

        batch_size = options["batch_size"]

        # SAVE MAIN RECORDS
        with transaction.atomic():

            # REPLACE
            if options["replace"]:

                deleted_count, _ = (
                    MunicipalityForecastDetails.objects.all().delete()
                )

                self.stdout.write(
                    self.style.WARNING(
                        f"Deleted {deleted_count} existing "
                        f"marine detail record(s)."
                    )
                )

            # EXISTING LEGACY IDS
            legacy_ids = [
                record.legacy_id
                for record in records
            ]

            existing_ids = set(
                MunicipalityForecastDetails.objects.filter(legacy_id__in=legacy_ids).values_list("legacy_id",flat=True)
            )

            # CREATE
            new_records = [
                record
                for record in records
                if record.legacy_id not in existing_ids
            ]

            if new_records:

                MunicipalityForecastDetails.objects.bulk_create(
                    new_records,
                    batch_size=batch_size,
                )

            # GET EXISTING OBJECTS
            existing_objects = {
                obj.legacy_id: obj
                for obj in MunicipalityForecastDetails.objects.filter(
                    legacy_id__in=existing_ids
                )
            }

            # UPDATE CHANGED RECORDS
            existing_records = []

            for record in records:

                if record.legacy_id not in existing_ids:
                    continue

                # This is the REAL database object and has a primary key
                current = existing_objects[record.legacy_id]

                if current.updated_datetime != record.updated_datetime:

                    # Copy imported values onto the existing DB object
                    current.marine_forecast = record.marine_forecast
                    current.marine_category = record.marine_category
                    current.wind_speed = record.wind_speed
                    current.wind_direction = record.wind_direction
                    current.wind_condition = record.wind_condition
                    current.sea_state = record.sea_state
                    current.waves = record.waves
                    current.additional_info = record.additional_info

                    current.created_by = record.created_by
                    current.created_datetime = record.created_datetime

                    current.updated_by = record.updated_by
                    current.updated_datetime = record.updated_datetime

                    existing_records.append(current)

            updated_count = 0

            if existing_records:

                field_names = [
                    "marine_forecast",
                    "marine_category",
                    "wind_speed",
                    "wind_direction",
                    "wind_condition",
                    "sea_state",
                    "waves",
                    "additional_info",
                    "created_by",
                    "created_datetime",
                    "updated_by",
                    "updated_datetime",
                ]
                MunicipalityForecastDetails.objects.bulk_update(existing_records,field_names,batch_size=batch_size)
                updated_count = len(existing_records)

            # M2M SYNC
            # M2M fields cannot be populated with bulk_create()
            # or bulk_update(), so handle them afterward.

            changed_legacy_ids = {
                record.legacy_id
                for record in new_records
            }

            changed_legacy_ids.update(
                record.legacy_id
                for record in existing_records
            )

            detail_objects = {
                obj.legacy_id: obj
                for obj in MunicipalityForecastDetails.objects.filter(legacy_id__in=changed_legacy_ids)
            }

            for data in rows:

                legacy_id = data["id"]

                if legacy_id not in changed_legacy_ids:
                    continue

                detail = detail_objects.get(legacy_id)

                if not detail:
                    continue

                # WIND DIRECTION M2M
                wind_values = split_values(data["wind_direction"])

                if wind_values:
                    wind_items = WindDirection.objects.filter(description__in=wind_values)
                    detail.wind_direction_m2m.set(wind_items)
                else:
                    detail.wind_direction_m2m.clear()

                # SEA STATE M2M
                sea_values = split_values(data["sea_state"])

                if sea_values:
                    sea_items = SeaState.objects.filter(description__in=sea_values)
                    detail.sea_state_m2m.set(sea_items)
                else:
                    detail.sea_state_m2m.clear()

        # COMPLETE
        self.stdout.write(
            self.style.SUCCESS(
                "\nMarine forecast details sync completed successfully.\n"
                f"Legacy rows read: {len(rows)}\n"
                f"Valid rows processed: {len(records)}\n"
                f"New rows imported: {len(new_records)}\n"
                f"Existing rows updated: {updated_count}\n"
                f"Rows skipped: {skipped}"
            )
        )