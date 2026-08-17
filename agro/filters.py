# inventory/filters.py

import django_filters
from django import forms

from django.contrib.auth.models import User
from .models import PestRiskInfo, Sector, PestRiskEffect

class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        full_name = user.get_full_name()
        return full_name if full_name else user.username

class UserModelChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = UserChoiceField
    
class InfoItemFilter(django_filters.FilterSet):

    info_description    = django_filters.CharFilter(lookup_expr="icontains", label="Description")
    sector              = django_filters.ModelChoiceFilter(queryset=Sector.objects.all(), label="Sector", empty_label="All Sectors")
    
    class Meta:
        model = PestRiskInfo
        fields = [ "info_description", "sector"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.fields["info_description"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Search Description..."
        })

        self.form.fields["sector"].widget.attrs.update({
            "class": "form-select color-select"
        })

class EffectItemFilter(django_filters.FilterSet):

    effect_description    = django_filters.CharFilter(lookup_expr="icontains", label="Description")
    sector              = django_filters.ModelChoiceFilter(queryset=Sector.objects.all(), label="Sector", empty_label="All Sectors")
    
    class Meta:
        model = PestRiskEffect
        fields = [ "effect_description", "sector"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.fields["effect_description"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Search Description..."
        })

        self.form.fields["sector"].widget.attrs.update({
            "class": "form-select color-select"
        })