from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.contrib.auth import get_user_model

from forecasts.models import MunicipalityForecast, MunicipalityForecastDetails, MunicipalityZone, WeatherConditions, WindCondition

User = get_user_model()

# HELPERS
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

# COMMAND
class Command(BaseCommand):

    help = "Sync MunicipalityForecastDetails records from legacy WIMP2."

    def add_arguments(self, parser):
        parser.add_argument("--replace",action="store_true",help="Delete existing MunicipalityForecastDetails before importing.")
        parser.add_argument("--batch-size",type=int,default=500,help="Number of records processed per batch.")

    def handle(self, *args, **options):

        # READ LEGACY DATA
        with connections["legacy"].cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    zone_id,
                    temp_max,
                    temp_min,
                    wind_speed,
                    wind_cond,
                    icon_day,
                    icon_night,
                    weather_condition,
                    icon_day,
                    icon_night,
                    forecast_id,
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
            #created_user = get_user(data["created_by"])
            #updated_user = get_user(data["updated_by"])

            # MARINE FORECAST FK

            municipality_forecast_entry = None
            zone_id = None
            wind_cond = None
            weather_cond = None

            if data["forecast_id"]:
                municipality_forecast_entry = MunicipalityForecast.objects.filter(id=data["forecast_id"]).first()

            if data["zone_id"]:
                zone_id = MunicipalityZone.objects.filter(id=data["zone_id"]).first()

            if data["wind_cond"]:
                wind_cond = WindCondition.objects.filter(id=data["wind_cond"]).first()

            if data["weather_condition"]:
                weather_cond = WeatherConditions.objects.filter(id=data["weather_condition"]).first()

            # CREATE MODEL OBJECT
            record = MunicipalityForecastDetails(
                legacy_id=data["id"],

                municipality_forecast=municipality_forecast_entry,
                municipality_area=zone_id,

                temp_max=data["temp_max"] or 0,
                temp_min=data["temp_min"] or 0,

                wind_speed=clean_optional_text(data["wind_speed"]),

                # No wind_direction field in legacy table
                wind_direction=None,

                # Legacy wind_cond value
                wind_condition=wind_cond,
                weather_condition=weather_cond,

                updated_datetime=data["auto_update"],
            )
            records.append(record)

        batch_size = options["batch_size"]

        # SAVE MAIN RECORDS
        with transaction.atomic():

            # REPLACE
            if options["replace"]:

                deleted_count, _ = (MunicipalityForecastDetails.objects.all().delete())

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

            existing_ids = set(MunicipalityForecastDetails.objects.filter(legacy_id__in=legacy_ids).values_list("legacy_id",flat=True))

            # CREATE
            new_records = [
                record
                for record in records
                if record.legacy_id not in existing_ids
            ]

            if new_records:
                MunicipalityForecastDetails.objects.bulk_create(new_records,batch_size=batch_size)

            # GET EXISTING OBJECTS
            existing_objects = {
                obj.legacy_id: obj
                for obj in MunicipalityForecastDetails.objects.filter(legacy_id__in=existing_ids)
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
                    current.municipality_forecast = record.municipality_forecast
                    current.municipality_area = record.municipality_area

                    current.temp_max = record.temp_max
                    current.temp_min = record.temp_min

                    current.wind_speed = record.wind_speed
                    current.wind_direction = record.wind_direction
                    current.wind_condition = record.wind_condition
                    current.weather_condition = record.weather_condition

                    current.updated_datetime = record.updated_datetime

                    existing_records.append(current)

            updated_count = 0

            if existing_records:

                field_names = [
                    "municipality_forecast",
                    "municipality_area",
                    "temp_max",
                    "temp_min",
                    "wind_speed",
                    "wind_direction",
                    "wind_condition",
                    "weather_condition",
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