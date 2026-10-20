from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.contrib.auth import get_user_model

from forecasts.models import (
    MunicipalityForecast,
    MunicipalityForecastDetails,
    MunicipalityZone,
    WeatherConditions,
    WindCondition,
    WindSpeed,
)

from observations.models import WeatherIcons

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

    return User.objects.filter(username=value).first()

def clean_optional_text(value):

    if value is None:
        return None

    value = str(value).strip()

    return value if value else None


def get_fk(model, value, use_legacy_id=False):
    """
    Retrieve a ForeignKey object.

    Uses legacy_id when requested and available.
    Otherwise uses the model primary key.
    """

    if value is None or str(value).strip() == "":
        return None
    try:
        field_names = {
            field.name
            for field in model._meta.get_fields()
        }
        if use_legacy_id and "legacy_id" in field_names:
            return model.objects.filter(legacy_id=value).first()

        return model.objects.filter(pk=value).first()

    except (ValueError, TypeError):
        return None


# ============================================================
# COMMAND
# ============================================================

class Command(BaseCommand):

    help = "Sync MunicipalityForecastDetails records from legacy WIMP2."

    def add_arguments(self, parser):

        parser.add_argument(
            "--replace",
            action="store_true",
            help="Delete existing MunicipalityForecastDetails before importing."
        )

        parser.add_argument(
            "--batch-size",
            type=int,
            default=500,
            help="Number of records processed per batch."
        )

    def handle(self, *args, **options):

        batch_size = options["batch_size"]

        # ====================================================
        # READ LEGACY DATA
        # ====================================================

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
                    forecast_id,
                    auto_update
                FROM tbl_forecast_area_zone
                ORDER BY id
            """)

            columns = [
                column[0]
                for column in cursor.description
            ]

            rows = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        self.stdout.write(f"Legacy municipality forecast detail rows read: {len(rows)}")

        # BUILD RECORDS
        records = []
        skipped = 0

        for data in rows:

            legacy_id = data["id"]

            if legacy_id is None:
                skipped += 1
                continue

            # FOREIGN KEY MAPPINGS

            # MUNICIPALITY FORECAST
            municipality_forecast_entry = MunicipalityForecast.objects.filter(id=data["forecast_id"]).first() if data["forecast_id"] else None

            # MUNICIPALITY ZONE
            municipality_zone = MunicipalityZone.objects.filter(id=data["zone_id"]).first() if data["zone_id"] else None

            # WIND SPEED
            wind_speed = WindSpeed.objects.filter(id=data["wind_speed"]).first() if data["wind_speed"] else None

            # WIND CONDITION
            wind_condition = WindCondition.objects.filter(id=data["wind_cond"]).first() if data["wind_cond"] else None

            # WEATHER CONDITION
            weather_condition = WeatherConditions.objects.filter(id=data["weather_condition"]).first() if data["weather_condition"] else None

            # WEATHER ICON DAY
            icon_day_id = WeatherIcons.objects.filter(legacy_id=data["icon_day"]).values_list("id", flat=True).first() if data["icon_day"] else None

            # WEATHER ICON NIGHT
            icon_night_id = WeatherIcons.objects.filter(legacy_id=data["icon_night"]).values_list("id", flat=True).first() if data["icon_night"] else None

            # CREATE MODEL OBJECT
            record = MunicipalityForecastDetails(

                legacy_id=data["id"],

                municipality_forecast=municipality_forecast_entry,
                municipality_area=municipality_zone,

                temp_max=data["temp_max"] or 0,
                temp_min=data["temp_min"] or 0,

                wind_speed=wind_speed,
                wind_condition=wind_condition,
                weather_condition=weather_condition,

                icon_day_id=icon_day_id,
                icon_night_id=icon_night_id,

                updated_datetime=data["auto_update"],
            )
            records.append(record)

        # SAVE RECORDS
        with transaction.atomic():

            # REPLACE EXISTING RECORDS
            if options["replace"]:

                deleted_count, _ = (MunicipalityForecastDetails.objects.all().delete())

                self.stdout.write(
                    self.style.WARNING(
                        f"Deleted {deleted_count} existing "
                        f"municipality forecast detail record(s)."
                    )
                )

            # EXISTING LEGACY IDS
            legacy_ids = [
                record.legacy_id
                for record in records
            ]

            existing_ids = set(MunicipalityForecastDetails.objects.filter(legacy_id__in=legacy_ids).values_list("legacy_id",flat=True))

            # CREATE NEW RECORDS
            new_records = [
                record
                for record in records
                if record.legacy_id not in existing_ids
            ]

            if new_records:
                MunicipalityForecastDetails.objects.bulk_create(new_records,batch_size=batch_size)

            # LOAD EXISTING OBJECTS
            existing_objects = {
                obj.legacy_id: obj
                for obj in MunicipalityForecastDetails.objects.filter(legacy_id__in=existing_ids)
            }

            # UPDATE EXISTING RECORDS
            existing_records = []

            for record in records:

                if record.legacy_id not in existing_ids:
                    continue

                current = existing_objects.get(record.legacy_id)

                if not current:
                    continue

                # Compare imported values, not just timestamps.
                # This also detects changes to related objects.

                fields_changed = (
                    current.municipality_forecast_id != record.municipality_forecast_id
                    or current.municipality_area_id != record.municipality_area_id
                    or current.temp_max != record.temp_max
                    or current.temp_min != record.temp_min
                    or current.wind_speed_id != record.wind_speed_id
                    or current.wind_condition_id != record.wind_condition_id
                    or current.weather_condition_id != record.weather_condition_id
                    or current.icon_day_id != record.icon_day_id
                    or current.icon_night_id != record.icon_night_id
                    or current.updated_datetime != record.updated_datetime
                )

                if not fields_changed:
                    continue

                # Copy values

                current.municipality_forecast = record.municipality_forecast
                current.municipality_area = record.municipality_area

                current.temp_max = record.temp_max
                current.temp_min = record.temp_min

                current.wind_speed = record.wind_speed

                current.wind_condition = record.wind_condition
                current.weather_condition = record.weather_condition

                current.weather_condition_id = record.weather_condition_id
                current.weather_condition_id = record.weather_condition_id

                current.updated_datetime = record.updated_datetime

                existing_records.append(current)

            # -----------------------------------------------
            # BULK UPDATE
            # -----------------------------------------------

            updated_count = 0

            if existing_records:

                field_names = [
                    "municipality_forecast",
                    "municipality_area",
                    "temp_max",
                    "temp_min",
                    "wind_speed",
                    "wind_condition",
                    "weather_condition",
                    "icon_day",
                    "icon_night",
                    "updated_datetime",
                ]
                MunicipalityForecastDetails.objects.bulk_update(
                    existing_records,
                    field_names,
                    batch_size=batch_size
                )
                updated_count = len(existing_records)

        # COMPLETE
        self.stdout.write(
            self.style.SUCCESS(
                "\nMunicipality forecast details sync completed successfully.\n"
                f"Legacy rows read: {len(rows)}\n"
                f"Valid rows processed: {len(records)}\n"
                f"New rows imported: {len(new_records)}\n"
                f"Existing rows updated: {updated_count}\n"
                f"Rows skipped: {skipped}"
            )
        )