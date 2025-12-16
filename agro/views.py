from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.template import loader

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

#################### Create/Define Views ####################
def index(request):
    template = loader.get_template('agro_services.html')
    context = {'name': 'World'}  # Data to pass to the template
    return HttpResponse(template.render(context))
  
def livestock_entry(request):
    template = loader.get_template('entry_form_livestock.html')
    context = {'name': 'World'}  # Data to
    return HttpResponse(template.render(context))    

def pest_risk_list(request):
    #pr_data = PestRiskEntry.objects.all()
    #return render(request, "pest_risk_list.html", {"pest_risk_data": pr_data })
    #template = loader.get_template('pest_risk_list.html')
    #context = {}  # Data to pass to the template
    #return HttpResponse(template.render(context))
    table = PestRiskMainListTable(PestRiskEntryMainListing.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "pest_risk_list.html", {"table": table})

#################### PEST RISK DETAILS - TABLE ####################
def pest_risk_details_list(request, entry_id):
    qs = PestRiskEntryDetails.objects.filter(pest_risk_listing_id=entry_id)
    table = PestRiskDetailsTable(qs)
    RequestConfig(request).configure(table)
    return render(request, "pest_risk_list.html", {"table": table})

def pest_risk_entry_update(request, entry_id):
    
    entry = get_object_or_404(PestRiskEntryMainListing, id = entry_id)

    if request.method == 'POST':
        form = PestRiskMainListingForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('pest_risk_entry_update', entry_id = entry.id)
    else:
        form = PestRiskMainListingForm(instance=entry)  # <-- pre-fills the form

    return render(request, 'entry_form_pest_risk_update.html', {'form': form })

def pest_risk_entry_edit(request, entry_id):
    return render(request, 'entry_form_pest_risk_update.html', {'form': form })

########################## INITIALIZE A NEW FORM ##############################
def pest_risk_entry_new(request):

    form = PestRiskMainListingForm(request.POST)

    if form.is_valid():
        selected = form.cleaned_data['months']
        return render(request, 'pest_risk_new.html', { 'selected': selected })
    else:
        form = PestRiskMainListingForm()

    return render(request, 'pest_risk_new.html', { 'form' : form })

########################## INSER RECORD / PEST RISK MAIN ENTRY ##############################
def pest_risk_entry_add(request):

    if request.method == 'POST':

        form = PestRiskMainListingForm(request.POST)

        if form.is_valid():
            entry = form.save()  # this actually writes to DB
            return redirect('pest_risk_details', entry.id)
    else:
        form = PestRiskMainListingForm()

    return render(request, 'pest_risk_new.html', {'form': form})

def pest_risk_details(request, entry_id):

    if request.method == 'POST':

        form = PestRiskEntryFormDetails(request.POST)

        if form.is_valid():
            entry = form.save()
            return redirect('pest_risk_details', entry.id)
    else:
        form = PestRiskEntryFormDetails()

    return render(request, 'pest_risk_details.html', {'form': form})







    '''if form.is_valid():
        selected = form.cleaned_data.get('list_months')
        return render(request, 'entry_form_pest_risk.html', { 
            'selected': selected,
            'form': form,
            'pest_risk_start_id': entry_id
        })'''
    #else:
        #form = PestRiskEntryFormDetails(entry_id=entry_id)

    '''return render(request, 'pest_risk_list.html', {
        #'form': form,
        #'pest_risk_start_id': entry_id
    })'''

def pest_risk_add_details(request, entry_id):
    
    if request.method == 'POST':
        form = PestRiskEntryFormDetails(request.POST)
        if form.is_valid():
            # Get cleaned data
            pest_risk_listing_id = form.cleaned_data['pest_risk_listing_id']
            district_id         = form.cleaned_data['district_id']
            drought_alert_lvl_id = form.cleaned_data['drought_alert_lvl_id']
            temp_min        = form.cleaned_data['temp_min']
            temp_max        = form.cleaned_data['temp_max']
            precip_min  = form.cleaned_data['precip_min']
            precip_max  = form.cleaned_data['precip_max']
            effect      = form.cleaned_data['effect']
            actions     = form.cleaned_data['actions']
            info        = form.cleaned_data['info']

            # Save to DB
            entry = PestRiskEntryDetails.objects.create(
                pest_risk_listing_id  = pest_risk_listing_id,
                district_id         = district_id,         # list gets stored in JSONField
                drought_alert_lvl_id = drought_alert_lvl_id,
                temp_min        = temp_min,
                temp_max        = temp_max,
                precip_min      = precip_min,
                precip_max      = precip_max,
                effect          = effect,
                actions         = actions,
                info            = info
            )
            return redirect('pest_risk_list')  # replace with your success page/view
    else:
        form = FormPestRiskStartForm()
    return render(request, 'pest_risk_details.html', {'form': form })



############# TABLE LIST: PEST RISK VARIABlE - Commodity
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
        'new_url': "/agro-climat-services/pest-risk/commodity-entry/",
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
            return redirect('commodity_list', saved_entry.id)
    else:
        form = CommodityTypeForm(instance=entry)

    return render(request, 'entry_form.html', {
        'page_name': page_name,
        'new_url': "/agro-climat-services/pest-risk/commodity-entry/",
        'back_url': "/agro-climat-services/pest-risk/commodity-list/",
        'api_url': "/api/commodity-types/",
        'form': form,
        'entry': entry
    })

def commodity_type_delete(request, id):
    
    entry = get_object_or_404(CommodityType, id=id)
    
    page_name = "Commodity Type Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('commodity_list')  # redirect anywhere you prefer

    return render(request, "delete_confirm.html", {
        "entry": entry,
        'page_name': page_name,
    })

############# TABLE LIST: PEST RISK VARIABlE - Pest Alert Levels
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
        'new_url': "/agro-climat-services/pest-risk/pest-alert-level-entry/",
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
            return redirect('pest_alert_level_list', saved_entry.id)
    else:
        form = PestAlertLevelForm(instance=entry)

    return render(request, 'entry_form.html', {
        'page_name':    page_name,
        'new_url':      "/agro-climat-services/pest-risk/pest-alert-level-entry/",
        'back_url':     "/agro-climat-services/pest-risk/apest-alert-level-list/",
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

    return render(request, "delete_confirm.html", {
        "entry": entry,
        'page_name': page_name,
    })


#################### DROUGHT ALERT LEVELS - TABLE ####################
def drought_alert_level_list(request):
    page_name = "Drought Alert Levels"
    qs = DroughtAlertLevel.objects.all().order_by('id')
    table = PestAlertLevelsTable(qs)
    RequestConfig(request).configure(table)
    context = {
        'page_name': page_name,
        'table': table
    }
    return render(request, 'table_list_template.html', context)




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
        'new_url': "/agro-climat-services/pest-risk/action-items-entry/",
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
        return redirect('action_items_list')  # redirect anywhere you prefer

    return render(request, "delete_confirm.html", {
        "entry": entry,
        'page_name': page_name,
    })

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
        'new_url': "/agro-climat-services/pest-risk/effect-items-entry/",
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
            return redirect('effect_items_list', saved_entry.id)
    else:
        form = EffectItemsForm(instance=entry)

    return render(request, 'entry_form.html', {
        'page_name':    page_name,
        'new_url':      "/agro-climat-services/pest-risk/effect-items-entry/",
        'back_url':     "/agro-climat-services/pest-risk/effect-items-list/",
        'api_url':      "/api/effect-items/",
        'form':         form,
        'entry':        entry
    })

def effect_items_delete(request, id):
    
    entry = get_object_or_404(PestRiskEffect, id=id)
    
    page_name = "Effect Item Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('effect_items_list')  # redirect anywhere you prefer

    return render(request, "delete_confirm.html", {
        "entry": entry,
        'page_name': page_name,
    })

#################### PEST ALERT LEVELS - UPDATE ####################
def pest_alert_level_update(request, entry_id):
    
    entry = get_object_or_404(PestAlertLevel, id = entry_id)

    if request.method == 'POST':
        form = PestRiskMainListingForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('pest_risk_entry_update', entry_id = entry.id)
    else:
        form = PestRiskMainListingForm(instance=entry)  # <-- pre-fills the form

    return render(request, 'pest_alert_level_update.html', {'form': form })
#################### Form Processing ####################


#API endpoint that allows groups to be viewed or edited.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

#API endpoint that allows groups to be viewed or edited.
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

class PestRiskEntryDetailsViewSet(viewsets.ModelViewSet):
   queryset = PestRiskEntryDetails.objects.all().order_by('id')
   serializer_class = sx.PestRiskEntryDetailsSerializer

class PestRiskMainListingViewSet(viewsets.ModelViewSet):
   #queryset = PestRiskEntryMainListing.objects.all().order_by('id')
   #serializer_class = sx.PestRiskEntryMainListingSerializer
   queryset = PestRiskEntryMainListing.objects.all().prefetch_related("pest_risk_entries")
   serializer_class = sx.PestRiskEntryMainListingSerializer