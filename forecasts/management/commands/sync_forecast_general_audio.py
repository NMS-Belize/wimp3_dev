import os
import json
import urllib.request

from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

API_URL = "https://wimp.nms.gov.bz/api/forecast_general/read.php"


class Command(BaseCommand):

    help = "Synchronize the current forecast audio from WIMP2."

    def handle(self, *args, **options):

        audio_dir   = os.path.join(settings.MEDIA_ROOT, "forecast", "general", "audio")
        state_file  = os.path.join(audio_dir, "audio_state.json")

        os.makedirs(audio_dir, exist_ok=True)

        self.stdout.write( "=" * 60)
        self.stdout.write(f"WIMP2 audio check: "f"{datetime.now():%Y-%m-%d %H:%M:%S}")

        try:
            # GET ACTIVE FORECAST
            request = urllib.request.Request(API_URL, headers={ "User-Agent": "WIMP3 Audio Sync" })

            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))

            forecasts = data.get("forecast_data", [])

            if not forecasts:
                self.stdout.write(self.style.WARNING("No active forecast found."))
                return

            forecast    = forecasts[0]
            audio_url   = forecast.get("audio")

            if not audio_url:
                self.stdout.write(self.style.WARNING("Active forecast contains no audio."))
                return

            filename = (forecast.get("audio_basename") or os.path.basename(audio_url))

            self.stdout.write(f"Active audio: {filename}")

            # CHECK ACTUAL REMOTE FILE
            head_request = urllib.request.Request(audio_url, method="HEAD", headers={"User-Agent": "WIMP3 Audio Sync"})

            with urllib.request.urlopen(head_request,timeout=30) as response:
                remote_info = {
                    "last_modified":    response.headers.get("Last-Modified"),
                    "etag":             response.headers.get("ETag"),
                    "content_length":   response.headers.get("Content-Length"),
                }

            # LOAD STATE
            state = {}

            if os.path.exists(state_file):

                try:
                    with open(state_file,"r") as f:
                        state = json.load(f)
                except (OSError,json.JSONDecodeError):
                    state = {}

            local_file = os.path.join(audio_dir, filename)

            # DETERMINE IF DOWNLOAD REQUIRED
            download_required = False
            reason = ""

            if not os.path.exists(local_file):
                download_required = True
                reason = "Local audio file missing"

            elif filename != state.get("filename"):
                download_required = True
                reason = "New active audio filename"

            elif (remote_info["last_modified"] and remote_info["last_modified"] != state.get("last_modified")):
                download_required = True
                reason = "Remote audio modified"

            elif (remote_info["etag"] and remote_info["etag"] != state.get("etag")):
                download_required = True
                reason = "Remote ETag changed"

            elif (remote_info["content_length"] and remote_info["content_length"] != state.get("content_length")):
                download_required = True
                reason = "Remote file size changed"

            # -----------------------------------------
            if not download_required:
                self.stdout.write(self.style.SUCCESS("Audio has not changed."))
                self.stdout.write("No download required.")
                return

            self.stdout.write(f"Update detected: {reason}")

            # DOWNLOAD
            temp_file = local_file + ".tmp"
            download_request = urllib.request.Request(audio_url,headers={"User-Agent": "WIMP3 Audio Sync"})

            with urllib.request.urlopen(download_request,timeout=60) as response:
                with open(temp_file,"wb") as output:
                    while True:
                        chunk = response.read(1024 * 1024)

                        if not chunk:
                            break

                        output.write(chunk)

            # Atomic replacement
            os.replace(temp_file,local_file)

            self.stdout.write(f"Stored: {local_file}")

            # SAVE STATE
            state = {
                "forecast_id":      forecast.get("id"),
                "forecast_date":    forecast.get("forecast_date"),
                "forecast_time":    forecast.get("forecast_time"),
                "filename":         filename,
                "audio_url":        audio_url,
                "last_modified":    remote_info[ "last_modified"],
                "etag":             remote_info["etag"],
                "content_length":   remote_info["content_length"],
                "downloaded_at":    datetime.now().isoformat()
            }

            with open(state_file,"w") as f:
                json.dump(state, f, indent=4)

            self.stdout.write(self.style.SUCCESS("Audio synchronization completed."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Audio synchronization failed: {e}"))