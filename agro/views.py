import calendar, json

from django.db import IntegrityError
from django.db.models import Prefetch

from django.contrib import messages
#from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.urls import reverse

from django_tables2 import RequestConfig
from rest_framework import permissions, viewsets
from wimp.serializers import GroupSerializer, UserSerializer

from agro.models import PestRisk, PestRiskEntryDetails, PestRiskAction, PestRiskEffect, Sector, Commodity, DroughtAlertLevel, PestRiskInfo
from agro.forms import PestRiskForm, PestRiskEntryDetailsForm, SectorForm, CommodityTypeForm, DroughtAlertLevelForm, ActionItemsForm, EffectItemsForm, InfoItemsForm
from agro.filters import InfoItemFilter, EffectItemFilter, ActionItemFilter
from agro.tables import PestRiskMainListTable, PestRiskDetailsTable, SectorTable, ActionItemsTable, CommodityTable, DroughtAlertLevelsTable, EffectItemsTable, InfoItemsTable
from agro.serializers import CommodityCategorySerializer, SectorSerializer, PestRiskEntryDetailsSerializer, PestRiskSerializer, ActionItemsSerializer, EffectItemsSerializer, DroughtAlertLevelSerializer

from system_core.models import Zone, District, AlertLevel
from system_core.serializers import ZoneSerializer, DistrictSerializer

#from .serializers import CommodityTypeSerializer, CommodityCategorySerializer

#################### Create/Define Views ####################
def index(request):
    context = {
        'page_name': 'Agriculture Services'
    }
    return render(request, 'agro_home.html', context) 

############# PEST RISK ENTRY
def pest_risk_list(request, id=None):

    page_name = "Pest Risk"

    id = 1
    
    qs = Commodity.objects.all().order_by('sector__id','description')
    table = PestRiskMainListTable(qs)

    RequestConfig(request).configure(table)    
    
    # Load entry ONLY if id is provided
    entry = None

    if id is not None:
        entry = get_object_or_404(PestRisk, id=id)
        print(type(entry.months))
        
        #if entry.months:
        #    entry.months = json.loads(entry.months)

    if request.method == 'POST':
        form = PestRiskForm(request.POST, instance=entry)
        
        if form.is_valid():
            try:
                saved_entry = form.save()
                return redirect('agro:pest_risk_list_id', saved_entry.id)
            except IntegrityError:
                form.add_error(None, "This combination of Months, Year and Commodity already exists.")

        # Temporary debugging.
        print(form.errors)
    else:
        form = PestRiskForm(instance=entry)
        print(form.errors)

    context = {
        'id' : id,
        'entry': entry,
        'page_name': page_name,
        'prev_page': "Agriculture Services",
        'table': table,
        'form': form,
        'back_url': reverse('agro:index'),
        'api_url': reverse('pestrisk-list')
    }
    return render(request, 'pest-risk/table_list_main.html', context)

def pest_risk_entry(request, id=None):

    page_name = "Pest Risk Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(PestRisk, id=id)

        #if entry.months:
        #    entry.months = json.loads(entry.months)
    else:
        entry = None

    if request.method == 'POST':
        form = PestRiskMainListingForm(request.POST, instance=entry)

        #if form.is_valid():
        #   saved_entry = form.save()    # Creates or updates
        #  return redirect('agro:pest_risk_details_list', saved_entry.id)
        
        if form.is_valid():
            try:
                saved_entry = form.save()
                return redirect('agro:pest_risk_details_list', saved_entry.id)
            except IntegrityError:
                form.add_error(None, "This combination of Months, Year and Commodity already exists.")
    else:
        #form = PestRiskMainListingForm(instance=entry)
        form = PestRiskMainListingForm(instance=entry,initial={'months': True})

    return render(request, 'entry_form_pest_risk_main.html', {
        'page_name':    page_name,
        'new_url':      reverse('agro:pest_risk_entry'),
        'details_url':  "",
        'back_url':     reverse('agro:pest_risk_list'),
        'api_url':      "/api/pest-risk/",
        'form': form,
        'entry': entry
    })

def pest_risk_details_list(request,c_id=None):

    page_name   = "Pest Risk Details"
    #pr_id       = 1       #Updates Single Pest Risk Main Record

    entry       = get_object_or_404(Commodity, id=c_id)
    print(entry.description)
    #print(entry)

    #c_id = entry.commodity_id_id
    #commodity_entry = get_object_or_404(Commodity, id=c_id)

    #print(entry)
    qs = PestRiskEntryDetails.objects.all().order_by('id').filter(commodity_id_id=c_id)
    table = PestRiskDetailsTable(qs)
    RequestConfig(request).configure(table)

    context = {
        #'id': pr_id,
        'commodity_id': c_id,
        'commodity': entry.description,
        'page_name': page_name,
        'prev_page': "Pest Risk List",
        'table': table,
        'back_url': reverse('agro:pest_risk_list'),
        'api_url': reverse('pestrisk-list'),
    }
    return render(request,'pest-risk/table_list_details_template.html',context)

def pest_risk_details_entry(request, id=None):

    entry = get_object_or_404(PestRiskEntryDetails,id=id)

    # SAVE ORIGINAL VALUES BEFORE FORM VALIDATION
    commodity = entry.commodity_id
    district = entry.district_id
    c_id = entry.commodity_id_id

    pest_colors = {
        str(level.id): level.color
        for level in AlertLevel.objects.all()
    }

    drought_colors = {
        str(level.id): level.color_hex
        for level in DroughtAlertLevel.objects.all()
    }

    c_id = entry.commodity_id_id 

    page_name = "Pest Risk Details Entry"

    if request.method == 'POST':
        form = PestRiskEntryDetailsForm(request.POST, instance=entry, commodity=entry.commodity_id, district=entry.district_id)

        #messages.info(request, f"Effect POST: {request.POST.getlist('effect')}")
        #messages.info(request, f"Info POST: {request.POST.getlist('info')}")
        #messages.info(request, f"Actions POST: {request.POST.getlist('actions')}")

        if form.is_valid():
            saved_entry = form.save(commit=False)

            # Restore original FK values
            saved_entry.commodity_id = commodity
            saved_entry.district_id = district

            saved_entry.save()
            form.save_m2m()

            messages.success(request, "Pest Risk Details saved successfully.")
            #messages.info(request, f"Saved Effects: {list(saved_entry.effect.values_list('id', flat=True))}")
            #messages.info(request, f"Saved Info: {list(saved_entry.info.values_list('id', flat=True))}")
            #messages.info(request, f"Saved Actions: {list(saved_entry.actions.values_list('id', flat=True))}")

            return redirect('agro:pest_risk_details_list', c_id)
        else:
            messages.error(request, f"Form could not be saved: {form.errors.as_text()}")
    else:
        form = PestRiskEntryDetailsForm(instance=entry)

    context = {
        'page_name': page_name,
        'back_url':     reverse('agro:pest_risk_list'),
        'api_url': "/api/pest-risk-entries/",
        'form' : form,
        'entry' : entry,
        "pest_colors": pest_colors,
        "drought_colors": drought_colors,
    }

    return render(request, 'pest-risk/entry_form_details.html', context)

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

@require_POST
@permission_required("agro.change_pestriskentrymainlisting", raise_exception=True)
def pest_risk_toggle_is_published(request, id, commodity):
    record = get_object_or_404(PestRiskEntryDetails, id=id)

    record.is_published = not record.is_published
    record.save(update_fields=["is_published"])

    status = "published" if record.is_published else "unpublished"
    messages.success(request, f"Record {status} successfully.")

    return redirect("agro:pest_risk_details_list",commodity)

############# PEST RISK VARIABlE - Sector
def sector_list(request, id=None):
    page_name = "Sector"
    qs = Sector.objects.all().order_by('id')
    table = SectorTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(Sector, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': "Agriculture Services",
        'table': table,
        'new_url': reverse('agro:sector_entry'),
        'back_url': reverse('agro:index'),
        'api_url': reverse('sectors-list'),
    }
    return render(request, 'table_list_template.html', context)

def sector_entry(request, id=None):

    page_name = "Sector Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(Sector, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = SectorForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('agro:sector_list', saved_entry.id)
    else:
        form = SectorForm(instance=entry)

    return render(request, 'pest-risk/parameters_entry_form.html', {
        'page_name': page_name,
        'prev_page': "Sector List",
        'new_url':  reverse('agro:sector_entry'),
        'back_url': reverse('agro:sector_list'),
        'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })

def sector_delete(request, id):
    
    entry = get_object_or_404(Sector, id=id)
    
    page_name = "Zone/Area Entry"

    if request.method == "POST":
        entry.delete()
        messages.success(request, "deleted")  # acts like True
        return redirect('agro:sector_list')  # redirect anywhere you prefer
    
    return render(request, "delete_sector.html", {
        "entry": entry,
        'page_name': page_name,
    })

############# PEST RISK VARIABlE - District/Zone
'''
def district_zone_list(request, id=None):
    page_name = "District/Zone"
    qs = District.objects.all().order_by('id')
    table = DistrictZoneTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(District, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': "Agriculture Services",
        'table': table,
        'new_url': reverse('agro:district_zone_entry'),
        'api_url': reverse('districts-list'),
        'back_url': reverse('agro:index'),
    }
    return render(request, 'table_list_template.html', context)

def district_zone_entry(request, id=None):

    page_name = "District/Zone Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(District, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = DistrictZoneForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('agro:district_zone_list', saved_entry.id)
    else:
        form = DistrictZoneForm(instance=entry)

    return render(request, 'entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('agro:district_zone_entry'),
        'back_url': reverse('agro:district_zone_list'),
        'api_url':  reverse('districts-list'),
        'form': form,
        'entry': entry
    })

def district_zone_delete(request, id):
    
    entry = get_object_or_404(District, id=id)
    
    page_name = "District/Zone Entry"

    if request.method == "POST":
        entry.delete()
        messages.success(request, "deleted")  # acts like True
        return redirect('agro:district_zone_list')  # redirect anywhere you prefer
    
    return render(request, "delete_district.html", {
        "entry": entry,
        'page_name': page_name,
    })
'''
############# PEST RISK VARIABlE - Commodity
def commodity_list(request, id=None):
    page_name = "Commodity"
    qs = Commodity.objects.all().order_by('id')
    table = CommodityTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(Commodity, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': "Agriculture Services",
        'table': table,
        'new_url': reverse('agro:commodity_entry'),
        'api_url': reverse('commodity-list'),
        'back_url': reverse('agro:index'),
    }
    return render(request, 'table_list_template.html', context)

def commodity_entry(request, id=None):

    page_name = "Commodity Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(Commodity, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = CommodityTypeForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('agro:commodity_list', saved_entry.id)
    else:
        form = CommodityTypeForm(instance=entry)

    return render(request, 'pest-risk/parameters_entry_form.html', {
        'page_name': page_name,
        'prev_page': "Commodity List",
        'new_url':  reverse('agro:commodity_entry'),
        'back_url': reverse('agro:commodity_list'),
        'api_url':  reverse('commodity-list'),
        'form': form,
        'entry': entry
    })

def commodity_type_delete(request, id):
    
    entry = get_object_or_404(Commodity, id=id)
    
    page_name = "Commodity Type Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('agro:commodity_list')  # redirect anywhere you prefer

    return render(request, "delete_commodity.html", {
        "entry": entry,
        'page_name': page_name,
    })

    
    entry = get_object_or_404(PestAlertLevel, id=id)
    
    page_name = "Pest Alert Level Type Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('agro:pest_alert_level_list')  # redirect anywhere you prefer

    return render(request, "delete_pest_alert_level.html", {
        "entry": entry,
        'page_name': page_name,
    })

#################### DROUGHT ALERT LEVELS - TABLE ####################
def drought_alert_level_list(request, id=None):
    
    page_name = "Drought Alert Levels"
    qs = DroughtAlertLevel.objects.all().order_by('id')
    table = DroughtAlertLevelsTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(DroughtAlertLevel, id=id)  

    context = {
        'id' : id,
        'entry': entry,  
        'page_name':    page_name,
        'prev_page':    "Agriculture Services",
        'new_url':      reverse('agro:drought_alert_level_entry'),
        'back_url':     reverse('agro:index'),
        'api_url':      reverse('droughtalertlevels-list'),
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
            return redirect('agro:drought_alert_level_list_id', saved_entry.id)
    else:
        form = DroughtAlertLevelForm(instance=entry)

    return render(request, 'pest-risk/parameters_entry_form.html', {
        'page_name':    page_name,
        'prev_page':    "Drought Alert Level List",
        'new_url':      reverse('agro:drought_alert_level_entry'),
        'back_url':     reverse('agro:drought_alert_level_list'),
        'api_url':      reverse('droughtalertlevels-list'),
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
    qs = PestRiskAction.objects.all().order_by('commodity','action_description')
    filterset = ActionItemFilter(request.GET, queryset=qs)

    table = ActionItemsTable(filterset.qs)
    table.empty_text = "No records available"

    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(PestRiskAction, id=id)

    context = {
        'id' :      id,
        'entry':    entry,  
        'page_name': page_name,
        'prev_page': "Agriculture Services",
        'table':    table,
        'filter':   filterset,
        'new_url':  reverse('agro:action_items_entry'),
        'back_url': reverse('agro:index'),
        'api_url':  reverse('actionitems-list'),
    }
    return render(request, 'pest-risk/parameters_table_list.html', context)

def action_items_entry(request, id=None):

    page_name = "Action Items Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(PestRiskAction, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = ActionItemsForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            messages.success(request,(f"Item created/updated"))
            return redirect('agro:action_items_list', saved_entry.id)
        else:
            messages.error(request,f"Unable to update/create")
    else:
        form = ActionItemsForm(instance=entry)

    return render(request, 'pest-risk/parameters_entry_form.html', {
        'page_name':    page_name,
        'prev_page':    "Action Items List",
        'new_url':      reverse('agro:action_items_entry'),
        'back_url':     reverse('agro:action_items_list'),
        'api_url':      reverse('actionitems-list'),
        'form':         form,
        'entry':        entry
    })

def action_items_delete(request, id):
    
    entry = get_object_or_404(PestRiskAction, id=id)
    
    page_name = "Action Item Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('agro:action_items_list')  # redirect anywhere you prefer

    return render(request, "pest-risk/parameters_delete.html", {
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

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
@require_POST
def import_agro_data(request):
    try:
        call_command("import_agro_data")
        messages.success(request,"Agro data imported successfully.")

    except Exception as error:
        messages.error(request,f"Agro data import failed: {error}")

    return redirect("agro:index")

@login_required
@user_passes_test(is_admin)
@require_POST
def load_data_commodities(request):
    try:
        call_command("load_commodities")
        messages.success(request,"Commodities loaded form JSON successfully.")

    except Exception as error:
        messages.error(request,f"Commodities load failed: {error}")

    return redirect("agro:index")

@login_required
@user_passes_test(is_admin)
@require_POST
def load_data_action_items(request):
    try:
        call_command("load_action_items")
        messages.success(request,"Action Items loaded form JSON successfully.")

    except Exception as error:
        messages.error(request,f"Action Items load failed: {error}")

    return redirect("agro:index")

@login_required
@user_passes_test(is_admin)
@require_POST
def load_data_drought_alerts(request):
    try:
        call_command("load_drought_alerts")
        messages.success(request,"Drought Alert Levels loaded form JSON successfully.")

    except Exception as error:
        messages.error(request,f"Drought Alert Levels load failed: {error}")

    return redirect("agro:index")

@login_required
@user_passes_test(is_admin)
@require_POST
def load_data_effects(request):
    try:
        call_command("load_effects")
        messages.success(request,"Effects loaded form JSON successfully.")

    except Exception as error:
        messages.error(request,f"Effects load failed: {error}")

    return redirect("agro:index")

@login_required
@user_passes_test(is_admin)
@require_POST
def load_data_addtional_info(request):
    try:
        call_command("load_additional_info")
        messages.success(request,"Additional Information loaded form JSON successfully.")

    except Exception as error:
        messages.error(request,f"Additional Information load failed: {error}")

    return redirect("agro:index")

#################### PEST RISK EFFECT ITEMS - TABLE ####################
def effect_items_list(request, id=None):
    
    page_name = "Effect Items"
    qs = PestRiskEffect.objects.all().order_by('commodity','effect_description')

    filterset = EffectItemFilter(request.GET, queryset=qs)

    table = EffectItemsTable(filterset.qs)
    table.empty_text = "No records available"

    RequestConfig(request, paginate={"per_page": 50}).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(PestRiskEffect, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': "Agriculture Services",
        'table': table,
        'filter':   filterset,
        'new_url': reverse('agro:effect_items_entry'),
        'list_url': reverse('agro:effect_items_list'),
        'back_url': reverse('agro:index'),
        'api_url':  reverse('effectitems-list'),
    }
    return render(request, 'pest-risk/parameters_table_list.html', context)

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
            messages.success(request,(f"Item created: saved_entry.effect_description"))
            return redirect('agro:effect_items_list', saved_entry.id)
    else:
        messages.error(request,f"Unable to update/create")
        form = EffectItemsForm(instance=entry)

    return render(request, 'pest-risk/parameters_entry_form.html', {
        'page_name':    page_name,
        'prev_page':    "Effect Items List",
        'new_url':      reverse('agro:effect_items_entry'),
        'back_url':     reverse('agro:effect_items_list'),
        'api_url':      reverse('effectitems-list'),
        'form':         form,
        'entry':        entry
    })

def effect_items_delete(request, id):
    
    entry = get_object_or_404(PestRiskEffect, id=id)
    
    page_name = "Effect Item Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('agro:effect_items_list')  # redirect anywhere you prefer

    return render(request, "pest-risk/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
    })

def duplicate_object_pest_risk_effect(obj):
    data = model_to_dict(obj)
    data.pop('id', None)
    data['effect_description'] = f"{obj.effect_description}"
    return obj.__class__.objects.create(**data)

def effect_items_duplicate_object(obj):
    new_obj = PestRiskEffect.objects.create(effect_description=obj.effect_description)
    return new_obj

def effect_items_entry_duplicate(request, id):
    obj     = get_object_or_404(PestRiskEffect, pk=id)
    new_obj = effect_items_duplicate_object(obj)
    return redirect('agro:effect_items_entry', new_obj.id)

#################### PEST RISK Additional Info ITEMS - TABLE ####################
def info_items_list(request, id=None):

    page_name = "Additional Info Items"
    qs = PestRiskInfo.objects.all().order_by('commodity__description','info_description')

    filterset = InfoItemFilter(request.GET, queryset=qs)

    table = InfoItemsTable(filterset.qs)
    table.empty_text = "No records available"

    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None

    if id is not None:
        entry = get_object_or_404(PestRiskInfo, id=id)

    context = {
        'id' :      id,
        'entry':    entry,  
        'page_name': page_name,
        'prev_page': "Agriculture Services",
        'table':    table,
        'filter':   filterset,
        'new_url':  reverse('agro:info_items_entry'),
        'back_url': reverse('agro:index'),
        'list_url': reverse('agro:effect_items_list'),
        #'api_url':  reverse('actionitems-list'),
    }
    return render(request, 'pest-risk/parameters_table_list.html', context)

def info_items_entry(request, id=None):

    page_name = "Action Items Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(PestRiskInfo, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = InfoItemsForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('agro:info_items_list', saved_entry.id)
    else:
        form = InfoItemsForm(instance=entry)

    return render(request, 'pest-risk/parameters_entry_form.html', {
        'page_name':    page_name,
        'prev_page':    "Action Items List",
        'new_url':      reverse('agro:action_items_entry'),
        'back_url':     reverse('agro:action_items_list'),
        'api_url':      reverse('actionitems-list'),
        'form':         form,
        'entry':        entry
    })

def info_items_delete(request, id):
    
    entry = get_object_or_404(PestRiskInfo, id=id)
    
    page_name = "Additional Info Item Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('agro:info_items_list')  # redirect anywhere you prefer

    return render(request, "pest-risk/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
    })

def info_items_duplicate_object(obj):
    new_obj = PestRiskInfo.objects.create(info_description=obj.info_description)
    return new_obj

def info_items_entry_duplicate(request, id):
    obj     = get_object_or_404(PestRiskInfo, pk=id)
    new_obj = info_items_duplicate_object(obj)
    return redirect('agro:info_items_entry', new_obj.id)

def duplicate_object_pest_risk_action(obj):
    data = model_to_dict(obj)
    data.pop('id', None)
    data['action_description'] = f"{obj.action_description}"
    return obj.__class__.objects.create(**data)

def action_items_entry_duplicate(request, id):
    obj = get_object_or_404(PestRiskAction, pk=id)
    duplicate_object_pest_risk_action(obj)
    return redirect('agro:action_items_list')




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
class SectorViewSet(viewsets.ModelViewSet):
   queryset = Sector.objects.all().order_by('id')
   serializer_class = SectorSerializer
   http_method_names = ['get', 'head','options']

class ZoneViewSet(viewsets.ModelViewSet):
   queryset = Zone.objects.all().order_by('id')
   serializer_class = ZoneSerializer
   http_method_names = ['get', 'head','options']

class DistrictViewSet(viewsets.ModelViewSet):
   queryset = District.objects.all().order_by('id')
   serializer_class = DistrictSerializer
   http_method_names = ['get', 'head','options']

class CommodityTypeViewSet(viewsets.ModelViewSet):
   queryset = Commodity.objects.all().order_by('id')
   serializer_class = CommodityCategorySerializer
   http_method_names = ['get', 'head','options']

class ActionItemsViewSet(viewsets.ModelViewSet):
   queryset = PestRiskAction.objects.all().order_by('id')
   serializer_class = ActionItemsSerializer
   http_method_names = ['get', 'head','options']

class EffectItemsViewSet(viewsets.ModelViewSet):
   queryset = PestRiskEffect.objects.all().order_by('id')
   serializer_class = EffectItemsSerializer
   http_method_names = ['get', 'head','options']

class DroughtAlertLevelViewSet(viewsets.ModelViewSet):
   queryset = DroughtAlertLevel.objects.all().order_by('id')
   serializer_class = DroughtAlertLevelSerializer
   http_method_names = ['get', 'head','options']   

class PestRiskEntryDetailsViewSet(viewsets.ModelViewSet):
   queryset = PestRiskEntryDetails.objects.filter(is_published=True).order_by('id')
   serializer_class = PestRiskEntryDetailsSerializer
   http_method_names = ['get', 'head','options']

class PestRiskViewSet(viewsets.ModelViewSet):
   queryset = PestRisk.objects.filter(id=1).prefetch_related(Prefetch(
                        "pest_risk_entries",
                        queryset=PestRiskEntryDetails.objects.filter(
                            is_published=True
                        ).select_related(
                            "commodity_id",
                            "district_id",
                            "pest_alert_lvl_id",
                            "drought_alert_lvl_id",
                            'updated_by',
                        ).prefetch_related(
                        'effect',
                        'info',
                        'actions',
                    ).order_by("id"),
                                    )
                                )
   serializer_class = PestRiskSerializer
   pagination_class = None
   http_method_names = ['get', 'head','options']