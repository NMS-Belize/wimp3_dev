# inventory/filters.py

import django_filters
from .models import InventoryItem

class InventoryItemFilter(django_filters.FilterSet):

    device_name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Device Name"
    )

    assigned_user = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Assigned User"
    )

    serial_number = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Serial Number"
    )

    class Meta:
        model = InventoryItem
        fields = [
            "device_name",
            "category",
            "serial_number",
            "department_section",
            "assigned_user",
            "device_status",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.form.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })