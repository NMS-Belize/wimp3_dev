import json
from pathlib import Path

from django.core.management.base import BaseCommand
from agro.models import PestRiskAction


class Command(BaseCommand):
    help = "Export PestRiskAction records to JSON"

    def handle(self, *args, **options):

        output_dir = Path("agro/data")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "actions.json"

        records = PestRiskAction.objects.select_related("commodity").order_by("commodity_id","action_description")

        data = []

        for obj in records:
            data.append({
                "id": obj.id,
                "commodity": obj.commodity_id,
                "action_description": obj.action_description,
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
                f"Exported {len(data)} PestRiskAction records to {output_file}"
            )
        )