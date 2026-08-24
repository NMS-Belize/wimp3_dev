# inventory/filters.py

import django_filters
from django import forms

from django.contrib.auth.models import User
from .models import ForecastGeneral, ForescastGeneralCategory

class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        full_name = user.get_full_name()
        return full_name if full_name else user.username

class UserModelChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = UserChoiceField
    
class ForecastGeneralFilter(django_filters.FilterSet):

    forecast_date   = django_filters.DateFilter(lookup_expr="icontains", label="Forecast Date")
    forecast_time   = django_filters.CharFilter(lookup_expr="icontains", label="Forecast Time")
    forecast_category = django_filters.ModelChoiceFilter(queryset=ForescastGeneralCategory.objects.all(), label="Forecast Category", empty_label="All Categories")
    general_situation   = django_filters.CharFilter(lookup_expr="icontains", label="General Situation")

    created_by      = UserModelChoiceFilter(queryset=User.objects.filter(is_active=True).order_by("first_name","last_name","username"), label="Forecaster", empty_label="All Forecasters")
    updated_by      = UserModelChoiceFilter(queryset=User.objects.filter(is_active=True).order_by("first_name","last_name","username"), label="Forecaster", empty_label="All Forecasters")

    class Meta:
        model = ForecastGeneral
        fields = ["forecast_date","forecast_time", "forecast_category", "general_situation", "created_by", "updated_by"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.form.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({"class": "form-select" })
            else:
                field.widget.attrs.update({ "class": "form-control", "placeholder":"" })