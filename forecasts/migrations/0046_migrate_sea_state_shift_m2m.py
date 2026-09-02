import ast

from django.db import migrations


def migrate_sea_state_shift(apps, schema_editor):

    ForecastGeneral = apps.get_model(
        "forecasts",
        "ForecastGeneral"
    )

    SeaState = apps.get_model(
        "forecasts",
        "SeaState"
    )

    for forecast in ForecastGeneral.objects.only(
                "id",
                "sea_state"
            ).iterator():

        old_value = forecast.sea_state_shift

        if old_value in (None, "", "[]"):
            continue

        try:
            parsed = ast.literal_eval(str(old_value))
        except (ValueError, SyntaxError, TypeError):
            continue

        # Single value:
        # "5" -> [5]
        if isinstance(parsed, int):
            ids = [parsed]

        # Multiple values:
        # "[4,5]" -> [4,5]
        elif isinstance(parsed, list):
            ids = parsed

        else:
            continue

        sea_states = SeaState.objects.filter(
            id__in=ids
        )

        forecast.sea_state_shift_m2m.set(
            sea_states
        )


def reverse_migration(apps, schema_editor):

    ForecastGeneral = apps.get_model(
        "forecasts",
        "ForecastGeneral"
    )

    for forecast in ForecastGeneral.objects.all():

        ids = list(
            forecast.sea_state_shift_m2m.values_list(
                "id",
                flat=True
            )
        )

        forecast.sea_state_shift = str(ids)

        forecast.save(
            update_fields=["sea_state_shift"]
        )


class Migration(migrations.Migration):

    dependencies = [
        ("forecasts", "0045_forecastgeneral_sea_state_shift_m2m"),
    ]

    operations = [
        migrations.RunPython(
            migrate_sea_state_shift,
            reverse_migration
        ),
    ]