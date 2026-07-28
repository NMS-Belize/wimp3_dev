from datetime import timezone
from unicodedata import category

from click import option
from django import forms
from pytz import timezone
from .models import DistrictForecast, ForecastGeneral, DistrictForecastDetails, DistrictForecastInstructions, DistrictForecastInstructionsCategory, Probability, Severity

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

class DistrictForecastInstructionsCategoryForm(forms.ModelForm):
    class Meta:
        model = DistrictForecastInstructionsCategory
        fields = ['category_name']
        labels = {   
            # <-- add human-friendly labels here
            'category_name': 'Category Name:'
        }
        widgets = {            
            'category_name': forms.TextInput(attrs={'class': 'form-control'})
        }

class DistrictForecastInstructionsForm(forms.ModelForm):
    class Meta:
        model = DistrictForecastInstructions
        fields = ['description', 'category']
        labels = {   
            # <-- add human-friendly labels here
            'description': 'Description:',
            'category': 'Category:'
        }
        widgets = {            
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'})
        }

class SeverityForm(forms.ModelForm):
    class Meta:
        model = Severity
        fields = ['description', 'color']
        labels = {   
            # <-- add human-friendly labels here
            'description': 'Description:',
            'color': 'Color HEX',
        }
        widgets = {            
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'})
        }

class ProbabilityForm(forms.ModelForm):
    class Meta:
        model = Probability
        fields = ['description', 'color']
        labels = {   
            # <-- add human-friendly labels here
            'description': 'Description:',
            'color': 'Color HEX',
        }
        widgets = {            
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'})
        }

class DistrictForecastForm(forms.ModelForm):
    class Meta:
        model = DistrictForecast
        fields = ['forecast_date']
        labels = {   
            # <-- add human-friendly labels here
            'forecast_date': 'Forecast Date:',
            #'is_published': 'Is Published:'
        }
        widgets = {            
            'forecast_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            #'is_published': DjangoToggleSwitchWidget(attrs={'class': 'form-check-input'})
            #'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'})
        }

    def clean_forecast_date(self):
        forecast_date = self.cleaned_data.get("forecast_date")

        if forecast_date and forecast_date < timezone.now().date():
            raise forms.ValidationError(
                "Forecast date cannot be earlier than today."
            )

        qs = DistrictForecast.objects.filter(forecast_date=forecast_date)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "A forecast already exists for this date."
            )

        return forecast_date
    
class DistrictForecastPublishForm(forms.ModelForm):
    class Meta:
        model = DistrictForecast
        fields = ['is_published']
        labels = {   
            # <-- add human-friendly labels here
            'is_published': 'Is Published:'
        }
        widgets = {            
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'})
        }

class DistrictForecastDetailsForm(forms.ModelForm):
    
    class Meta:
        model = DistrictForecastDetails
        fields = [ 
            'temp_max', 'prob_temp_max', 'sev_temp_max', 'risk_temp_max', 'ins_temp_max',
            'temp_min', 'prob_temp_min', 'sev_temp_min', 'risk_temp_min', 'ins_temp_min',
            'winds_min', 'winds_max', 'prob_winds', 'sev_winds', 'risk_winds', 'ins_winds',
            'precip_max', 'prob_precip_max', 'sev_precip_max', 'risk_precip_max', 'ins_precip_max',
            'weather_conditions', 'prob_weather_conditions', 'sev_weather_conditions', 'risk_weather_conditions', 'ins_weather_conditions'
        ]
        widgets = { 
            'weather_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 20, 'style': 'width: 100%'}),
            'prob_weather_conditions': forms.Select(attrs={'class': 'form-select color-select', 'width': '100%'}),
            'sev_weather_conditions': forms.Select(attrs={'class': 'form-select color-select', 'width': '100%'}),
            #'risk_weather_conditions': forms.Select(attrs={'class': 'form-control','style': 'display:none','placeholder': ''}),
            'risk_weather_conditions': forms.HiddenInput(),
            'ins_weather_conditions': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),

            'temp_max': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.5', 'width': '100%'}),
            'prob_temp_max': forms.Select(attrs={'class': 'form-select color-select','width': '100%'}),
            'sev_temp_max': forms.Select(attrs={'class': 'form-select color-select', 'width': '100%'}),
            'risk_temp_max': forms.HiddenInput(),
            'ins_temp_max': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),

            'temp_min': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.5', 'width': '100%'}),
            'prob_temp_min': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),
            'sev_temp_min': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),
            'risk_temp_min': forms.HiddenInput(),
            'ins_temp_min': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),

            'winds_min': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.5', 'width': '45%'}),
            'winds_max': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.5', 'width': '45%'}),
            'prob_winds': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),
            'sev_winds': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),
            'risk_winds': forms.HiddenInput(),
            'ins_winds': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),

            'precip_max': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.25', 'width': '100%'}),
            'prob_precip_max': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),
            'sev_precip_max': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),
            'risk_precip_max': forms.HiddenInput(),
            'ins_precip_max': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ins_weather_conditions'].queryset = (
            DistrictForecastInstructions.objects.filter(
                Q(category__category_name="Weather Conditions") |
                Q(category__category_name="Uncategorized")
            ).order_by(Lower('description'))
        )

        self.fields['ins_temp_max'].queryset = (
            DistrictForecastInstructions.objects.filter(
                Q(category__category_name="Temperature") |
                Q(category__category_name="Uncategorized")
            ).order_by(Lower('description'))
        )

        self.fields['ins_temp_min'].queryset = (
            DistrictForecastInstructions.objects.filter(
                Q(category__category_name="Temperature") |
                Q(category__category_name="Uncategorized")
            ).order_by(Lower('description'))
        )        

        self.fields['ins_winds'].queryset = (
            DistrictForecastInstructions.objects.filter(
                Q(category__category_name="Winds") |
                Q(category__category_name="Uncategorized")
            ).order_by(Lower('description'))
        )

        self.fields['ins_precip_max'].queryset = (
            DistrictForecastInstructions.objects.filter(
                Q(category__category_name="Precipitation") |
                Q(category__category_name="Uncategorized")
            ).order_by(Lower('description'))
        )

class ForecastGeneralForm(forms.ModelForm):

    class Meta:
        model = ForecastGeneral
        exclude = (
            "created_by",
            "created_time",
            "updated_by",
            "updated_time",
            "auto_update",
        )

        widgets = {
            "forecast_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "forecast_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),

            "forecast_type": forms.Select(attrs={"class": "form-select"}),

            "general_situation": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),

            "thr_forecast": forms.Textarea(
                attrs={"rows": 4, "class": "form-control"}
            ),

            "sea_state": forms.Textarea(
                attrs={"rows": 2, "class": "form-control"}
            ),

            "sea_state_shift": forms.Textarea(
                attrs={"rows": 2, "class": "form-control"}
            ),

            "advisory": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),

            "outlook": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),

            "wind_speed": forms.TextInput(attrs={"class": "form-control"}),
            "wind_direction": forms.TextInput(attrs={"class": "form-control"}),
            "wind_condition": forms.TextInput(attrs={"class": "form-control"}),

            "wind_shift_speed": forms.TextInput(attrs={"class": "form-control"}),
            "wind_shift_direction": forms.TextInput(attrs={"class": "form-control"}),
            "wind_shift_condition": forms.TextInput(attrs={"class": "form-control"}),

            "wave": forms.TextInput(attrs={"class": "form-control"}),
            "wave_shift": forms.TextInput(attrs={"class": "form-control"}),

            "coast_high_f": forms.NumberInput(attrs={"class": "form-control"}),
            "coast_high_c": forms.NumberInput(attrs={"class": "form-control"}),

            "coast_low_f": forms.NumberInput(attrs={"class": "form-control"}),
            "coast_low_c": forms.NumberInput(attrs={"class": "form-control"}),

            "inland_high_f": forms.NumberInput(attrs={"class": "form-control"}),
            "inland_high_c": forms.NumberInput(attrs={"class": "form-control"}),

            "inland_low_f": forms.NumberInput(attrs={"class": "form-control"}),
            "inland_low_c": forms.NumberInput(attrs={"class": "form-control"}),

            "hills_high_f": forms.NumberInput(attrs={"class": "form-control"}),
            "hills_high_c": forms.NumberInput(attrs={"class": "form-control"}),

            "hills_low_f": forms.NumberInput(attrs={"class": "form-control"}),
            "hills_low_c": forms.NumberInput(attrs={"class": "form-control"}),

            "publish_to_web": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),

            "light_variable": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),

            "forecaster_id": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-control")