from django import forms
from .models import InventoryCategory, InventoryItem

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
        
'''class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = [
            'name',
            'asset_tag',
            'serial_number',
            'category',
            'placement',
            'brand',
            'model',
            'description',
            'quantity',
            'acquisition_date',
            'status',
            'is_active',
            'sponsor'
        ]
        widgets = {
            'acquisition_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'asset_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'placement': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }'''