from datetime import timezone
from unicodedata import category

from click import option
from django import forms
from pytz import timezone
from .models import TropicalWeatherAlertsCategory, TropicalWeatherAlerts

from django.forms import inlineformset_factory

from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from django.core.exceptions import ValidationError

from django.db.models.functions import Lower
from django.db.models import Q

from django.utils import timezone

today = timezone.now().date()

class ColorSelect(forms.Select):
    def create_option(
        self, name, value, label, selected, index,
        subindex=None, attrs=None
    ):

        option = super().create_option(
            name, value, label, selected, index,
            subindex=subindex, attrs=attrs
        )

        if value:

            severity_id = value.value if hasattr(value, "value") else value
            severity    = AlertLevel.objects.filter(pk=severity_id).first()

            if severity and severity.color:
                #option["attrs"]["style"] = (
                #    f"color: {severity.color} !important; "
                #)
                option["attrs"]["class"] = (f"{severity.description.lower()}")
                

        return option

class TropicalWeatherAlertsCategoryForm(forms.ModelForm):
    class Meta:
        model = TropicalWeatherAlertsCategory
        fields = ['category_name']
        labels = {   
            # <-- add human-friendly labels here
            'category_name': 'Category Name:'
        }
        widgets = {            
            'category_name': forms.TextInput(attrs={'class': 'form-control'})
        }

class TropicalWeatherAlertsForm(forms.ModelForm):
    class Meta:
        model = TropicalWeatherAlerts
        fields = ['storm_name', 'storm_category', 'description']

        labels = {   
            # <-- add human-friendly labels here
            'storm_name': 'Storm Name:',
            'storm_category': 'Category:',
            'description': 'Description:',
            
        }
        widgets = { 
            'storm_name':       forms.TextInput(attrs={"class": "form-control"}),
            'storm_category':   forms.Select(attrs={'class': 'form-select'}),
            'description':      forms.Textarea(attrs={'class': 'form-control'}),
        }