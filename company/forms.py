from django import forms

from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name','short_name','established_date','logo','website','address_line1','address_line2','city','district','phone','email','registration_number','tax_id_number']
        labels = {   
            # <-- add human-friendly labels here
            'company_name': 'Company Name:',
            'short_name': 'Short Name:',
            'established_date': 'Established Date:'
        }
        widgets = {            
            'company_name':     forms.TextInput(attrs={'class': 'form-control'}),
            'short_name':       forms.TextInput(attrs={'class': 'form-control'}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "email":            forms.EmailInput(attrs={"class": "form-control","placeholder": "Email Address"}),
            "logo":             forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "website":          forms.URLInput(attrs={"class": "form-control", "placeholder": "https://www.example.com"}),
            "address_line1":    forms.TextInput(attrs={ "class": "form-control", "placeholder": "Address Line 1"}),
            "address_line2":    forms.TextInput(attrs={"class": "form-control","placeholder": "Address Line 2"
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City"
                }
            ),

            "district": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "District"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number"
                }
            ),

            

            "registration_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Registration Number"
                }
            ),

            "tax_id_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tax ID Number"
                }
            ),

            '''"contact_person": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Contact Person"
                }
            ),

            "mobile_contact_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Mobile Contact Number"
                }
            ),

            "vision": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Company Vision"
                }
            ),

            "mission": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Company Mission"
                }
            ),'''

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }