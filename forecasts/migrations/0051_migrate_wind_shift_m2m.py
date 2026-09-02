import ast

from django.db import migrations


def parse_ids(value):
    if value in (None, "", "[]"):
        return []

    try:
        parsed = ast.literal_eval(str(value))
    except (ValueError, SyntaxError, TypeError):
        return []

    if isinstance(parsed, int):
        return [parsed]

    if isinstance(parsed, list):
        return parsed

    return []


def migrate_wind_shift_fields(apps, schema_editor):

    ForecastGeneral = apps.get_model(
        "forecasts",
        "ForecastGeneral"
    )

    WindDirection = apps.get_model(
        "forecasts",
        "WindDirection"
    )

    WindCondition = apps.get_model(
        "forecasts",
        "WindCondition"
    )

    for forecast in ForecastGeneral.objects.all():

        # Wind Shift Direction
        direction_ids = parse_ids(
            forecast.wind_shift_direction
        )

        if direction_ids:
            forecast.wind_shift_direction_m2m.set(
                WindDirection.objects.filter(
                    id__in=direction_ids
                )
            )

        # Wind Shift Condition
        condition_ids = parse_ids(
            forecast.wind_shift_condition
        )

        if condition_ids:
            forecast.wind_shift_condition_m2m.set(
                WindCondition.objects.filter(
                    id__in=condition_ids
                )
            )


def reverse_migration(apps, schema_editor):

    ForecastGeneral = apps.get_model(
        "forecasts",
        "ForecastGeneral"
    )

    for forecast in ForecastGeneral.objects.all():

        direction_ids = list(
            forecast.wind_shift_direction_m2m.values_list(
                "id",
                flat=True
            )
        )

        condition_ids = list(
            forecast.wind_shift_condition_m2m.values_list(
                "id",
                flat=True
            )
        )

        forecast.wind_shift_direction = str(direction_ids)
        forecast.wind_shift_condition = str(condition_ids)

        forecast.save(
            update_fields=[
                "wind_shift_direction",
                "wind_shift_condition",
            ]
        )


class Migration(migrations.Migration):

    dependencies = [
        ("forecasts", "0050_forecastgeneral_wind_shift_condition_m2m_and_more"),
    ]

    operations = [
        migrations.RunPython(
            migrate_wind_shift_fields,
            reverse_migration
        ),
    ]