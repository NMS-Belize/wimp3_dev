from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from observations.models import WeatherIcons


class Command(BaseCommand):

    help = "Import weather icon filenames into WeatherIcons."

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Update existing icon records.",
        )

    def handle(self, *args, **options):

        icon_dir = Path(settings.BASE_DIR) / "static" / "weather_icons"

        extensions = {
            ".png", ".jpg", ".jpeg",
            ".gif", ".webp", ".svg"
        }

        if not icon_dir.is_dir():
            self.stderr.write(
                self.style.ERROR(f"Directory not found: {icon_dir}")
            )
            return

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for file_path in sorted(icon_dir.iterdir()):

            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in extensions:
                continue

            icon_name = file_path.stem
            icon_filename = file_path.name

            icon, created = WeatherIcons.objects.get_or_create(
                name=icon_name,
                defaults={"icon_file": icon_filename}
            )

            if created:
                created_count += 1

            elif options["replace"]:
                icon.icon_file.name = icon_filename
                icon.save(update_fields=["icon_file"])
                updated_count += 1

            else:
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nImport completed!\n"
                f"Created: {created_count}\n"
                f"Updated: {updated_count}\n"
                f"Skipped: {skipped_count}"
            )
        )