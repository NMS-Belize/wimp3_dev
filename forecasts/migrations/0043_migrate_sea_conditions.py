import ast

from django.db import migrations


def migrate_sea_state(apps, schema_editor):
    ForecastGeneral = apps.get_model(
        "forecasts",
        "ForecastGeneral"
    )

    SeaState = apps.get_model(
        "forecasts",
        "SeaState"
    )

    # Only retrieve fields that actually exist and are needed.
    # This avoids Django trying to SELECT the old thr_forecast column.
    for forecast in ForecastGeneral.objects.only(
        "id",
        "sea_state"
    ).iterator():

        old_value = forecast.sea_state

        if not old_value:
            continue

        try:
            ids = ast.literal_eval(old_value)
        except (ValueError, SyntaxError, TypeError):
            continue

        if not isinstance(ids, list):
            continue

        conditions = SeaState.objects.filter(
            id__in=ids
        )

        forecast.sea_state_m2m.set(conditions)


def reverse_migration(apps, schema_editor):
    ForecastGeneral = apps.get_model(
        "forecasts",
        "ForecastGeneral"
    )

    for forecast in ForecastGeneral.objects.only(
        "id",
        "sea_state"
    ).iterator():

        ids = list(
            forecast.sea_state_m2m.values_list(
                "id",
                flat=True
            )
        )

        forecast.sea_state = str(ids)

        forecast.save(
            update_fields=["sea_state"]
        )


class Migration(migrations.Migration):

    dependencies = [
        ("forecasts", "0042_forecastgeneral_sea_state_m2m"),
    ]

    operations = [
        migrations.RunPython(
            migrate_sea_state,
            reverse_migration
        ),
    ]