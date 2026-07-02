# inventory/filters.py

import django_filters
from .models import InventoryItem

class InventoryItemFilter(django_filters.FilterSet):
    device_label = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Device Label"
    )

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
            #"device_label",
            "device_name",
            "assigned_user",
            "serial_number",
            "device_status",
            "category",
            "device_type",
            "department_section",
            "placement",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.form.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })