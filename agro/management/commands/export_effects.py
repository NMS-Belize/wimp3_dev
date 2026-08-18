import json
from pathlib import Path

from django.core.management.base import BaseCommand
from agro.models import PestRiskEffect


class Command(BaseCommand):
    help = "Export PestRiskEffect records to JSON"

    def handle(self, *args, **options):

        output_dir = Path("agro/data")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "effects.json"

        records = PestRiskEffect.objects.select_related("commodity").order_by("commodity_id","effect_description")

        data = []

        for obj in records:
            data.append({
                "id": obj.id,
                "commodity": obj.commodity_id,
                "effect_description": obj.effect_description,
            })

        with output_file.open("w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Exported {len(data)} PestRiskEffect records to {output_file}"
            )
        )