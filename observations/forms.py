from pathlib import Path

from django import forms
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html

from .models import WeatherIcons, WeatherCodes

class WeatherIconsForm(forms.ModelForm):
    class Meta:
        model = WeatherIcons
        fields = ['name', 'icon_file']
        labels = {   
            'name': 'Icon Name:',
            'icon_file': 'Icon File:',
        }
        widgets = {            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'icon_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class WeatherCodeForm(forms.ModelForm):

    day_icon_choice = forms.ModelChoiceField(queryset=WeatherIcons.objects.all(),label="Day Icon",required=False, empty_label="No icon",widget=forms.RadioSelect)
    night_icon_choice = forms.ModelChoiceField(queryset=WeatherIcons.objects.all(),label="Night Icon",required=False, empty_label="No icon",widget=forms.RadioSelect)

    class Meta:
        model = WeatherCodes
        fields = ['code', 'description']
        widgets = {            
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
        #icon_path = f'weather_icons/{icon.icon_file.name}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        icons = WeatherIcons.objects.all().order_by("name")

        for field_name, model_field in [("day_icon_choice", "icon_day"),("night_icon_choice", "icon_night")]:
            field = self.fields[field_name]
            field.queryset = icons

            # Preselect existing icon when editing
            if self.instance and self.instance.pk:
                self.initial[field_name] = getattr(self.instance,f"{model_field}_id")

            # Render image labels
            field.label_from_instance = self.icon_label

    @staticmethod
    def icon_label(icon):

        filename = Path(icon.icon_file.name).name
        icon_url = static(f"weather_icons/{filename}")

        return format_html('<img src="{}" alt="{}" style="width:65px;height:65px;object-fit:contain;" /><small>{}</small>', icon_url,icon.name,icon.name)

    def save(self, commit=True):

        instance = super().save(commit=False)

        # ModelChoiceField returns WeatherIcons instances
        instance.icon_day = self.cleaned_data.get("day_icon_choice")
        instance.icon_night = self.cleaned_data.get("night_icon_choice")

        if commit:
            instance.save()
            self.save_m2m()

        return instance

        