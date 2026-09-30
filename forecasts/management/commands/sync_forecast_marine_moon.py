from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.contrib.auth import get_user_model

from forecasts.models import (MoonRiseSet,ForecastMarine,MoonDayCategory,MoonMovementCategory)

User = get_user_model()

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


def get_category(model, value):
    """
    Resolve legacy category value by ID or description.
    """

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    # Try ID
    if value.isdigit():
        obj = model.objects.filter(id=int(value)).first()

        if obj:
            return obj

    # Try description
    return model.objects.filter(
        description__iexact=value
    ).first()


class Command(BaseCommand):

    help = "Sync MoonRiseSet records from the legacy WIMP2 database."

    def add_arguments(self, parser):

        parser.add_argument(
            "--replace",
            action="store_true",
            help="Delete existing MoonRiseSet records before importing.",
        )

        parser.add_argument(
            "--batch-size",
            type=int,
            default=500,
            help="Number of records inserted/updated per batch.",
        )

    def handle(self, *args, **options):

        # ---------------------------------------------------------
        # READ LEGACY MOON DATA
        # ---------------------------------------------------------

        with connections["legacy"].cursor() as cursor:

            cursor.execute("""
                SELECT
                    id,
                    moon_type,
                    moon_date_type,
                    moon_date,
                    moon_time,
                    forecast_id,
                    created_by,
                    created_time,
                    updated_by,
                    updated_time
                FROM tbl_forecast_marine_moon
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
            f"Legacy moon rows read: {len(rows)}"
        )

        # ---------------------------------------------------------
        # CREATE MODEL OBJECTS
        # ---------------------------------------------------------

        records = []
        skipped = 0

        for data in rows:

            created_user = get_user(data["created_by"])
            updated_user = get_user(data["updated_by"])

            # Marine Forecast
            forecast = None

            if data["forecast_id"]:
                forecast = ForecastMarine.objects.filter(
                    id=data["forecast_id"]
                ).first()

            # Categories can be NULL
            moon_movement = None
            moon_day = None

            if data["moon_type"] is not None:
                moon_movement = get_category(
                    MoonMovementCategory,
                    data["moon_type"]
                )

            if data["moon_date_type"] is not None:
                moon_day = get_category(
                    MoonDayCategory,
                    data["moon_date_type"]
                )

            # -----------------------------------------------------
            # CREATE MOON OBJECT
            # -----------------------------------------------------

            record = MoonRiseSet(
                id=data["id"],

                moon_move_category=moon_movement,
                moon_day_category=moon_day,

                moon_date=data["moon_date"],
                moon_time=data["moon_time"],

                marine_forecast=forecast,

                created_by=created_user,
                created_datetime=data["created_time"],

                updated_by=updated_user,
                updated_datetime=data["updated_time"],
            )

            records.append(record)

        batch_size = options["batch_size"]

        # ---------------------------------------------------------
        # SAVE
        # ---------------------------------------------------------

        with transaction.atomic():

            if options["replace"]:

                deleted_count, _ = MoonRiseSet.objects.all().delete()

                self.stdout.write(
                    self.style.WARNING(
                        f"Deleted {deleted_count} existing moon record(s)."
                    )
                )

            record_ids = [
                record.id
                for record in records
            ]

            existing_ids = set(
                MoonRiseSet.objects.filter(
                    id__in=record_ids
                ).values_list(
                    "id",
                    flat=True
                )
            )

            # CREATE
            new_records = [
                record
                for record in records
                if record.id not in existing_ids
            ]

            if new_records:

                MoonRiseSet.objects.bulk_create(
                    new_records,
                    batch_size=batch_size,
                )

            # Existing objects
            existing_objects = {
                obj.id: obj
                for obj in MoonRiseSet.objects.filter(
                    id__in=existing_ids
                )
            }

            # UPDATE
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
                    for field in MoonRiseSet._meta.fields
                    if field.name != "id"
                ]

                MoonRiseSet.objects.bulk_update(
                    existing_records,
                    field_names,
                    batch_size=batch_size,
                )

                updated_count = len(existing_records)

        self.stdout.write(
            self.style.SUCCESS(
                "\nMarine moon sync completed successfully.\n"
                f"Legacy rows read: {len(rows)}\n"
                f"Valid rows processed: {len(records)}\n"
                f"New rows imported: {len(new_records)}\n"
                f"Existing rows updated: {updated_count}\n"
                f"Rows skipped: {skipped}"
            )
        )