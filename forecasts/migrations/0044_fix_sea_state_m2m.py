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

    for forecast in ForecastGeneral.objects.only(
            "id",
            "sea_state"
        ).iterator():

        old_value = forecast.sea_state

        if old_value in (None, "", "[]"):
            continue

        try:
            parsed = ast.literal_eval(str(old_value))
        except (ValueError, SyntaxError, TypeError):
            continue

        if isinstance(parsed, int):
            ids = [parsed]
        elif isinstance(parsed, list):
            ids = parsed
        else:
            continue

        forecast.sea_state_m2m.set(
            SeaState.objects.filter(id__in=ids)
        )


class Migration(migrations.Migration):

    dependencies = [
        ("forecasts", "0043_migrate_sea_conditions"),
    ]

    operations = [
        migrations.RunPython(
            migrate_sea_state,
            migrations.RunPython.noop
        ),
    ]