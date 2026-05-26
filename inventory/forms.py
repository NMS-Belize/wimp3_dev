from django import forms
from .models import DepartmentSection, InventoryCategory, Manufacturer,InventoryItem

class InventoryCategoryForm(forms.ModelForm):
    class Meta:
        model = InventoryCategory
        fields = ['name']
        labels = {   
            # <-- add human-friendly labels here
            'name': 'Category Name:',
        }
        widgets = {            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
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
        
class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name']
        labels = {   
            # <-- add human-friendly labels here
            'name': 'Manufacturer Name:',
        }
        widgets = {     
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = [
            'device_label',
            'device_name',
            'device_type',
            'assigned_user',
            'placement',
            'department_section',
            'floor_level',
            'category',
            'manufacturer',
            'model_number',
            'service_tag',
            'processor',
            'ram',
            'operating_system',
            'disk',
            'device_status',
            'serial_number',
            'mac_address',
            'ip_address',
            'acquisition_date',
            'date_issued',
            'sponsor',
        ]
        widgets = {
            'device_label': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Device Label'}),
            'device_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Device Name'}),
            'device_type': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Device Type'}),
            'assigned_user': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Assigned User'}),
            'placement': forms.Select(attrs={'class': 'form-select'}),
            'department_section': forms.Select(attrs={'class': 'form-select'}),
            'floor_level': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'manufacturer': forms.Select(attrs={'class': 'form-select'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
            'service_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'processor': forms.TextInput(attrs={'class': 'form-control' }),
            'ram': forms.TextInput(attrs={'class': 'form-control'}),
            'operating_system': forms.TextInput(attrs={'class': 'form-control'}),
            'disk': forms.TextInput(attrs={'class': 'form-control'}),
            'device_status': forms.Select(attrs={'class': 'form-select'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'mac_address': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'acquisition_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'date_issued': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'sponsor': forms.TextInput(attrs={'class': 'form-control'}),
        }