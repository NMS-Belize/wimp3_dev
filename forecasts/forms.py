from datetime import timezone

from click import option
from django import forms
from pytz import timezone
from .models import AlertLevel, District, DistrictForecast, DistrictForecastDetails, DistrictForecastInstructions, Probability, RiskLevel, Severity

from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from django.core.exceptions import ValidationError

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
            severity    = Severity.objects.filter(pk=severity_id).first()

            if severity and severity.color:
                option["attrs"]["style"] = (
                    f"background-color: {severity.color} !important; --bs-form-select-bg-img: none;"
                )

        return option

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['district_name']
        labels = {   
            # <-- add human-friendly labels here
            'district_name': 'District Name:'
        }
        widgets = {            
            'district_name': forms.TextInput(attrs={'class': 'form-control'})
        }

class AlertLevelForm(forms.ModelForm):
    class Meta:
        model = AlertLevel
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

class DistrictForecastInstructionsForm(forms.ModelForm):
    class Meta:
        model = DistrictForecastInstructions
        fields = ['description']
        labels = {   
            # <-- add human-friendly labels here
            'description': 'Description:'
        }
        widgets = {            
            'description': forms.TextInput(attrs={'class': 'form-control'})
        }

class RiskLevelForm(forms.ModelForm):
    class Meta:
        model = RiskLevel
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
                  'temp_max', 'prob_temp_max', 'sev_temp_max', 'ins_temp_max',
                  'temp_min', 'prob_temp_min', 'sev_temp_min', 'ins_temp_min',
                  'winds_min', 'winds_max', 'prob_winds', 'sev_winds', 'ins_winds',
                  'precip_max', 'prob_precip_max', 'sev_precip_max', 'ins_precip_max',
                  'weather_conditions', 'prob_weather_conditions', 'sev_weather_conditions', 'ins_weather_conditions'
        ]
        labels = {   
            # <-- add human-friendly labels here
            #'district': 'District:',
            #'temp_max': 'TEMP MAX (°F):',
            #'prob_temp_max': 'PROBABILITY - TEMP MAX:',
            #'sev_temp_max': 'SEVERITY - TEMP MAX:',
            #'temp_min': 'TEMP MIN (°F):',
            #'prob_temp_min': 'PROBABILITY - TEMP MIN:',
            #'sev_temp_min': 'SEVERITY - TEMP MIN:',
            #'winds': 'WINDS (kts):',
            #'prob_winds': 'PROBABILITY - WINDS:',
            #'sev_winds': 'SEVERITY - WINDS:',
            #'precip_max': 'PRECIPITATION (MAX 24H, in):',
            #'prob_precip_max': 'PROBABILITY - PRECIPITATION:',
            #'sev_precip_max': 'SEVERITY - PRECIPITATION:',
            #'weather_conditions': 'WEATHER CONDITIONS:',
            #'prob_weather_conditions': 'PROBABILITY - WEATHER CONDITIONS:',
            #'sev_weather_conditions': 'SEVERITY - WEATHER CONDITIONS:'
        }
        widgets = {            
            #'district': forms.TextInput(attrs={'class': 'form-select', 'disabled': 'disabled'}),

            'temp_max': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.5', 'width': '100%'}),
            'prob_temp_max': forms.Select(attrs={'class': 'form-select','width': '100%'}),
            'sev_temp_max': ColorSelect(attrs={'class': 'form-select', 'width': '100%'}),
            'ins_temp_max': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),

            'temp_min': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.5', 'width': '100%'}),
            'prob_temp_min': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),
            'sev_temp_min': ColorSelect(attrs={'class': 'form-select', 'width': '100%'}),
            'ins_temp_min': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),

            'winds_min': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.5', 'width': '45%'}),
            'winds_max': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.5', 'width': '45%'}),
            'prob_winds': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),
            'sev_winds': ColorSelect(attrs={'class': 'form-select', 'width': '100%'}),
            'ins_winds': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),

            'precip_max': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.5', 'width': '100%'}),
            'prob_precip_max': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),
            'sev_precip_max': ColorSelect(attrs={'class': 'form-select', 'width': '100%'}),
            'ins_precip_max': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),

            'weather_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 20, 'style': 'width: 100%'}),
            'prob_weather_conditions': forms.Select(attrs={'class': 'form-select', 'width': '100%'}),
            'sev_weather_conditions': ColorSelect(attrs={'class': 'form-select', 'width': '100%'}),
            'ins_weather_conditions': forms.Select(attrs={'class': 'form-select', 'width': '100%'})
        }

    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['probability'].queryset = Probability.objects.all().order_by("id")
        self.fields['probability'].empty_label = "Select Probability Level"
        self.fields['probability'].label_from_instance = lambda obj: obj.description

        self.fields['severity'].queryset = Severity.objects.all().order_by("id")
        self.fields['severity'].empty_label = "Select Severity Level"
        self.fields["severity"].label_from_instance = (
            lambda obj: f"⬛ {obj.description}"
        )

        self.fields['risk_level'].queryset = RiskLevel.objects.all().order_by("id")
        self.fields['risk_level'].empty_label = "Select Risk Level"
        self.fields['risk_level'].label_from_instance = lambda obj: obj.description'''

