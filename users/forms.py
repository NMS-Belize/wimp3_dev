from django import forms

from users.models import UserProfile, Employee
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserEntryForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","is_active","is_staff")
        widgets = { 
            'username': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'width': '100%', 'readonly': 'readonly'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'width': '100%'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'width': '100%'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'width': '100%'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for name, field in self.fields.items():
                if name in ("is_active", "is_staff"):
                    field.widget.attrs["class"] = "form-check-input"
                else:
                    field.widget.attrs["class"] = "form-control"

            #self.fields["password1"].help_text = ""

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["phone","department","job_title"]
        widgets = {
            "phone": forms.TextInput(attrs={"class": "form-control", "type": "text", "width": "100%"}),
            "department": forms.Select(attrs={"class": "form-select", "width": "100%"}),
            "job_title": forms.Select(attrs={"class": "form-select", "width": "100%"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["first_name","last_name","job_title","department","email","phone","office_location","has_user_account","user"]
        widgets = {            
            'first_name':   forms.TextInput(attrs={'class': 'form-control', 'placeholder':'First Name'}),
            'last_name':    forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}),
            'email':        forms.EmailInput(attrs={'class': 'form-control'}),
            "phone":        forms.TextInput(attrs={"class": "form-control", "type": "text", "width": "100%"}),
            "department":   forms.Select(attrs={"class": "form-select", "width": "100%"}),
            "job_title":    forms.Select(attrs={"class": "form-select", "width": "100%"}),
            'has_user_account': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'user':         forms.Select(attrs={"class": "form-select", }),
        }