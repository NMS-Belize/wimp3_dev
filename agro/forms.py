from django import forms
from .models import Sector, Commodity, DroughtAlertLevel, PestRiskEntryDetails,  PestAlertLevel, PestRiskEffect, PestRiskAction, PestRisk, PestRiskInfo

from system_core.models import Months, AlertLevel

from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from django.core.exceptions import ValidationError
from django_select2.forms import Select2Widget

class PestRiskForm(forms.ModelForm):

    months = forms.ModelMultipleChoiceField(
        queryset = Months.objects.all().order_by('id'),
        widget = forms.CheckboxSelectMultiple(attrs={'class': 'btn-check','id': 'mnth'}),
        required = True,
        label = 'Months'
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['months'].label_from_instance = (
            lambda obj: obj.short_name
        )

    class Meta:
        model = PestRisk
        fields = ['months', 'year']
        labels = {   
            'months':       'Months',
            'year':         'Year:'
        }
        widgets = {
            'year':     forms.TextInput(attrs={'class': 'form-control','style':'width:120px !important;'}),
        }
        required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only set initial values when loading the form,
        # not when processing submitted POST data.
        if (not self.is_bound and self.instance and self.instance.pk and self.instance.months):
            month_ids = [
                int(month_id)
                for month_id in self.instance.months
            ]

            self.fields['months'].initial = month_ids

    def clean_months(self):
        selected_months = self.cleaned_data['months']

        # Convert the Months queryset into a JSON-compatible list.
        return list(
            selected_months.values_list('id', flat=True)
        )

    def save(self, commit=True):
        instance = super().save(commit=False)

        # clean_months() already converted this to a list of IDs.
        instance.months = self.cleaned_data['months']

        if commit:
            instance.save()

        return instance

class PestRiskEntryDetailsForm(forms.ModelForm):

    commodity_name = forms.CharField(
        label="Commodity",
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={ "class": "form-control bg-secondary-subtle" }),
    )

    district_name = forms.CharField(
        label="District",
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={ "class": "form-control bg-secondary-subtle" }),
    )

    class Meta:
        model = PestRiskEntryDetails
        fields = ['district_id', 'commodity_id', 'pest_alert_lvl_id','drought_alert_lvl_id','temp_max','temp_min','precip_min','precip_max','effect','info','actions']
        labels = {   
            'pest_alert_lvl_id': 'Pest Alert Level:',
            'drought_alert_lvl_id': 'Drought Level Alert:',
            'temp_min': 'Minimum:',
            'temp_max': 'Maximum:',
            'precip_min': 'Minimum:',
            'precip_max': 'Maximum:',
            'effect': 'Possible Effect:',
            'info': 'Additional Info for Possible Effect:',
            'actions': 'Actions:'
        }
        widgets = {
            "commodity_id":     forms.HiddenInput(),
            "district_id":      forms.HiddenInput(),
            'pest_alert_lvl_id': forms.RadioSelect(attrs={'class': 'btn-check'}),
            'drought_alert_lvl_id': forms.RadioSelect(attrs={'class': 'btn-check'}),
            'temp_min':         forms.TextInput(attrs={'class': 'form-control'}),
            'temp_max':         forms.TextInput(attrs={'class': 'form-control'}),
            'precip_min':       forms.TextInput(attrs={'class': 'form-control'}),
            'precip_max':       forms.TextInput(attrs={'class': 'form-control'}),
            'effect':           forms.SelectMultiple(attrs={'class': 'form-select select2'}),
            'info':             forms.SelectMultiple(attrs={'class': 'form-select select2'}),
            'actions':          forms.SelectMultiple(attrs={'class': 'form-select select2'}),
        }

    def __init__(self, *args, **kwargs):

        commodity   = kwargs.pop("commodity", None)
        district    = kwargs.pop("district", None)

        super().__init__(*args,**kwargs)

        self.fields["commodity_id"].required = False
        self.fields["district_id"].required = False

        # Set display fields
        if commodity is not None:
            self.fields["commodity_id"].initial = commodity
            self.fields["commodity_name"].initial = str(commodity)

        if district is not None:
            self.fields["district_id"].initial = district
            self.fields["district_name"].initial = str(district)

        # Updating an existing record
        if self.instance and self.instance.pk:
            if self.instance.commodity_id:
                commodity = self.instance.commodity_id
                self.fields["commodity_name"].initial = str(self.instance.commodity_id)

            if self.instance.district_id:
                district = self.instance.district_id
                self.fields["district_name"].initial = str(self.instance.district_id)

        self.fields['pest_alert_lvl_id'].queryset = AlertLevel.objects.all().order_by("id")
        self.fields['pest_alert_lvl_id'].label_from_instance = lambda obj: obj.description

        self.fields['drought_alert_lvl_id'].queryset = DroughtAlertLevel.objects.all().order_by("id")
        self.fields['drought_alert_lvl_id'].label_from_instance = lambda obj: obj.description

        # Default empty
        self.fields['effect'].queryset = PestRiskEffect.objects.none()
        self.fields['info'].queryset = PestRiskInfo.objects.none()
        self.fields['actions'].queryset = PestRiskAction.objects.none()

        if commodity is not None:
            self.fields['effect'].queryset = (PestRiskEffect.objects.filter(commodity=commodity).order_by('effect_description'))
            self.fields['info'].queryset = (PestRiskInfo.objects.filter(commodity=commodity).order_by('info_description'))
            self.fields['actions'].queryset = (PestRiskAction.objects.filter(commodity=commodity).order_by('action_description'))

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['description']
        labels = {   
            # <-- add human-friendly labels here
            'description': 'Description:',
        }
        widgets = {            
            'description': forms.TextInput(attrs={'class': 'form-control select2'}),
        }

class DroughtAlertLevelForm(forms.ModelForm):
    class Meta:
        model = DroughtAlertLevel
        fields = ['description', 'color_hex']
        labels = {   
            # <-- add human-friendly labels here
            'description': 'Description:',
            'action_level': 'Action Level:',
            'color_hex': 'Color HEX',
        }
        widgets = {            
            'description':  forms.TextInput(attrs={'class': 'form-control'}),
            'action_level': forms.TextInput(attrs={'class': 'form-control'}),
            'color_hex':    forms.ColorInput(attrs={'class': 'form-control form-control-color'})
        }

class CommodityTypeForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = ['description','sector']
        labels = {   
            # <-- add human-friendly labels here
            'description': 'Description:',
            'sector': 'Sector:'
        }
        widgets = {            
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'sector': forms.Select(attrs={'class': 'form-select'})
        }

class ActionItemsForm(forms.ModelForm):
    class Meta:
        model = PestRiskAction
        fields = ['commodity','action_description']
        labels = {   
            # <-- add human-friendly labels here
            'commodity': 'Commodity:',
            'action_description': 'Description:',
        }
        widgets = { 
            'commodity': forms.Select(attrs={'class': 'form-select color-select'}),
            'action_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class InfoItemsForm(forms.ModelForm):
    class Meta:
        model = PestRiskInfo
        fields = ['commodity','info_description']
        labels = {   
            # <-- add human-friendly labels here
            'commodity': 'Commodity:',
            'info_description': 'Description:'
        }
        widgets = { 
            'commodity': forms.Select(attrs={'class': 'form-select color-select'}),           
            'info_description': forms.Textarea(attrs={'class': 'form-control'})
        }

class EffectItemsForm(forms.ModelForm):
    class Meta:
        model = PestRiskEffect
        fields = ['commodity','effect_description']
        labels = {   
            # <-- add human-friendly labels here
            'commodity': 'Commodity:',
            'effect_description': 'Description:'
        }
        widgets = {            
            'commodity': forms.Select(attrs={'class': 'form-select color-select'}),
            'effect_description': forms.Textarea(attrs={'class': 'form-control'})
        }