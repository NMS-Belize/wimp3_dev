from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from django.template import loader

#from django_tables2 import RequestConfig

#from django import forms
#from .forms import FormPestRisk

# Create your views here.

def index(request):
    template = loader.get_template('dashboard.html')
    #context = {'name': 'World'}  # Data to pass to the template
    return HttpResponse(template.render())