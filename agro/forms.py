from django import forms
from .models import Months, CommodityType, DroughtAlertLevel, District, PestRiskEntryMainListing, PestRiskEntryDetails,  PestAlertLevel, PestRiskEffect, PestRiskAction

MONTH_CHOICES = [
    ('1','JAN'),
    ('2', 'FEB'),
    ('3','MAR'),
    ('4','APR'),
    ('5','MAY'),
    ('6','JUN'),
    ('7','JUL'),
    ('8','AUG'),
    ('9','SEP'),
    ('10','OCT'),
    ('11','NOV'),
    ('12','DEC')
]

'''class FormPestRiskStartForm(forms.Form):
    months = forms.MultipleChoiceField(
        choices = MONTH_CHOICES,
        widget = forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input'}
        ),
        required = True
    )
    commodity = forms.ModelChoiceField(
        queryset = CommodityType.objects.all(),
        empty_label = "Select a Commodity",
        required = True,
        widget = forms.Select(attrs = {'class': 'form-control' })
    )
    year = forms.CharField(
        label = "Year",
        required = True,
        max_length = 4,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Year'})
    )

    def clean_months(self):
        months = self.cleaned_data.get("months", [])
        if len(months) > 3:
            raise forms.ValidationError("You can only select up to 3 months.")
        return months'''

class PestRiskMainListingForm(forms.ModelForm):
    class Meta:
        model = PestRiskEntryMainListing
        fields = ['months', 'year', 'commodity']
        labels = {   
            'months': 'Select Months',
            'year': 'Year:',
            'commodity': 'Commodity',
        }
        widgets = {
            'months': forms.CheckboxSelectMultiple(
                choices=MONTH_CHOICES,
                attrs={'class': 'form-check-input'}
            ),
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'commodity': forms.Select(attrs={'class': 'form-control'})
        }
        required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if the form is bound to an instance
        if self.instance and self.instance.pk:
            # For ManyToManyField or MultiSelectField storing month values
            # Convert them to a list of strings to match MONTH_CHOICES values
            self.fields['months'].initial = [
                str(month) for month in getattr(self.instance, 'months', [])
            ]

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
        model = PestAlertLevel
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
            'description': forms.Textarea(attrs={'class': 'form-control'}),
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