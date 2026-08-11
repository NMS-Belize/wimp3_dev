from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory

from .models import InventoryItem, InventoryCategory, InventoryItemPhoto, Manufacturer, DeviceType, NetworkDetails, Vendor, HardwareSpecifications
from users.models import Employee

User = get_user_model()

class InventoryCategoryForm(forms.ModelForm):
    class Meta:
        model = InventoryCategory
        fields = ['name','description']
        labels = {   
            # <-- add human-friendly labels here
            'name':         'Category Name:',
            'description':  'Description:',
        }
        widgets = {            
            'name':         forms.TextInput(attrs={'class': 'form-control'}),
            'description':  forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
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

class InventoryItemPhotoForm(forms.ModelForm):
    class Meta:
        model = InventoryItemPhoto
        fields = ["photo","caption","is_primary"]

        widgets = {
            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "caption": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Photo description",
                }
            ),
            "is_primary": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

InventoryItemPhotoFormSet = inlineformset_factory(
    InventoryItem,
    InventoryItemPhoto,
    form=InventoryItemPhotoForm,
    fields=[
        "photo",
        "caption",
        "is_primary",
    ],
    extra=1,
    max_num=10,
    validate_max=True,
    can_delete=True,
)

class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        #if obj.first_name or obj.last_name:
        return f"{obj.first_name} {obj.last_name}".strip()
        #return obj.username
    
class InventoryItemForm(forms.ModelForm):

    assigned_user = UserChoiceField(
        queryset    = Employee.objects.order_by('first_name', 'last_name'),
        required    = False,
        widget      = forms.Select(attrs={'class': 'form-select'}),
    )

    placement_floor = forms.CharField(
        label = "Floor", required = False, disabled = True,
        widget=forms.TextInput(attrs={ "class": "form-control", "placeholder": "Select a placement to view its floor" }),
    )

    class Meta:
        model = InventoryItem
        fields = [
            'device_label',
            'device_name',
            'device_type',
            'assigned_user',
            'placement',
            'department_section',
            'category',
            'manufacturer',
            'model_number',
            'device_status',
            'serial_number',
            'acquisition_date',
            'date_issued',
            'vendor',
            'notes',
        ]
        widgets = {
            'device_label':     forms.TextInput(attrs={'class': 'form-control','placeholder': 'Device Label'}),
            'device_name':      forms.TextInput(attrs={'class': 'form-control','placeholder': 'Device Name'}),
            'device_type':      forms.Select(attrs={'class': 'form-control'}),
            'assigned_user':    forms.Select(attrs={'class': 'form-select'}),
            'placement':        forms.Select(attrs={'class': 'form-select'}),
            'department_section': forms.Select(attrs={'class': 'form-select'}),
            'category':         forms.Select(attrs={'class': 'form-select'}),
            'manufacturer':     forms.Select(attrs={'class': 'form-select'}),
            'model_number':     forms.TextInput(attrs={'class': 'form-control'}),
            'device_status':    forms.Select(attrs={'class': 'form-select'}),
            'serial_number':       forms.TextInput(attrs={'class': 'form-control'}),
            'acquisition_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'date_issued':      forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'vendor':           forms.Select(attrs={'class': 'form-control'}),
            'notes':            forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Display the existing floor when editing an inventory item.
        if self.instance.pk and self.instance.placement:
            self.fields["placement_floor"].initial = (
                self.instance.placement.floor
            )

class NetworkDetailsForm(forms.ModelForm):
    class Meta:
        model = NetworkDetails
        fields = [
            'inventory_item',
            'mac_address',
            'mac_address_wireless',
            'ip_address',
            'cabinet',
            'switch_port_number',
            'rack_number',
        ]
        widgets = {
            'inventory_item':   forms.TextInput(attrs={'class': 'form-control','placeholder': 'Inventory Item'}),
            'mac_address':      forms.TextInput(attrs={'class': 'form-control','placeholder': 'MAC Address (LAN)'}),
            'mac_address_wireless': forms.TextInput(attrs={'class': 'form-control','placeholder': 'MAC Address (Wireless)'}),
            'ip_address':       forms.TextInput(attrs={'class': 'form-control','placeholder': 'IP Address'}),
            'cabinet':          forms.Select(attrs={'class': 'form-select'}),
            'switch_port_number': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Switch Port Number'}),
            'rack_number':      forms.TextInput(attrs={'class': 'form-control','placeholder': 'Rack'}),
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
        