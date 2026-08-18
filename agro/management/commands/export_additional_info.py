import json
from pathlib import Path

from django.core.management.base import BaseCommand
from agro.models import PestRiskInfo


class Command(BaseCommand):
    help = "Export PestRiskInfo records to JSON"

    def handle(self, *args, **options):

        output_dir = Path("agro/data")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "additional_info.json"

        records = PestRiskInfo.objects.select_related("commodity").order_by("commodity_id","info_description")

        data = []

        for obj in records:
            data.append({
                "id": obj.id,
                "commodity": obj.commodity_id,
                "info_description": obj.info_description,
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
                f"Exported {len(data)} PestRiskInfo records to {output_file}"
            )
        )