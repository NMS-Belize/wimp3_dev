from django import forms
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

from .models import RadarImages

class RadarImageForm(forms.ModelForm):
    class Meta:
        model = RadarImages
        fields = ['image_title', 'image_url', 'web_directory', 'is_published','display_order']
        labels = {   
            # <-- add human-friendly labels here
            'image_title': 'Image Title:',
            'image_url': 'Remote Image URL:',
            'web_directory': 'Web Directory:',
            'is_published': 'Published Status:',
            'display_order': 'Display Order:'
        }
        widgets = {
            'image_title':  forms.TextInput(attrs={'class': 'form-control'}),
            'image_url':    forms.TextInput(attrs={'class': 'form-control'}),
            'web_directory': forms.TextInput(attrs={'class': 'form-control'}),
            'is_published': DjangoToggleSwitchWidget(attrs={'class': 'form-check-input'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }