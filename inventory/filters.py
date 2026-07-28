# inventory/filters.py

import django_filters
from django import forms

from django.contrib.auth.models import User
from .models import InventoryItem

class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        full_name = user.get_full_name()
        return full_name if full_name else user.username

class UserModelChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = UserChoiceField
    
class InventoryItemFilter(django_filters.FilterSet):

    device_name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Device Name",
    )

    assigned_user = UserModelChoiceFilter(
        queryset=User.objects.filter(is_active=True).order_by(
            "first_name",
            "last_name",
            "username",
        ),
        label="Assigned User",
        empty_label="All Users",
    )

    serial_number = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Serial Number",
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
                "class": "form-control",
                 })