from django import forms
from .models import Months, Zone, CommodityCategory, CommodityType, DroughtAlertLevel, District, PestRiskEntryMainListing, PestRiskEntryDetails,  PestAlertLevel, PestRiskEffect, PestRiskAction

from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from django.core.exceptions import ValidationError

MONTH_CHOICES   = [(1,'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),(6,'June'),(7,'July'),(8,'August'),(9,'September'),(10,'October'),(11,'November'),(12,'December')]
YEAR_CHOICES    = [('2026', '2026'),('2027', '2027')]

class PestRiskMainListingForm(forms.ModelForm):

    # Replace the default field with MultipleChoiceField
    months = forms.MultipleChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': ''}),
        label="Months"
    )

    class Meta:
        model = PestRiskEntryMainListing
        fields = ['months', 'year', 'commodity']
        labels = {   
            'months':       'Months',
            'year':         'Year:',
            'commodity':    'Commodity'
        }
        widgets = {
            'months':       forms.CheckboxSelectMultiple(choices=MONTH_CHOICES,attrs={'class': ''}),
            'year':         forms.Select(choices=YEAR_CHOICES,attrs={'class': 'form-control'}),
            'commodity':    forms.Select(attrs={'class': 'form-control'})
        }
        required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate months from instance JSONField
        if self.instance and self.instance.months:
            self.initial['months'] = self.instance.months

    def save(self, commit=True):
        instance = super().save(commit=False)

        if isinstance(instance.months, list):
            instance.months = sorted(instance.months)
        if commit:
            instance.save()
        return instance

    def clean_months(self):
        
        months = self.cleaned_data.get('months', [])

        # Convert string selections back to integers
        month_numbers = sorted([int(m) for m in months])

        if len(month_numbers) != 3:
            raise ValidationError("You must select exactly 3 months.")

        # Check for consecutive months
        if not (month_numbers[1] == month_numbers[0] + 1 and
                month_numbers[2] == month_numbers[1] + 1):
            raise ValidationError("The 3 months must be consecutive.")

        return month_numbers  # store as integers

    def clean(self):
        cleaned_data = super().clean()
        months = cleaned_data.get("months")
        year = cleaned_data.get("year")
        commodity = cleaned_data.get("commodity")

        if months and year and commodity:
            months_sorted = sorted(months)

            queryset = PestRiskEntryMainListing.objects.filter(
                year=year,
                commodity=commodity
            )

            # Exclude current instance when editing
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)

            for entry in queryset:
                if sorted(entry.months) == months_sorted:
                    raise ValidationError(
                        "This combination of Months, Year and Commodity already exists."
                    )

        return cleaned_data

    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if the form is bound to an instance
        if self.instance and self.instance.pk:
            # For ManyToManyField or MultiSelectField storing month values
            # Convert them to a list of strings to match MONTH_CHOICES values
            self.fields['months'].initial = [
                str(month) for month in getattr(self.instance, 'months', [])
            ]'''

class PestRiskEntryDetailsForm(forms.ModelForm):
    class Meta:
        model = PestRiskEntryDetails
        fields = ['pest_risk_listing_id','district_id', 'pest_alert_lvl_id','drought_alert_lvl_id','temp_max','temp_min','precip_min','precip_max','effect','info','actions']
        labels = {   
            'pest_risk_listing_id': 'PR ID',
            'district_id': 'Select District / Zone',
            'pest_alert_lvl_id': 'Pest Alert Level:',
            'drought_alert_lvl_id': 'Drought Level Alert:',
            'temp_min': 'TEMP MIN (°F):',
            'temp_max': 'TEMP MAX (°F):',
            'precip_min': 'PRECIP MIN (mm):',
            'precip_max': 'PRECIP MAX (mm):',
            'effect': 'Possible Effect:',
            'info': 'Additional Info for Possible Effect:',
            'actions': 'Actions:'
        }
        widgets = {
            'pest_risk_listing_id': forms.HiddenInput(),
            'district_id':  forms.Select(attrs={'class': 'form-control'}),
            'pest_alert_lvl_id': forms.Select(attrs={'class': 'form-control'}),
            'drought_alert_lvl_id': forms.Select(attrs={'class': 'form-control'}),
            'temp_min': forms.TextInput(attrs={'class': 'form-control'}),
            'temp_max': forms.TextInput(attrs={'class': 'form-control'}),
            'precip_min': forms.TextInput(attrs={'class': 'form-control'}),
            'precip_max': forms.TextInput(attrs={'class': 'form-control'}),
            'effect': forms.Select(attrs={'class': 'form-control'}),
            'info': forms.Textarea(attrs={'class': 'form-control'}),
            'actions': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):

        pest_risk_listing_id = kwargs.pop('pest_risk_listing_id',None)
        super().__init__(*args,**kwargs)
        
        # set hidden pest_risk_listing_id if provided
        #if pest_risk_listing_id is not None:
        self.fields['pest_risk_listing_id'].initial = pest_risk_listing_id

        # ensure dropdown is populated from PestAlertLevel model
        self.fields['district_id'].queryset = District.objects.all().order_by("id")
        self.fields['district_id'].empty_label = "Select District / Zone"
        
        self.fields['pest_alert_lvl_id'].queryset = PestAlertLevel.objects.all().order_by("id")
        self.fields['pest_alert_lvl_id'].empty_label = "Select Pest Alert Level"
        self.fields['pest_alert_lvl_id'].label_from_instance = lambda obj: obj.description

        self.fields['drought_alert_lvl_id'].queryset = DroughtAlertLevel.objects.all().order_by("id")
        self.fields['drought_alert_lvl_id'].empty_label = "Select Drought Alert Level"
        self.fields['drought_alert_lvl_id'].label_from_instance = lambda obj: obj.title

        self.fields['effect'].queryset = PestRiskEffect.objects.all().order_by("id")
        self.fields['effect'].empty_label = "Possible Effects"

        self.fields['actions'].queryset = PestRiskAction.objects.all().order_by("id")
        self.fields['actions'].empty_label = "Select Actions"

class SectorForm(forms.ModelForm):
    class Meta:
        model = CommodityCategory
        fields = ['description']
        labels = {   
            # <-- add human-friendly labels here
            'description': 'Description:',
        }
        widgets = {            
            'description': forms.TextInput(attrs={'class': 'form-control'}),
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

class DistrictZoneForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['district_area', 'zone_id']
        labels = {   
            # <-- add human-friendly labels here
            'district_area': 'District:',
            'zone_id': 'Zone/Area',
        }
        widgets = {            
            'district_area': forms.TextInput(attrs={'class': 'form-control'}),
            'zone_id': forms.Select(attrs={'class': 'form-control'})
        }

class PestAlertLevelForm(forms.ModelForm):
    class Meta:
        model = PestAlertLevel
        fields = ['description', 'color_hex']
        labels = {   
            # <-- add human-friendly labels here
            'description': 'Description:',
            'color_hex': 'Color HEX',
        }
        widgets = {            
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'color_hex': forms.TextInput(attrs={'class': 'form-control'})
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
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'action_level': forms.TextInput(attrs={'class': 'form-control'}),
            'color_hex': forms.TextInput(attrs={'class': 'form-control'})
        }

class CommodityTypeForm(forms.ModelForm):
    class Meta:
        model = CommodityType
        fields = ['description','commodity_category']
        labels = {   
            # <-- add human-friendly labels here
            'description': 'Description:',
            'commodity_category': 'Commodity Category:'
        }
        widgets = {            
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'commodity_category': forms.Select(attrs={'class': 'form-control'})
        }

class ActionItemsForm(forms.ModelForm):
    class Meta:
        model = PestRiskAction
        fields = ['action_description']
        labels = {   
            # <-- add human-friendly labels here
            'action_description': 'Description:',
        }
        widgets = {            
            'action_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class EffectItemsForm(forms.ModelForm):
    class Meta:
        model = PestRiskEffect
        fields = ['effect_description']
        labels = {   
            # <-- add human-friendly labels here
            'effect_description': 'Description:',
        }
        widgets = {            
            'effect_description': forms.Textarea(attrs={'class': 'form-control'}),
        }