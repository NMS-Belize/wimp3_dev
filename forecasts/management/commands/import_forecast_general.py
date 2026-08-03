# forecasts/management/commands/import_forecast_general.py

from datetime import datetime
from django.utils import timezone

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth import get_user_model

from forecasts.models import ForecastGeneral

User = get_user_model()

TABLE_NAME = "tbl_forecast_general"

COLUMN_NAMES = [
    "id",
    "forecast_date",
    "forecast_time",
    "forecast_type",
    "general_situation",
    "thr_forecast",
    "light_variable",
    "wind_speed",
    "wind_direction",
    "wind_condition",
    "wind_shift_speed",
    "wind_shift_direction",
    "wind_shift_condition",
    "sea_state",
    "wave",
    "sea_state_shift",
    "wave_shift",
    "advisory",
    "outlook",
    "coast_high_f",
    "coast_high_c",
    "coast_low_f",
    "coast_low_c",
    "inland_high_f",
    "inland_high_c",
    "inland_low_f",
    "inland_low_c",
    "hills_high_f",
    "hills_high_c",
    "hills_low_f",
    "hills_low_c",
    "publish_to_web",
    "forecaster_id",
    "created_by",
    "created_time",
    "updated_by",
    "updated_time",
    "auto_update",
]


def split_sql_statements(sql_text):
    """
    Split SQL into statements while respecting quoted text.

    This prevents semicolons inside forecast text from prematurely ending
    an INSERT statement.
    """
    statements = []
    current = []

    inside_string = False
    escaped = False

    for character in sql_text:
        current.append(character)

        if escaped:
            escaped = False
            continue

        if character == "\\" and inside_string:
            escaped = True
            continue

        if character == "'":
            inside_string = not inside_string
            continue

        if character == ";" and not inside_string:
            statement = "".join(current).strip()

            if statement:
                statements.append(statement)

            current = []

    remaining = "".join(current).strip()

    if remaining:
        statements.append(remaining)

    return statements


def parse_mysql_values(values_text):
    """
    Parse the VALUES section from a MySQL INSERT statement.

    Returns a list of rows. Each row is a list of Python values.
    """
    rows = []
    row = []
    value_buffer = []

    inside_string = False
    escaped = False
    inside_row = False
    depth = 0

    def finish_value():
        raw_value = "".join(value_buffer).strip()
        value_buffer.clear()

        if not raw_value:
            return ""

        if raw_value.upper() == "NULL":
            return None

        if (
            len(raw_value) >= 2
            and raw_value[0] == "'"
            and raw_value[-1] == "'"
        ):
            value = raw_value[1:-1]

            replacements = {
                r"\'": "'",
                r"\"": '"',
                r"\\": "\\",
                r"\n": "\n",
                r"\r": "\r",
                r"\t": "\t",
                r"\0": "\0",
            }

            for old, new in replacements.items():
                value = value.replace(old, new)

            return value

        try:
            return int(raw_value)
        except ValueError:
            pass

        try:
            return float(raw_value)
        except ValueError:
            return raw_value

    for character in values_text:
        if escaped:
            value_buffer.append(character)
            escaped = False
            continue

        if character == "\\" and inside_string:
            value_buffer.append(character)
            escaped = True
            continue

        if character == "'":
            inside_string = not inside_string
            value_buffer.append(character)
            continue

        if inside_string:
            value_buffer.append(character)
            continue

        if character == "(":
            if not inside_row:
                inside_row = True
                depth = 1
                row = []
                value_buffer = []
            else:
                depth += 1
                value_buffer.append(character)

            continue

        if character == ")" and inside_row:
            depth -= 1

            if depth == 0:
                row.append(finish_value())
                rows.append(row)

                row = []
                inside_row = False
                value_buffer = []
            else:
                value_buffer.append(character)

            continue

        if character == "," and inside_row and depth == 1:
            row.append(finish_value())
            continue

        if inside_row:
            value_buffer.append(character)

    return rows


def parse_date(value):
    if value is None:
        return None

    value = str(value).strip()

    if not value or value.startswith("0000-00-00"):
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def parse_time(value):
    if not value:
        return None

    return datetime.strptime(str(value), "%H:%M:%S").time()


def parse_datetime(value):
    if not value or str(value).startswith("0000-00-00"):
        return None

    value = str(value).strip()

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
    ]

    for date_format in formats:
        try:
            parsed_datetime = datetime.strptime(value, date_format)

            return timezone.make_aware(
                parsed_datetime,
                timezone.get_default_timezone(),
            )

        except ValueError:
            continue

    return None


def clean_required_text(value):
    """
    Required CharFields cannot receive None.
    """
    return "" if value is None else str(value)


def clean_optional_text(value):
    return None if value is None else str(value)


class Command(BaseCommand):
    help = "Import tbl_forecast_general records from a MySQL SQL dump."

    def add_arguments(self, parser):
        parser.add_argument(
            "sql_file",
            type=str,
            help="Path to the MySQL SQL dump.",
        )

        parser.add_argument(
            "--replace",
            action="store_true",
            help="Delete existing ForecastGeneral records before importing.",
        )

        parser.add_argument(
            "--update-existing",
            action="store_true",
            help="Update records whose primary-key IDs already exist.",
        )

        parser.add_argument(
            "--batch-size",
            type=int,
            default=500,
            help="Number of new records inserted per batch.",
        )

    def handle(self, *args, **options):
        sql_path = Path(options["sql_file"])

        if not sql_path.exists():
            raise CommandError(f"SQL file not found: {sql_path}")

        self.stdout.write(f"Reading: {sql_path}")

        sql_text = sql_path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        insert_prefix = f"INSERT INTO `{TABLE_NAME}` VALUES"

        statements = [
            statement
            for statement in split_sql_statements(sql_text)
            if statement.lstrip().startswith(insert_prefix)
        ]

        if not statements:
            raise CommandError(
                f"No INSERT statements found for `{TABLE_NAME}`."
            )

        self.stdout.write(
            f"Found {len(statements)} INSERT statement(s)."
        )

        parsed_rows = []

        for statement_number, statement in enumerate(statements, start=1):
            values_position = statement.find("VALUES")

            if values_position == -1:
                continue

            values_text = statement[values_position + len("VALUES"):].strip()

            if values_text.endswith(";"):
                values_text = values_text[:-1]

            rows = parse_mysql_values(values_text)

            self.stdout.write(
                f"Statement {statement_number}: {len(rows)} row(s)"
            )

            parsed_rows.extend(rows)

        if not parsed_rows:
            raise CommandError("No forecast records could be parsed.")

        invalid_rows = [
            row
            for row in parsed_rows
            if len(row) != len(COLUMN_NAMES)
        ]

        if invalid_rows:
            first_invalid = invalid_rows[0]

            raise CommandError(
                "A parsed row has the wrong number of columns. "
                f"Expected {len(COLUMN_NAMES)}, "
                f"received {len(first_invalid)}."
            )

        records = []

        skipped_invalid_dates = []

        for row in parsed_rows:
            data = dict(zip(COLUMN_NAMES, row))

            forecast_date = parse_date(data["forecast_date"])

            if forecast_date is None:
                skipped_invalid_dates.append(
                    {
                        "id": data["id"],
                        "forecast_date": data["forecast_date"],
                    }
                )
                continue

            created_user = User.objects.filter(
                id=data["created_by"]
            ).first()

            updated_user = User.objects.filter(
                id=data["updated_by"]
            ).first()

            record = ForecastGeneral(
                id=data["id"],
                forecast_date=forecast_date,
                forecast_time=parse_time(data["forecast_time"]),
                forecast_type=data["forecast_type"],

                general_situation=clean_required_text(
                    data["general_situation"]
                ),
                thr_forecast=clean_required_text(data["thr_forecast"]),

                light_variable=data["light_variable"],

                wind_speed=clean_required_text(data["wind_speed"]),
                wind_direction=clean_optional_text(
                    data["wind_direction"]
                ),
                wind_condition=clean_optional_text(
                    data["wind_condition"]
                ),

                wind_shift_speed=clean_optional_text(
                    data["wind_shift_speed"]
                ),
                wind_shift_direction=clean_optional_text(
                    data["wind_shift_direction"]
                ),
                wind_shift_condition=clean_optional_text(
                    data["wind_shift_condition"]
                ),

                sea_state=clean_required_text(data["sea_state"]),
                wave=clean_optional_text(data["wave"]),

                sea_state_shift=clean_optional_text(
                    data["sea_state_shift"]
                ),
                wave_shift=clean_optional_text(data["wave_shift"]),

                advisory=clean_required_text(data["advisory"]),
                outlook=clean_required_text(data["outlook"]),

                coast_high_f=data["coast_high_f"],
                coast_high_c=data["coast_high_c"],
                coast_low_f=data["coast_low_f"],
                coast_low_c=data["coast_low_c"],

                inland_high_f=data["inland_high_f"],
                inland_high_c=data["inland_high_c"],
                inland_low_f=data["inland_low_f"],
                inland_low_c=data["inland_low_c"],

                hills_high_f=data["hills_high_f"],
                hills_high_c=data["hills_high_c"],
                hills_low_f=data["hills_low_f"],
                hills_low_c=data["hills_low_c"],

                publish_to_web=bool(data["publish_to_web"]),
                forecaster_id=data["forecaster_id"],

                created_by = created_user,
                created_time = parse_datetime(data["created_time"]),

                updated_by = updated_user,
                updated_time=parse_datetime(data["updated_time"]),

                auto_update=parse_datetime(data["auto_update"]),
            )

            records.append(record)

        batch_size = options["batch_size"]
        update_existing = options["update_existing"]

        with transaction.atomic():
            if options["replace"]:
                deleted_count, _ = ForecastGeneral.objects.all().delete()

                self.stdout.write(
                    self.style.WARNING(
                        f"Deleted {deleted_count} existing record(s)."
                    )
                )

            existing_ids = set(
                ForecastGeneral.objects.filter(
                    id__in=[record.id for record in records]
                ).values_list("id", flat=True)
            )

            new_records = [
                record
                for record in records
                if record.id not in existing_ids
            ]

            updated_count = 0

            if update_existing:
                field_names = [
                    field.name
                    for field in ForecastGeneral._meta.fields
                    if field.name != "id"
                ]

                for record in records:
                    if record.id not in existing_ids:
                        continue

                    values = {
                        field_name: getattr(record, field_name)
                        for field_name in field_names
                    }

                    ForecastGeneral.objects.filter(
                        id=record.id
                    ).update(**values)

                    updated_count += 1

            ForecastGeneral.objects.bulk_create(
                new_records,
                batch_size=batch_size,
            )

        skipped_count = len(existing_ids)

        if update_existing:
            skipped_count = 0

        if skipped_invalid_dates:
            self.stdout.write(
                self.style.WARNING(
                    f"\nSkipped {len(skipped_invalid_dates)} row(s) "
                    "with invalid forecast dates."
                )
            )

            for item in skipped_invalid_dates[:20]:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipped ID {item['id']}: "
                        f"forecast_date={item['forecast_date']!r}"
                    )
                )

            if len(skipped_invalid_dates) > 20:
                self.stdout.write(
                    self.style.WARNING(
                        f"...and {len(skipped_invalid_dates) - 20} more."
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "\nImport completed successfully.\n"
                f"SQL rows parsed: {len(parsed_rows)}\n"
                f"Valid rows processed: {len(records)}\n"
                f"Invalid-date rows skipped: {len(skipped_invalid_dates)}\n"
                f"New rows imported: {len(new_records)}\n"
                f"Existing rows updated: {updated_count}\n"
                f"Existing rows skipped: {skipped_count}"
            )
        )