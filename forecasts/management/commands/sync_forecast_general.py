# forecasts/management/commands/import_forecast_general.py
from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.contrib.auth import get_user_model

from forecasts.models import ForecastGeneral

User = get_user_model()

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

    help = "Sync ForecastGeneral records from the legacy WIMP2 database."

    def add_arguments(self, parser):
        parser.add_argument("--replace", action="store_true", help="Delete existing ForecastGeneral records before importing.")
        parser.add_argument("--batch-size", type=int, default=500, help="Number of new records inserted per batch.")

    def handle(self, *args, **options):

        with connections["legacy"].cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    forecast_date, forecast_time, forecast_type,
                    general_situation, thr_forecast, light_variable,
                    wind_speed, wind_direction, wind_condition, wind_shift_speed, wind_shift_direction, wind_shift_condition,
                    sea_state, sea_state_shift,
                    wave,  wave_shift, 
                    advisory, outlook,
                    coast_high_f, coast_high_c, coast_low_f, coast_low_c, 
                    inland_high_f, inland_high_c, inland_low_f, inland_low_c,
                    hills_high_f, hills_high_c, hills_low_f, hills_low_c,
                    publish_to_web,
                    created_by, created_time, updated_by, updated_time
                FROM tbl_forecast_general
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

            record = ForecastGeneral(
                id              = data["id"],
                forecast_date   = data["forecast_date"],
                forecast_time   = data["forecast_time"],
                forecast_category_id = data["forecast_type"],

                general_situation   = clean_required_text(data["general_situation"]),
                twenty_four_hour_forecast = clean_required_text(data["thr_forecast"]),

                light_variable  = data["light_variable"],

                wind_speed      = clean_required_text(data["wind_speed"]),
                wind_direction  = clean_optional_text(data["wind_direction"]),
                wind_condition  = clean_optional_text(data["wind_condition"]),

                wind_shift_speed        = clean_optional_text(data["wind_shift_speed"]),
                wind_shift_direction    = clean_optional_text(data["wind_shift_direction"]),
                wind_shift_condition    = clean_optional_text(data["wind_shift_condition"]),

                sea_state   = clean_required_text(data["sea_state"]),
                wave        = clean_optional_text(data["wave"]),

                sea_state_shift = clean_optional_text(data["sea_state_shift"]),
                wave_shift  = clean_optional_text(data["wave_shift"]),

                advisory    = clean_required_text(data["advisory"]),
                outlook     = clean_required_text(data["outlook"]),

                coast_high_f    = data["coast_high_f"],
                coast_high_c    = data["coast_high_c"],
                coast_low_f     = data["coast_low_f"],
                coast_low_c     = data["coast_low_c"],

                inland_high_f   = data["inland_high_f"],
                inland_high_c   = data["inland_high_c"],
                inland_low_f    = data["inland_low_f"],
                inland_low_c    = data["inland_low_c"],

                hills_high_f    = data["hills_high_f"],
                hills_high_c    = data["hills_high_c"],
                hills_low_f     = data["hills_low_f"],
                hills_low_c     = data["hills_low_c"],

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
                deleted_count, _ = ForecastGeneral.objects.all().delete()

                self.stdout.write(
                    self.style.WARNING(f"Deleted {deleted_count} existing record(s).")
                )

            # Get IDs that already exist in WIMP3
            existing_ids = set(
                ForecastGeneral.objects.filter(id__in=[record.id for record in records]).values_list("id", flat=True)
            )

            # CREATE NEW RECORDS
            new_records = [
                record
                for record in records
                if record.id not in existing_ids
            ]

            if new_records:
                ForecastGeneral.objects.bulk_create(new_records, batch_size = batch_size)

            # UPDATE EXISTING RECORDS ONLY IF SOURCE CHANGED
            existing_objects = {
                obj.id: obj
                for obj in ForecastGeneral.objects.filter(id__in=existing_ids)
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
                    for field in ForecastGeneral._meta.fields
                    if field.name != "id"
                ]

                ForecastGeneral.objects.bulk_update(existing_records, field_names, batch_size=batch_size,)

                updated_count = len(existing_records)

        self.stdout.write(
            self.style.SUCCESS(
                "\nSync completed successfully.\n"
                f"Legacy rows read: {len(rows)}\n"
                f"Valid rows processed: {len(records)}\n"
                f"New rows imported: {len(new_records)}\n"
                f"Existing rows updated: {updated_count}"
            )
        )