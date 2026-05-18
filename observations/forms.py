from django import forms
from .models import WeatherIcons

class WeatherIconsForm(forms.ModelForm):
    class Meta:
        model = WeatherIcons
        fields = ['name', 'icon_file']
        labels = {   
            # <-- add human-friendly labels here
            'name': 'Icon Name:',
            'icon_file': 'Icon File:',
        }
        widgets = {            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'icon_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        