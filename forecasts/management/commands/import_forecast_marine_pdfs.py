import os
import re
import requests

from urllib.parse import urljoin

from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = "Import all Marine Forecast PDFs from WIMP2 into WIMP3."

    # Change this to the actual WIMP2 directory URL
    WIMP2_PDF_URL = "https://wimp.nms.gov.bz/forecast/marine/files/"

    def handle(self, *args, **options):

        destination_dir = os.path.join(settings.MEDIA_ROOT,"forecast","marine","doc")
        os.makedirs(destination_dir, exist_ok=True)
        self.stdout.write(f"Reading PDF list from {self.WIMP2_PDF_URL}")

        try:
            response = requests.get(self.WIMP2_PDF_URL, timeout=30)
            response.raise_for_status()

        except requests.RequestException as exc:
            self.stderr.write(self.style.ERROR(f"Unable to access WIMP2: {exc}"))
            return

        # Find PDF filenames in directory listing
        filenames = re.findall(r'href=["\']([^"\']+\.pdf)["\']', response.text, flags=re.IGNORECASE)
        filenames = sorted(set(filenames))

        if not filenames:
            self.stdout.write(self.style.WARNING("No PDF files found."))
            return

        self.stdout.write(f"Found {len(filenames)} PDF file(s).")

        downloaded = 0
        skipped = 0
        failed = 0

        for filename in filenames:

            # Prevent directory traversal
            filename = os.path.basename(filename)
            source_url = urljoin(self.WIMP2_PDF_URL, filename)
            destination = os.path.join(destination_dir, filename)

            # Don't download files already present
            if os.path.exists(destination):
                self.stdout.write(f"SKIP: {filename}")
                skipped += 1
                continue
            try:
                self.stdout.write(f"Downloading: {filename}")

                pdf_response = requests.get(source_url, timeout=60, stream=True)
                pdf_response.raise_for_status()

                with open(destination, "wb") as pdf_file:
                    for chunk in pdf_response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            pdf_file.write(chunk)
                downloaded += 1

            except requests.RequestException as exc:
                failed += 1
                self.stderr.write(self.style.ERROR(f"FAILED: {filename}: {exc}"))

        self.stdout.write(
            self.style.SUCCESS(
                "\nPDF import completed.\n"
                f"Found: {len(filenames)}\n"
                f"Downloaded: {downloaded}\n"
                f"Already existed: {skipped}\n"
                f"Failed: {failed}\n"
                f"Saved to: {destination_dir}"
            )
        )