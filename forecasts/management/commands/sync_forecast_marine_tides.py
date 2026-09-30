from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.contrib.auth import get_user_model

from forecasts.models import Tides, ForecastMarine, TideDayCategory, TideLevelCategory

User = get_user_model()

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

def get_category(model, value):
    """
    Resolve a legacy category value that may be either:
    - an integer ID: 1, 2
    - a numeric string: "1", "2"
    - description text: "Today", "Tomorrow", "High", "Low"
    """

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    # Try ID first
    if value.isdigit():
        obj = model.objects.filter(id=int(value)).first()

        if obj:
            return obj

    # Otherwise try description
    return model.objects.filter(
        description__iexact=value
    ).first()

class Command(BaseCommand):

    help = "Sync MarineTides records from the legacy WIMP2 database."

    def add_arguments(self, parser):

        parser.add_argument("--replace",action="store_true",help="Delete existing MarineTides records before importing.")
        parser.add_argument("--batch-size",type=int,default=500,help="Number of records inserted/updated per batch.")

    def handle(self, *args, **options):

        # READ LEGACY TIDE DATA
        with connections["legacy"].cursor() as cursor:

            cursor.execute("""
                SELECT
                    id,
                    tide_type,
                    tide_date_type,
                    tide_date,
                    tide_time,
                    forecast_id,
                    created_by,
                    created_time,
                    updated_by,
                    updated_time,
                    general_forecast_id
                FROM tbl_forecast_marine_tide
            """)

            columns = [
                column[0]
                for column in cursor.description
            ]

            rows = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        self.stdout.write(
            f"Legacy tide rows read: {len(rows)}"
        )

        # CREATE MODEL OBJECTS
        records = []

        skipped = 0

        for data in rows:

            created_user = get_user(data["created_by"])
            updated_user = get_user(data["updated_by"])

            # Resolve Marine Forecast FK
            forecast = None

            if data["forecast_id"]:
                forecast = ForecastMarine.objects.filter(id=data["forecast_id"]).first()

            tide_level = None
            tide_day = None

            if data["tide_type"] is not None:
                tide_level = get_category(TideLevelCategory,data["tide_type"])

            if data["tide_date_type"] is not None:
                tide_day = get_category(TideDayCategory,data["tide_date_type"])

            # Create Tide Object
            record = Tides(
                id=data["id"],
                tide_level_category=tide_level,
                tide_day_category=tide_day,
                tide_date=data["tide_date"],
                tide_time=data["tide_time"],
                marine_forecast=forecast,
                general_forecast=data["general_forecast_id"],
                created_by=created_user,
                created_datetime=data["created_time"],
                updated_by=updated_user,
                updated_datetime=data["updated_time"],
            )
            records.append(record)

        batch_size = options["batch_size"]

        # SAVE DATA
        with transaction.atomic():
            
            # REPLACE MODE
            if options["replace"]:

                deleted_count, _ = Tides.objects.all().delete()

                self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing tide record(s)."))

            # FIND EXISTING RECORDS

            record_ids = [
                record.id
                for record in records
            ]

            existing_ids = set(Tides.objects.filter(id__in=record_ids).values_list("id",flat=True))

            # CREATE NEW RECORDS
            new_records = [
                record
                for record in records
                if record.id not in existing_ids
            ]

            if new_records:

                Tides.objects.bulk_create(
                    new_records,
                    batch_size=batch_size,
                )

            # -----------------------------------------------------
            # GET EXISTING OBJECTS
            # -----------------------------------------------------

            existing_objects = {
                obj.id: obj
                for obj in Tides.objects.filter(
                    id__in=existing_ids
                )
            }

            # -----------------------------------------------------
            # UPDATE ONLY CHANGED RECORDS
            # -----------------------------------------------------

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
                    for field in Tides._meta.fields
                    if field.name != "id"
                ]

                Tides.objects.bulk_update(
                    existing_records,
                    field_names,
                    batch_size=batch_size,
                )

                updated_count = len(existing_records)

        # ---------------------------------------------------------
        # COMPLETE
        # ---------------------------------------------------------

        self.stdout.write(
            self.style.SUCCESS(
                "\nMarine tide sync completed successfully.\n"
                f"Legacy rows read: {len(rows)}\n"
                f"Valid rows processed: {len(records)}\n"
                f"New rows imported: {len(new_records)}\n"
                f"Existing rows updated: {updated_count}\n"
                f"Rows skipped: {skipped}"
            )
        )