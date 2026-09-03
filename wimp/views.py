from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.urls import reverse
from django.template import loader

from rest_framework.decorators import api_view
from rest_framework.response import Response

from company.models import Company

def index(request):
    template = loader.get_template('entry_form_user_login.html')
    context = {'page_name': 'Home'}  
    return HttpResponse(template.render(context))

@login_required
def dashboard(request):

    '''if id:
        entry = get_object_or_404(Company, id=id)
    else:
        entry = None'''
            
    context = {
        'page_name': 'Dashboard'
    }
    return render(request, 'dashboard.html', context)