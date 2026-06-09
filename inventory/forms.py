from django import forms
from .models import DepartmentSection, HardwareSpecifications, InventoryCategory, Manufacturer,InventoryItem, DeviceType, NetworkDetails, Vendor

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

class DeviceTypeForm(forms.ModelForm):
    class Meta:
        model = DeviceType
        fields = ['name', 'inventory_category']
        labels = {   
            # <-- add human-friendly labels here
            'name': 'Device Type Name:',
            'inventory_category': 'Inventory Category:',
        }
        widgets = {            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'inventory_category': forms.Select(attrs={'class': 'form-select'}),
        }

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'short_name']
        labels = {   
            # <-- add human-friendly labels here
            'name': 'Vendor Name:',
            'short_name': 'Short Name:',
        }
        widgets = {            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
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
            'device_status',
            'serial_number',
            #'service_tag',
            'acquisition_date',
            'date_issued',
            'vendor',
            'notes',
        ]
        widgets = {
            'device_label': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Device Label'}),
            'device_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Device Name'}),
            'device_type': forms.Select(attrs={'class': 'form-control'}),
            'assigned_user': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Assigned User'}),
            'placement': forms.Select(attrs={'class': 'form-select'}),
            'department_section': forms.Select(attrs={'class': 'form-select'}),
            'floor_level': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'manufacturer': forms.Select(attrs={'class': 'form-select'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
            'device_status': forms.Select(attrs={'class': 'form-select'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            #'service_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'acquisition_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'date_issued': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'vendor': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class NetworkDetailsForm(forms.ModelForm):
    class Meta:
        model = NetworkDetails
        fields = [
            'inventory_item',
            'mac_address',
            'ip_address',
            'cabinet',
            'switch_port_number',
        ]
        widgets = {
            'inventory_item': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Inventory Item'}),
            'mac_address': forms.TextInput(attrs={'class': 'form-control','placeholder': 'MAC Address'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control','placeholder': 'IP Address'}),
            'cabinet': forms.Select(attrs={'class': 'form-select'}),
            'switch_port_number': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Switch Port Number'}),
        }
    
class HardwareSpecificationsForm(forms.ModelForm):
    class Meta:
        model = HardwareSpecifications
        fields = [
            'inventory_item',
            'service_tag',
            'express_service_code',
            'processor',
            'ram',
            'operating_system',
            'disk_size'
        ]
        widgets = {
            'inventory_item': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Inventory Item'}),
            'service_tag': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Service Tag'}),
            'express_service_code': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Express Service Code'}),
            'processor': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Processor'}),
            'ram': forms.TextInput(attrs={'class': 'form-control','placeholder': 'RAM'}),
            'operating_system': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Operating System'}),
            'disk_size': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Disk'}),
        }
        