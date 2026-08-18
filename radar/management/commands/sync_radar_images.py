import json
import os
from pathlib import Path
from urllib.parse import urlparse

import requests

from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Import radar images and store image files locally"

    def handle(self, *args, **kwargs):

        json_file = (settings.BASE_DIR / "radar" / "data" / "radar_images.json")

        with open(json_file, encoding="utf-8") as f:
            radar_images = json.load(f)

        downloaded = 0
        failed = 0

        for item in radar_images:

            remote_url = item["image_url"]

            # Store all radar images in MEDIA_ROOT/radar
            local_directory = Path(settings.MEDIA_ROOT) / "radar"

            # Create directory if it doesn't exist
            local_directory.mkdir(parents=True, exist_ok=True)

            try:
                # Get filename from remote URL
                parsed_url = urlparse(remote_url)
                filename = os.path.basename(parsed_url.path)

                if not filename:
                    self.stdout.write(self.style.WARNING(f"Could not determine filename for: {remote_url}"))
                    failed += 1
                    continue

                # Full physical path
                local_file = local_directory / filename

                self.stdout.write(f"Downloading {remote_url}")

                response = requests.get(remote_url, timeout=30)
                response.raise_for_status()

                # Save/overwrite local file
                with open(local_file, "wb") as f:
                    f.write(response.content)

                # Public URL
                local_url = f"{settings.MEDIA_URL.rstrip('/')}/radar/{filename}"

                downloaded += 1
                self.stdout.write(self.style.SUCCESS(f"Saved: {local_file}"))

            except requests.RequestException as e:
                failed += 1
                self.stdout.write(self.style.ERROR(f"Failed downloading {remote_url}: {e}"))

            except Exception as e:
                failed += 1
                self.stdout.write(self.style.ERROR(f"Error processing radar image {item.get('id')}: {e}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Radar image sync complete. "
                f"Downloaded: {downloaded}, "
                f"Failed: {failed}"
            )
        )