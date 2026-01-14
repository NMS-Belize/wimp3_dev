from django import forms
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

from .models import RadarImages

class RadarImageForm(forms.ModelForm):
    class Meta:
        model = RadarImages
        fields = ['image_title', 'image_url', 'web_directory', 'is_published']
        labels = {   
            # <-- add human-friendly labels here
            'image_title': 'Image Title',
            'image_url': 'Image URL',
            'web_directory': 'Web Directory /images/radar/',
            'is_published': 'Published Status',
        }
        widgets = {
            'image_title': forms.TextInput(attrs={'class': 'form-control'}),
            'image_url': forms.TextInput(attrs={'class': 'form-control'}),
            'web_directory': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'is_published': DjangoToggleSwitchWidget(attrs={'class': 'form-check-input'}),
        }