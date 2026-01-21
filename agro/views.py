import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.urls import reverse

import calendar

from django.template import loader

from django.contrib.auth import login as auth_login

#from .models import CommodityType, CommodityCategory, District, PestAlertLevel, PestRiskEntryMainListing, PestRiskEntryDetails, DroughtAlertLevel, PestRiskAction, PestRiskEffect
from .models import *

from django_tables2 import RequestConfig
#from .tables import PestRiskListTable, PestRiskMainListTable, PestRiskDetailsTable, PestAlertLevelsTable, ActionItemsTable, EffectItemsTable
from .tables import *

#from .serializers import CommodityTypeSerializer, CommodityCategorySerializer
from . import serializers as sx

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from wimp.serializers import GroupSerializer, UserSerializer

#from .forms import  FormPestRiskStartForm, PestRiskMainListingForm, PestRiskEntryFormDetails, PestAlertLevelForm
from .forms import *

from django.forms.models import model_to_dict

#################### Create/Define Views ####################
#@login_required
def index(request):
    context = {
        'page_name': 'Agro-Met Services'
    }
    return render(request, 'agro_services.html', context)
  
def livestock_entry(request):
    template = loader.get_template('entry_form_livestock.html')
    context = {'name': 'World'}  # Data to
    return HttpResponse(template.render(context))    

############# PEST RISK ENTRY
def pest_risk_list(request, id=None):
    page_name = "Pest Risk Entries"
    qs = PestRiskEntryMainListing.objects.all().order_by('-id')
    table = PestRiskMainListTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(PestRiskEntryMainListing, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'table': table,
        'new_url':  reverse('agro:pest_risk_entry'),
        'back_url': reverse('agro:index'),
        'api_url': "/api/pest-risk/",
    }
    return render(request, 'table_list_main.html', context)

def pest_risk_entry(request, id=None):

    page_name = "Pest Risk Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(PestRiskEntryMainListing, id=id)

        #if entry.months:
        #    entry.months = json.loads(entry.months)
    else:
        entry = None

    if request.method == 'POST':
        form = PestRiskMainListingForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('agro:pest_risk_details_list', saved_entry.id)
    else:
        form = PestRiskMainListingForm(instance=entry)

    return render(request, 'entry_form_pest_risk_main.html', {
        'page_name':    page_name,
        'new_url':      reverse('agro:pest_risk_entry'),
        'details_url':  "",
        'back_url':     reverse('agro:pest_risk_list'),
        'api_url':      "/api/pest-risk/",
        'form': form,
        'entry': entry
    })

def pest_risk_delete(request, id):
    
    entry = get_object_or_404(PestRiskEntryMainListing, id=id)

    qs = PestRiskEntryDetails.objects.all().order_by('id')
    # Filter details by parent listing
    qs = qs.filter(pest_risk_listing_id=id)
    qs = qs.order_by('id')
    
    page_name = "Pest Risk Entry"
    month_names = [calendar.month_name[int(m)] for m in entry.months]

    if request.method == "POST":
        entry.delete()
        
        return redirect('agro:pest_risk_list')  # redirect anywhere you prefer

    return render(request, "delete_pr_confirm.html", {
        "entry": entry,
        'page_name': page_name,
        'month_names': month_names,
        'details': qs
    })

def pest_risk_details_list(request, id=None, fk=None):
    page_name = "Pest Risk Details"
    qs = PestRiskEntryDetails.objects.all().order_by('id')
    
    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(PestRiskEntryMainListing, id=id)

        # Filter details by parent listing
        qs = qs.filter(pest_risk_listing_id=id)
        qs = qs.order_by('id')

    table = PestRiskDetailsTable(qs)
    RequestConfig(request).configure(table)

    month_names = [calendar.month_name[int(m)] for m in entry.months]

    context = {
        'id' : id,
        'fk': fk,
        'entry': entry,  
        'page_name': page_name,
        'month_names': month_names,
        'table':    table,
        'new_url':  reverse('agro:pest_risk_entry'),
        'back_url': reverse('agro:pest_risk_list'),
        'api_url': "/api/pest-risk-/",
    }
    return render(request, 'table_list_pest_risk_details_template.html', context)

def pest_risk_details_create(request, fk, id=None):

    # Parent object (FK) is REQUIRED
    parent_entry = get_object_or_404(PestRiskEntryMainListing, id=fk)

    page_name = f"Pest Risk Entry Details: {parent_entry}"

   # Child object (details)
    entry = None
    if id:
        entry = get_object_or_404(PestRiskEntryDetails,id=id,pest_risk_listing=parent_entry)

    if request.method == 'POST':
        form = PestRiskEntryDetailsForm(request.POST, instance=entry)
        form.instance.pest_risk_listing_id = PestRiskEntryMainListing.objects.get(id=fk)

        if form.is_valid():
            saved_entry = form.save(commit=False)
            saved_entry.pest_risk_listing  = parent_entry   # set FK
            saved_entry.save()

            return redirect('agro:pest_risk_details_list', parent_entry.id)
    else:
        form = PestRiskEntryDetailsForm(instance=entry)

    return render(request, 'entry_form_pest_risk.html', {
        'page_name': page_name,
        'new_url':      reverse('agro:pest_risk_entry'),
        'details_url':  reverse('agro:pest_risk_details_create', args=[parent_entry.id]),
        'back_url':     reverse('agro:pest_risk_list'),
        'api_url': "/api/pest-risk-entries/",
        'form': form,
        'entry': entry,
        'parent_entry': parent_entry,
        'parent_id': parent_entry.id,
        'fk': fk
    })

def pest_risk_details_entry(request, id=None, fk=None):

    # Parent object (FK) is REQUIRED
    parent_entry = get_object_or_404(PestRiskEntryMainListing, id=fk)

    page_name = f"Pest Risk Entry Details: {parent_entry}"

   # Child object (details)
    entry = None
    if id:
        entry = get_object_or_404(PestRiskEntryDetails,id=id)

    if request.method == 'POST':
        form = PestRiskEntryDetailsForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save(commit=False)
            saved_entry.pest_risk_listing  = parent_entry   # set FK
            saved_entry.save()

            return redirect('agro:pest_risk_details_list', parent_entry.id)
    else:
        form = PestRiskEntryDetailsForm(instance=entry)

    return render(request, 'entry_form_pest_risk.html', {
        'page_name': page_name,
        'new_url':      reverse('agro:pest_risk_entry'),
        'details_url':  reverse('agro:pest_risk_details_create', args=[parent_entry.id]),
        'back_url':     reverse('agro:pest_risk_list'),
        'api_url': "/api/pest-risk-entries/",
        'form': form,
        'entry': entry,
        'parent_entry': parent_entry,
        'parent_id': parent_entry.id
    })

def pest_risk_details_delete(request, id=None, fk=None):
    entry = get_object_or_404(PestRiskEntryDetails, id=id)
    
    page_name = "Pest Risk Details Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('agro:pest_risk_details_list', fk)  # redirect anywhere you prefer

    return render(request, "delete_pest_risk_details.html", {
        "entry": entry,
        'page_name': page_name,
        "main_id":fk
    })

def duplicate_object_pest_risk_details(obj):    
    obj.pk = None                # this is the key trick
    obj.id = None
    obj.published_date = None
    obj.updated_datetime = None
    obj.save()
    return obj

def pest_risk_details_entry_duplicate(request, id, fk=None):
    obj = get_object_or_404(PestRiskEntryDetails, pk=id)
    duplicate_object_pest_risk_details(obj)
    return redirect('agro:pest_risk_details_list', id=fk)

############# PEST RISK VARIABlE - Commodity
def commodity_list(request, id=None):
    page_name = "Commodity"
    qs = CommodityType.objects.all().order_by('id')
    table = CommodityTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(CommodityType, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'table': table,
        'new_url': reverse('agro:commodity_entry'),
        'api_url': "/api/commodity-types/",
    }
    return render(request, 'table_list_template.html', context)

def commodity_entry(request, id=None):

    page_name = "Commodity Type Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(CommodityType, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = CommodityTypeForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('agro:commodity_list', saved_entry.id)
    else:
        form = CommodityTypeForm(instance=entry)

    return render(request, 'entry_form.html', {
        'page_name': page_name,
        'new_url': reverse('agro:commodity_entry'),
        'back_url': reverse('agro:commodity_list'),
        'api_url': "/api/commodity-types/",
        'form': form,
        'entry': entry
    })

def commodity_type_delete(request, id):
    
    entry = get_object_or_404(CommodityType, id=id)
    
    page_name = "Commodity Type Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('agro:commodity_list')  # redirect anywhere you prefer

    return render(request, "delete_commodity.html", {
        "entry": entry,
        'page_name': page_name,
    })

############# PEST RISK VARIABlE - Pest Alert Levels
def pest_alert_level_list(request, id=None):

    page_name = "Pest Alert Levels"
    qs = PestAlertLevel.objects.all().order_by('id')
    table = PestAlertLevelsTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(PestAlertLevel, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'table': table,
        'new_url': reverse('agro:pest_alert_level_entry'),
        'api_url': "/api/pest-alert-levels/",
    }
    return render(request, 'table_list_template.html', context)

def pest_alert_level_entry(request, id=None):

    page_name = "Pest Alert Level Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(PestAlertLevel, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = PestAlertLevelForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('agro:pest_alert_level_list', saved_entry.id)
    else:
        form = PestAlertLevelForm(instance=entry)

    return render(request, 'entry_form.html', {
        'page_name':    page_name,
        'new_url':      reverse('agro:pest_alert_level_entry'),
        'back_url':     reverse('agro:pest_alert_level_list'),
        'api_url':      "/api/pest-alert-levels/",
        'form':         form,
        'entry':        entry
    })

def pest_alert_level_delete(request, id):
    
    entry = get_object_or_404(PestAlertLevel, id=id)
    
    page_name = "Pest Alert Level Type Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('pest_alert_level_list')  # redirect anywhere you prefer

    return render(request, "delete_pest_alert_level.html", {
        "entry": entry,
        'page_name': page_name,
    })

#################### DROUGHT ALERT LEVELS - TABLE ####################
def drought_alert_level_list(request):
    page_name = "Drought Alert Levels"
    qs = DroughtAlertLevel.objects.all().order_by('id')
    table = DroughtAlertLevelsTable(qs)
    RequestConfig(request).configure(table)
    context = {
        'page_name':    page_name,
        'new_url':      reverse('agro:drought_alert_level_entry'),
        'back_url':     reverse('agro:drought_alert_level_list'),
        'api_url':      "/api/drought-alert-levels/",
        'table':        table
    }
    return render(request, 'table_list_template.html', context)

def drought_alert_level_entry(request, id=None):

    page_name = "Drought Alert Level Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(DroughtAlertLevel, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = DroughtAlertLevelForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('agro:drought_alert_level_list', saved_entry.id)
    else:
        form = DroughtAlertLevelForm(instance=entry)

    return render(request, 'entry_form.html', {
        'page_name':    page_name,
        'new_url':      reverse('agro:drought_alert_level_entry'),
        'back_url':     reverse('agro:drought_alert_level_list'),
        'api_url':      "/api/drought-alert-levels/",
        'form':         form,
        'entry':        entry
    })

def drought_alert_level_delete(request, id):
    
    entry = get_object_or_404(DroughtAlertLevel, id=id)
    
    page_name = "Drought Alert Level Type Entry"
    if request.method == "POST":
        entry.delete()
        return redirect('drought_alert_level_list')  # redirect anywhere you prefer

    return render(request, "delete_confirm.html", {
        "entry": entry,
        'page_name': page_name,
    })

#################### PEST RISK ACTION ITEMS - TABLE ####################
def action_items_list(request, id=None):

    page_name = "Action Items"
    qs = PestRiskAction.objects.all().order_by('id')
    table = ActionItemsTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(PestRiskAction, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'table': table,
        'new_url': reverse('agro:action_items_entry'),
        'api_url': "/api/action-items/",
    }
    return render(request, 'table_list_template.html', context)

def action_items_entry(request, id=None):

    page_name = "Action Items Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(CommodityType, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = ActionItemsForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('action_items_list', saved_entry.id)
    else:
        form = ActionItemsForm(instance=entry)

    return render(request, 'entry_form.html', {
        'page_name':    page_name,
        'new_url':      "/agro-climat-services/pest-risk/action-items-entry/",
        'back_url':     "/agro-climat-services/pest-risk/action-items-list/",
        'api_url':      "/api/action-items/",
        'form':         form,
        'entry':        entry
    })

def action_items_delete(request, id):
    
    entry = get_object_or_404(PestRiskAction, id=id)
    
    page_name = "Action Item Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('agro:action_items_list')  # redirect anywhere you prefer

    return render(request, "delete_pest_risk_action.html", {
        "entry": entry,
        'page_name': page_name,
    })

def duplicate_object_pest_risk_action(obj):
    data = model_to_dict(obj)
    data.pop('id', None)
    data['action_description'] = f"{obj.action_description}"
    return obj.__class__.objects.create(**data)

def action_items_entry_duplicate(request, id):
    obj = get_object_or_404(PestRiskAction, pk=id)
    duplicate_object_pest_risk_action(obj)
    return redirect('agro:action_items_list')

#################### PEST RISK EFFECT ITEMS - TABLE ####################
def effect_items_list(request, id=None):
    
    page_name = "Effect Items"
    qs = PestRiskEffect.objects.all().order_by('id')
    table = EffectItemsTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(PestRiskEffect, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'table': table,
        'new_url': reverse('agro:effect_items_entry'),
        'api_url': "/api/effect-items/",
    }
    return render(request, 'table_list_template.html', context)

def effect_items_entry(request, id=None):

    page_name = "Effect Items Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(PestRiskEffect, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = EffectItemsForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('agro:effect_items_list', saved_entry.id)
    else:
        form = EffectItemsForm(instance=entry)

    return render(request, 'entry_form.html', {
        'page_name':    page_name,
        'new_url':      reverse('agro:effect_items_entry'),
        'back_url':     reverse('agro:effect_items_list'),
        'api_url':      "/api/effect-items/",
        'form':         form,
        'entry':        entry
    })

def effect_items_delete(request, id):
    
    entry = get_object_or_404(PestRiskEffect, id=id)
    
    page_name = "Effect Item Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('agro:effect_items_list')  # redirect anywhere you prefer

    return render(request, "delete_pest_risk_effect.html", {
        "entry": entry,
        'page_name': page_name,
    })

def duplicate_object_pest_risk_effect(obj):
    data = model_to_dict(obj)
    data.pop('id', None)
    data['effect_description'] = f"{obj.effect_description}"
    return obj.__class__.objects.create(**data)

def effect_items_entry_duplicate(request, id):
    obj = get_object_or_404(PestRiskEffect, pk=id)
    duplicate_object_pest_risk_effect(obj)
    return redirect('agro:effect_items_list')

#API endpoint that allows groups to be viewed or edited.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

#API endpoint that allows groups to be viewed or edited.
class DistrictViewSet(viewsets.ModelViewSet):
   queryset = District.objects.all().order_by('id')
   serializer_class = sx.DistrictSerializer

class CommodityTypeViewSet(viewsets.ModelViewSet):
   queryset = CommodityType.objects.all().order_by('id')
   serializer_class = sx.CommodityTypeSerializer

class CommodityCategoryViewSet(viewsets.ModelViewSet):
   queryset = CommodityCategory.objects.all().order_by('id')
   serializer_class = sx.CommodityCategorySerializer

class ActionItemsViewSet(viewsets.ModelViewSet):
   queryset = PestRiskAction.objects.all().order_by('id')
   serializer_class = sx.ActionItemsSerializer

class EffectItemsViewSet(viewsets.ModelViewSet):
   queryset = PestRiskEffect.objects.all().order_by('id')
   serializer_class = sx.EffectItemsSerializer

class PestAlertLevelViewSet(viewsets.ModelViewSet):
   queryset = PestAlertLevel.objects.all().order_by('id')
   serializer_class = sx.PestAlertLevelSerializer

class DroughtAlertLevelViewSet(viewsets.ModelViewSet):
   queryset = DroughtAlertLevel.objects.all().order_by('id')
   serializer_class = sx.DroughtAlertLevelSerializer    

class PestRiskEntryDetailsViewSet(viewsets.ModelViewSet):
   queryset = PestRiskEntryDetails.objects.all().order_by('id')
   serializer_class = sx.PestRiskEntryDetailsSerializer

class PestRiskMainListingViewSet(viewsets.ModelViewSet):
   #queryset = PestRiskEntryMainListing.objects.all().order_by('id')
   #serializer_class = sx.PestRiskEntryMainListingSerializer
   queryset = PestRiskEntryMainListing.objects.all().prefetch_related("pest_risk_entries")
   serializer_class = sx.PestRiskEntryMainListingSerializer