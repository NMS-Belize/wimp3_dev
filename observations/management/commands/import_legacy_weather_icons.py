from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import connections, transaction

from observations.models import WeatherIcons


class Command(BaseCommand):

    help = "Import weather icons from legacy WIMP2 val_weather_element"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview import without saving records"
        )

    def handle(self, *args, **options):

        dry_run = options["dry_run"]

        with connections["legacy"].cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    description,
                    image_day,
                    image_night
                FROM val_weather_element
                ORDER BY id
            """)

            rows = cursor.fetchall()

        created = 0
        updated = 0
        skipped = 0

        with transaction.atomic():

            for legacy_id, description, image_day, image_night in rows:

                name = (description or "").strip()

                if not name:
                    name = f"Weather Icon {legacy_id}"

                # Model supports a maximum of 100 characters
                if len(name) > 100:
                    self.stdout.write(
                        self.style.WARNING(f"Skipping {legacy_id}: name exceeds 100 characters")
                    )
                    skipped += 1
                    continue

                # Keep filenames, not absolute filesystem paths
                day_filename = (
                    Path(str(image_day).replace("\\", "/")).name
                    if image_day else ""
                )

                night_filename = (
                    Path(str(image_night).replace("\\", "/")).name
                    if image_night else ""
                )

                defaults = {
                    "name": name,
                    "image_day": (
                        f"weather_icons/{day_filename}"
                        if day_filename else ""
                    ),
                    "image_night": (
                        f"weather_icons/{night_filename}"
                        if night_filename else ""
                    ),
                }

                if dry_run:
                    self.stdout.write(
                        f"[DRY RUN] {legacy_id}: {name} "
                        f"| Day: {day_filename} "
                        f"| Night: {night_filename}"
                    )
                    continue

                # Match by legacy ID first, then by name
                obj = WeatherIcons.objects.filter(
                    legacy_id=legacy_id
                ).first()

                if obj is None:
                    obj = WeatherIcons.objects.filter(
                        name=name
                    ).first()

                if obj:
                    for field, value in defaults.items():
                        setattr(obj, field, value)

                    obj.legacy_id = legacy_id
                    obj.save()

                    updated += 1
                else:
                    WeatherIcons.objects.create(
                        legacy_id=legacy_id,
                        **defaults
                    )

                    created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete | Created: {created} "
                f"| Updated: {updated} "
                f"| Skipped: {skipped}"
            )
        )