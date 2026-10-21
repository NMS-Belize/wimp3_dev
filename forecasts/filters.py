# inventory/filters.py

import django_filters
from django import forms

from django.contrib.auth.models import User
from .models import ForecastGeneral, ForescastGeneralCategory, ForecastMarine, ForecastMarineCategory, DistrictForecast

class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        full_name = user.get_full_name()
        return full_name if full_name else user.username

class UserModelChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = UserChoiceField
    
class ForecastGeneralFilter(django_filters.FilterSet):

    forecast_date   = django_filters.DateFilter(lookup_expr="exact", label="Forecast Date",  widget=forms.DateInput(attrs={ "type": "date", "class": "form-control" }, format="%Y-%m-%d"))
    forecast_category = django_filters.ModelChoiceFilter(queryset=ForescastGeneralCategory.objects.all(), label="Forecast Category", empty_label="All Categories")

    created_by      = UserModelChoiceFilter(queryset=User.objects.filter(is_active=True).order_by("first_name","last_name","username"), label="Forecaster", empty_label="All Forecasters")
    updated_by      = UserModelChoiceFilter(queryset=User.objects.filter(is_active=True).order_by("first_name","last_name","username"), label="Forecaster", empty_label="All Forecasters")

    class Meta:
        model = ForecastGeneral
        fields = ["forecast_date","forecast_time", "forecast_category","created_by", "updated_by"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.fields["forecast_date"].input_formats = ["%d/%m/%Y","%Y-%m-%d"]

        for field in self.form.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({"class": "form-select" })
            else:
                field.widget.attrs.update({ "class": "form-control", "placeholder":"" })

class ForecastMarineFilter(django_filters.FilterSet):

    forecast_date   = django_filters.DateFilter(lookup_expr="exact", label="Forecast Date",  widget=forms.DateInput(attrs={ "type": "date", "class": "form-control" }, format="%Y-%m-%d"))
    forecast_category = django_filters.ModelChoiceFilter(queryset=ForecastMarineCategory.objects.all(), label="Forecast Category", empty_label="All Categories")

    created_by      = UserModelChoiceFilter(queryset=User.objects.filter(is_active=True).order_by("first_name","last_name","username"), label="Forecaster", empty_label="All Forecasters")
    updated_by      = UserModelChoiceFilter(queryset=User.objects.filter(is_active=True).order_by("first_name","last_name","username"), label="Forecaster", empty_label="All Forecasters")

    class Meta:
        model = ForecastMarine
        fields = ["forecast_date","forecast_time", "forecast_category", "created_by", "updated_by"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.fields["forecast_date"].input_formats = ["%d/%m/%Y","%Y-%m-%d"]

        for field in self.form.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({ "class": "form-select" })
            else:
                field.widget.attrs.update({ "class": "form-control", "placeholder": "" })

class ForecastMunicipalityFilter(django_filters.FilterSet):

    forecast_date   = django_filters.DateFilter(lookup_expr="exact", label="Forecast Date",  widget=forms.DateInput(attrs={ "type": "date", "class": "form-control" }, format="%Y-%m-%d"))
    forecast_category = django_filters.ModelChoiceFilter(queryset=ForecastMarineCategory.objects.all(), label="Forecast Category", empty_label="All Categories")

    created_by      = UserModelChoiceFilter(queryset=User.objects.filter(is_active=True).order_by("first_name","last_name","username"), label="Forecaster", empty_label="All Forecasters")
    updated_by      = UserModelChoiceFilter(queryset=User.objects.filter(is_active=True).order_by("first_name","last_name","username"), label="Forecaster", empty_label="All Forecasters")

    class Meta:
        model = ForecastMarine
        fields = ["forecast_date","forecast_time", "forecast_category", "created_by", "updated_by"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.fields["forecast_date"].input_formats = ["%d/%m/%Y","%Y-%m-%d"]

        for field in self.form.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({ "class": "form-select" })
            else:
                field.widget.attrs.update({ "class": "form-control", "placeholder": "" })

class DistrictForecastFilter(django_filters.FilterSet):

    forecast_date   = django_filters.DateFilter(lookup_expr="exact", label="Forecast Date",  widget=forms.DateInput(attrs={ "type": "date", "class": "form-control" }, format="%Y-%m-%d"))

    created_by      = UserModelChoiceFilter(queryset=User.objects.filter(is_active=True).order_by("first_name","last_name","username"), label="Forecaster", empty_label="All Forecasters")
    updated_by      = UserModelChoiceFilter(queryset=User.objects.filter(is_active=True).order_by("first_name","last_name","username"), label="Forecaster", empty_label="All Forecasters")

    class Meta:
        model = DistrictForecast
        fields = ["forecast_date","created_by","updated_by"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.fields["forecast_date"].input_formats = ["%d/%m/%Y","%Y-%m-%d"]

        for field in self.form.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({ "class": "form-select" })
            else:
                field.widget.attrs.update({ "class": "form-control", "placeholder": "" })