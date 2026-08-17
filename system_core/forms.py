from django import forms

from .models import DepartmentSection, JobTitle, District, Months, OfficeLocation, RiskLevel, AlertLevel, Zone

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

class ZoneAreaForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['zone_name']
        labels = {   
            # <-- add human-friendly labels here
            'zone_name': 'Zone Name:',
        }
        widgets = {            
            'zone_name': forms.TextInput(attrs={'class': 'form-control'}),
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
            'description':  forms.TextInput(attrs={'class': 'form-control'}),
            'color':        forms.ColorInput(attrs={'class': 'form-control form-control-color'})
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
            'description':  forms.TextInput(attrs={'class': 'form-control'}),
            'color':        forms.ColorInput(attrs={'class': 'form-control form-control-color'})
        }

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