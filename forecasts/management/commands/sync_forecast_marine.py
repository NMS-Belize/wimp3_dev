# forecasts/management/commands/import_forecast_general.py
from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.contrib.auth import get_user_model

from forecasts.models import ForecastMarine, SeaState, WindCondition, WindDirection

User = get_user_model()

def split_values(value):
    if value is None:
        return []

    return [
        item.strip()
        for item in str(value).split(",")
        if item.strip()
    ]

def parse_boolean(value):
    if value is None:
        return False

    return str(value).strip().lower() in ("1", "true", "yes", "on")

def clean_required_text(value):

    # Required CharFields cannot receive None.
    return "" if value is None else str(value)

def clean_optional_text(value):
    return None if value is None else str(value)

def get_user(value):
    if value == 0 or value == '0':
        value = 'forecaster'
    elif value == 'admin':
        value = 'smatura'
    elif value == 'msmith':
            value = 'maugustine'

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    return User.objects.filter(username=value).first()

class Command(BaseCommand):

    help = "Sync ForecastMarine records from the legacy WIMP2 database."

    def add_arguments(self, parser):
        parser.add_argument("--replace", action="store_true", help="Delete existing ForecastMarine records before importing.")
        parser.add_argument("--batch-size", type=int, default=500, help="Number of new records inserted per batch.")

    def handle(self, *args, **options):

        with connections["legacy"].cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    forecast_date, forecast_time, marine_forecast_type,
                    synopsis, advisory, 
                    sea_surface_temperature, min_temperature, max_temperature,
                    publish_to_web,
                    created_by, created_time, updated_by, updated_time
                FROM tbl_forecast_marine
                WHERE forecast_date IS NOT NULL
                AND forecast_date <> '0000-00-00'
            """)

            columns = [
                column[0]
                for column in cursor.description
            ]

            rows = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        records = []

        for data in rows:

            created_user = get_user(data["created_by"])
            updated_user = get_user(data["updated_by"])

            record = ForecastMarine(
                id              = data["id"],
                forecast_date   = data["forecast_date"],
                forecast_time   = data["forecast_time"],
                forecast_category_id = data["marine_forecast_type"],

                synopsis   = clean_required_text(data["synopsis"]),
                
                advisory    = clean_required_text(data["advisory"]),
                
                sea_surface_temperature    = data["sea_surface_temperature"],
                min_temperature    = data["min_temperature"],
                max_temperature    = data["max_temperature"],
                
                is_published    = parse_boolean(data["publish_to_web"]),

                created_by      = created_user,
                created_datetime = data["created_time"],
                updated_by      = updated_user,
                updated_datetime = data["updated_time"],
            )

            records.append(record)

        batch_size = options["batch_size"]

        with transaction.atomic():

            if options["replace"]:
                deleted_count, _ = ForecastMarine.objects.all().delete()

                self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing record(s)."))

            # Get IDs that already exist in WIMP3
            existing_ids = set(ForecastMarine.objects.filter(id__in=[record.id for record in records]).values_list("id", flat=True))

            # CREATE NEW RECORDS
            new_records = [
                record
                for record in records
                if record.id not in existing_ids
            ]

            if new_records:
                ForecastMarine.objects.bulk_create(new_records, batch_size=batch_size)

            # UPDATE EXISTING RECORDS ONLY IF SOURCE CHANGED
            existing_objects = {
                obj.id: obj
                for obj in ForecastMarine.objects.filter(
                    id__in=existing_ids
                )
            }

            existing_records = []

            for record in records:
                if record.id not in existing_ids:
                    continue

                current = existing_objects[record.id]

                if current.updated_datetime != record.updated_datetime:
                    existing_records.append(record)

            updated_count = 0

            if existing_records:

                field_names = [
                    field.name
                    for field in ForecastMarine._meta.fields
                    if field.name != "id"
                ]

                ForecastMarine.objects.bulk_update(existing_records, field_names, batch_size=batch_size,)

                updated_count = len(existing_records)


            m2m_ids = {
                record.id
                for record in new_records
            }

            m2m_ids.update(
                record.id
                for record in existing_records
            )

            # SYNC MANY-TO-MANY FIELDS
            forecast_objects = {
                obj.id: obj
                for obj in ForecastMarine.objects.filter(id__in=m2m_ids)
            }

            for data in rows:

                if data["id"] not in m2m_ids:
                    continue

                forecast = forecast_objects.get(data["id"])

                if not forecast:
                    continue

                # WIND DIRECTION
                '''values = split_values(data["wind_direction"])

                if values:
                    items = WindDirection.objects.filter(description__in=values)
                    forecast.wind_direction_m2m.set(items)
                else:
                    forecast.wind_direction_m2m.clear()

                # WIND CONDITION
                values = split_values(data["wind_condition"])

                if values:
                    items = WindCondition.objects.filter(description__in=values)
                    forecast.wind_condition_m2m.set(items)
                else:
                    forecast.wind_condition_m2m.clear()

                # WIND SHIFT DIRECTION
                values = split_values(data["wind_shift_direction"])

                if values:
                    items = WindDirection.objects.filter(description__in=values)
                    forecast.wind_shift_direction_m2m.set(items)
                else:
                    forecast.wind_shift_direction_m2m.clear()

                # WIND SHIFT CONDITION
                values = split_values(data["wind_shift_condition"])

                if values:
                    items = WindCondition.objects.filter(description__in=values)
                    forecast.wind_shift_condition_m2m.set(items)
                else:
                    forecast.wind_shift_condition_m2m.clear()

                # SEA STATE
                values = split_values(data["sea_state"])

                if values:
                    items = SeaState.objects.filter(description__in=values)
                    forecast.sea_state_m2m.set(items)
                else:
                    forecast.sea_state_m2m.clear()

                # SEA STATE SHIFT
                values = split_values(data["sea_state_shift"])

                if values:
                    items = SeaState.objects.filter(description__in=values)
                    forecast.sea_state_shift_m2m.set(items)
                else:
                    forecast.sea_state_shift_m2m.clear()'''

        self.stdout.write(
            self.style.SUCCESS(
                "\nSync completed successfully.\n"
                f"Legacy rows read: {len(rows)}\n"
                f"Valid rows processed: {len(records)}\n"
                f"New rows imported: {len(new_records)}\n"
                f"Existing rows updated: {updated_count}"
            )
        )