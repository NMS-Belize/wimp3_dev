from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
#from django.contrib.auth import login as auth_login

from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
from django.urls import reverse
from django.template import loader

#from django_tables2 import RequestConfig

#from django import forms
#from .forms import FormPestRisk

# Create your views here.

def index(request):
    template = loader.get_template('entry_form_user_login.html')
    context = {'name': 'World'}  # Data to pass to the template
    return HttpResponse(template.render(context))
    #return render(request, 'entry_form_user_login.html', context)

@login_required
def dashboard(request):
    context = {
        'page_name': 'Home Dashboard'
    }
    return render(request, 'dashboard.html', context)

