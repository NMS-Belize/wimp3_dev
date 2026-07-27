from django import forms

from .models import DepartmentSection, JobTitle, District, Months, OfficeLocation, RiskLevel, AlertLevel

class JobTitleForm(forms.ModelForm):
    class Meta:
        model = JobTitle
        fields = ['description']
        labels = {   
            # <-- add human-friendly labels here
            'description': 'Description:'
        }
        widgets = {            
            'description': forms.TextInput(attrs={'class': 'form-control'})

        }

class DepartmentSectionForm(forms.ModelForm):
    class Meta:
        model = DepartmentSection
        fields = ['name', 'short_name']
        labels = {   
            # <-- add human-friendly labels here
            'name': 'Department/Section Name:',
            'short_name': 'Short Name:',
        }
        widgets = {            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OfficeLocationForm(forms.ModelForm):
    class Meta:
        model = OfficeLocation
        fields = ['name', 'floor', 'description']
        labels = {   
            # <-- add human-friendly labels here
            'name': 'Office Location Name:',
            'floor': 'Floor:',
            'description': 'Description:',
        }
        widgets = {            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'floor': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }