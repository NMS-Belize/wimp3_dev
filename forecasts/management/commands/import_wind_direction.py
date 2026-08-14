from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.contrib.auth import get_user_model

from forecasts.models import WindDirection

User = get_user_model()

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

    help = "Sync WindDirection records from the legacy WIMP2 database."

    def add_arguments(self, parser):
        parser.add_argument("--replace", action="store_true", help="Delete existing WindDirection records before importing.")
        parser.add_argument("--batch-size", type=int, default=500, help="Number of new records inserted per batch.")

    def handle(self, *args, **options):

        with connections["legacy"].cursor() as cursor:
            cursor.execute("""
                SELECT * FROM val_wind_direction WHERE description IS NOT NULL
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

            record = WindDirection(
                id              = data["id"],

                description     =clean_required_text(data["description"]),
                long_description=clean_required_text(data["long_description"]),
                value           =data["value"],

                created_by      = created_user,
                created_datetime = data["created_time"],
                updated_by      = updated_user,
                updated_datetime = data["updated_time"],
            )

            records.append(record)

        batch_size = options["batch_size"]

        with transaction.atomic():

            if options["replace"]:
                deleted_count, _ = WindDirection.objects.all().delete()

                self.stdout.write(
                    self.style.WARNING(f"Deleted {deleted_count} existing record(s).")
                )

            # Get IDs that already exist in WIMP3
            existing_ids = set(
                WindDirection.objects.filter(id__in=[record.id for record in records]).values_list("id", flat=True)
            )

            # CREATE NEW RECORDS
            new_records = [
                record
                for record in records
                if record.id not in existing_ids
            ]

            if new_records:
                WindDirection.objects.bulk_create(new_records, batch_size = batch_size)

            # UPDATE EXISTING RECORDS ONLY IF SOURCE CHANGED
            existing_objects = {
                obj.id: obj
                for obj in WindDirection.objects.filter(id__in=existing_ids)
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
                    for field in WindDirection._meta.fields
                    if field.name != "id"
                ]

                WindDirection.objects.bulk_update(existing_records, field_names, batch_size=batch_size,)

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