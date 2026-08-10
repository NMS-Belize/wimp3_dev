from django.core.management.base import BaseCommand
from django.db import connections, transaction

from forecasts.models import ForecastGeneral

class Command(BaseCommand):

    help = "Import ForecastGeneral records from the legacy MySQL database."

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0
        skipped_count = 0

        sql = """
            SELECT id, forecast_date, forecast_time, forecast_type, general_situation, thr_forecast, light_variable, wind_speed,wind_direction, wind_condition, wind_shift_speed, wind_shift_direction, wind_shift_condition, sea_state, wave, sea_state_shift,
                wave_shift, advisory, outlook, coast_high_f, coast_high_c, coast_low_f, coast_low_c, inland_high_f, inland_high_c, inland_low_f, inland_low_c, hills_high_f, hills_high_c, hills_low_f, hills_low_c, forecaster_id,
                created_by, created_time, updated_by, updated_time
            FROM tbl_forecast_general
            WHERE forecast_date IS NOT NULL
            AND forecast_date <> '0000-00-00'
            ORDER BY id;
        """

        try:
            with connections["legacy"].cursor() as cursor:
                cursor.execute(sql)

                column_names = [
                    column[0]
                    for column in cursor.description
                ]

                rows = [
                    dict(zip(column_names, row))
                    for row in cursor.fetchall()
                ]

        except Exception as exc:
            self.stderr.write(
                self.style.ERROR(f"Could not read the legacy database: {exc}")
            )
            return

        with transaction.atomic(using="default"):
            for row in rows:

                legacy_id       = row.get("id")
                forecast_date   = row.get("forecast_date")
                forecast_time   = row.get("forecast_time")
                forecast_type   = row.get("forecast_type")
                general_situation  = row.get("general_situation")
                tfhr_forecast   = row.get("thr_forecast")
                light_variable   = row.get("light_variable")
                wind_speed      = row.get("wind_speed")
                wind_direction  = row.get("wind_direction")
                wind_condition  = row.get("wind_condition")
                wind_shift_speed = row.get("wind_shift_speed")
                wind_shift_direction = row.get("wind_shift_direction")
                wind_shift_condition = row.get("wind_shift_condition")
                sea_state       = row.get("sea_state")
                wave            = row.get("wave")
                sea_state_shift = row.get("sea_state_shift")
                wave_shift      = row.get("wave_shift")
                advisory        = row.get("advisory")
                outlook         = row.get("outlook")
                coast_high_f    = row.get("coast_high_f")
                coast_high_c    = row.get("coast_high_c")
                coast_low_f     = row.get("coast_low_f")
                coast_low_c     = row.get("coast_low_c")
                inland_high_f   = row.get("inland_high_f")
                inland_high_c   = row.get("inland_high_c")
                inland_low_f    = row.get("inland_low_f")
                inland_low_c    = row.get("inland_low_c")
                hills_high_f    = row.get("hills_high_f")
                hills_high_c    = row.get("hills_high_c")
                hills_low_f     = row.get("hills_low_f")
                hills_low_c     = row.get("hills_low_c")
                forecaster_id   = row.get("forecaster_id")
                created_by      = row.get("created_by")
                created_time    = row.get("created_time")
                updated_by      = row.get("updated_by")
                updated_time    = row.get("updated_time")

                if not legacy_id or not forecast_date:
                    skipped_count += 1
                    continue

                _, created = ForecastGeneral.objects.using(
                    "default"
                ).update_or_create(
                    id = legacy_id,
                    legacy_id = legacy_id,
                    defaults={
                        "legacy_id":        legacy_id,
                        "forecast_date":    forecast_date,
                        "forecast_time":    forecast_time,
                        "forecast_category":    forecast_type,
                        "general_situation": general_situation,
                        "twenty_four_hour_forecast": tfhr_forecast,
                        "light_variable":   light_variable,
                        "wind_speed": wind_speed,
                        "wind_direction": wind_direction,
                        "wind_condition": wind_condition,
                        "wind_shift_speed": wind_shift_speed,
                        "wind_shift_direction": wind_shift_direction,
                        "wind_shift_condition": wind_shift_condition,
                        "sea_state": sea_state,
                        "wave": wave,
                        "sea_state_shift": sea_state_shift,
                        "wave_shift": wave_shift,
                        "advisory": advisory,
                        "outlook": outlook,
                        "coast_high_f": coast_high_f,
                        "coast_high_c": coast_high_c,
                        "coast_low_f": coast_low_f,
                        "coast_low_c": coast_low_c,
                        "inland_high_f": inland_high_f,
                        "inland_high_c": inland_high_c,
                        "inland_low_f": inland_low_f,
                        "inland_low_c": inland_low_c,
                        "hills_high_f": hills_high_f,
                        "hills_high_c": hills_high_c,
                        "hills_low_f": hills_low_f,
                        "hills_low_c": hills_low_c,
                        "forecaster_id": forecaster_id,
                        "created_by": created_by,
                        "created_datetime": created_time,
                        "updated_by": updated_by,
                        "updated_datetime": updated_time,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Legacy forecast import completed. "
                f"Created: {created_count}, "
                f"Updated: {updated_count}, "
                f"Skipped: {skipped_count}."
            )
        )