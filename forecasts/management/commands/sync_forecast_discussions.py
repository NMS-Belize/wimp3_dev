# forecasts/management/commands/import_forecast_discussion.py

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.contrib.auth import get_user_model

from forecasts.models import ForecastDiscussion, ForescastGeneralCategory

User = get_user_model()

def parse_boolean(value):
    if value is None:
        return False

    return str(value).strip().lower() in ("1", "true", "yes", "on")


def clean_required_text(value):
    # Required CharFields/TextFields cannot receive None.
    return "" if value is None else str(value)


def clean_optional_text(value):
    return None if value is None else str(value)


def get_user(value):
    """ Convert legacy usernames to WIMP3 users. """

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

class Command(BaseCommand):

    help = "Sync ForecastDiscussion records from the legacy WIMP2 database."

    def add_arguments(self, parser):
        parser.add_argument("--replace",action="store_true",help="Delete existing ForecastDiscussion records before importing.")
        parser.add_argument("--batch-size",type=int,default=500,help="Number of new records inserted per batch.")

    def handle(self, *args, **options):

        # READ LEGACY DATABASE
        try:
            with connections["legacy"].cursor() as cursor:

                cursor.execute("""
                    SELECT
                        id,
                        forecast_date,forecast_time,
                        forecast_type,
                        forecast_discussion,
                        forecast_id,
                        forecast,
                        outlook,
                        advisory,
                        wind_speed,
                        wind_direction,
                        wind_condition,
                        sea_state,
                        marine_wave,
                        wave,
                        forecaster_id,
                        created_time,
                        created_by,
                        updated_time,
                        updated_by
                    FROM tbl_forecast_discussion
                    WHERE forecast_date IS NOT NULL
                    AND forecast_date <> '0000-00-00'
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

        except Exception as exc:

            self.stderr.write(
                self.style.ERROR(f"Could not read legacy database: {exc}")
            )

            return


        # BUILD FORECAST DISCUSSION OBJECTS
        records = []
        skipped_count = 0

        # Load category IDs ONCE before processing rows
        valid_category_ids = set(
            ForescastGeneralCategory.objects.values_list("id",flat=True))

        for data in rows:

            legacy_id = data["id"]
            forecast_date = data["forecast_date"]

            # Required checks
            if not legacy_id or not forecast_date:
                skipped_count += 1
                continue

            created_user = get_user(data["created_by"])
            updated_user = get_user(data["updated_by"])

            # ---------------------------------------------------------
            # FORECAST CATEGORY
            # ---------------------------------------------------------

            forecast_type = data["forecast_type"]

            if forecast_type in valid_category_ids:
                forecast_category_id = forecast_type
            else:
                forecast_category_id = None

            created_datetime = (
                data["created_time"]
                or data["updated_time"]
                or timezone.now()
            )

            updated_datetime = (
                data["updated_time"]
                or data["created_time"]
                or created_datetime
            )

            record = ForecastDiscussion(

                # Preserve WIMP2 ID
                id=legacy_id,

                forecast_date=forecast_date,
                forecast_time=data["forecast_time"],

                forecast_category_id=forecast_category_id,

                # WYSIWYG / HTML content
                forecast_discussion = clean_required_text(data["forecast_discussion"]),

                forecast_id=data["forecast_id"],
                forecast=clean_optional_text(data["forecast"]),

                outlook=clean_optional_text(data["outlook"]),
                advisory=clean_optional_text(data["advisory"]),

                wind_speed=clean_optional_text(data["wind_speed"]),
                wind_direction=clean_optional_text(data["wind_direction"]),
                wind_condition=clean_optional_text(data["wind_condition"]),

                sea_state=clean_optional_text(data["sea_state"]),

                marine_wave=clean_optional_text(data["marine_wave"]),
                wave=clean_optional_text(data["wave"]),

                forecaster_id=data["forecaster_id"],

                created_by=created_user,
                created_datetime=created_datetime,

                updated_by=updated_user,
                updated_datetime=updated_datetime,
            )
            records.append(record)

        batch_size = options["batch_size"]

        # SYNC
        with transaction.atomic():

            # REPLACE MODE

            if options["replace"]:

                deleted_count, _ = (ForecastDiscussion.objects.all().delete())

                self.stdout.write(
                    self.style.WARNING(f"Deleted {deleted_count} existing record(s).")
                )

            # FIND EXISTING IDS
            record_ids = [
                record.id
                for record in records
            ]

            existing_ids = set(
                ForecastDiscussion.objects.filter(id__in=record_ids).values_list("id",flat=True))

            # CREATE NEW RECORDS
            new_records = [
                record
                for record in records
                if record.id not in existing_ids
            ]

            if new_records:
                ForecastDiscussion.objects.bulk_create(new_records,batch_size=batch_size)

            # LOAD EXISTING RECORDS
            existing_objects = {
                obj.id: obj
                for obj in ForecastDiscussion.objects.filter(
                    id__in=existing_ids
                )
            }

            # CHECK WHICH RECORDS ACTUALLY CHANGED
            changed_records = []
            unchanged_count = 0

            for record in records:

                if record.id not in existing_ids:
                    continue

                current = existing_objects[record.id]

                # Only update if source record has changed
                if current.updated_datetime != record.updated_datetime:

                    changed_records.append(record)

                else:

                    unchanged_count += 1

            # UPDATE CHANGED RECORDS
            updated_count = 0

            if changed_records:

                field_names = [
                    field.name
                    for field in ForecastDiscussion._meta.fields
                    if field.name != "id"
                ]

                ForecastDiscussion.objects.bulk_update(
                    changed_records,
                    field_names,
                    batch_size=batch_size,
                )

                updated_count = len(changed_records)

        # RESULTS
        self.stdout.write(
            self.style.SUCCESS(
                "\nForecast Discussion sync completed successfully.\n"
                f"Legacy rows read: {len(rows)}\n"
                f"Valid rows processed: {len(records)}\n"
                f"New rows imported: {len(new_records)}\n"
                f"Existing rows updated: {updated_count}\n"
                f"Existing rows unchanged: {unchanged_count}\n"
                f"Invalid rows skipped: {skipped_count}"
            )
        )