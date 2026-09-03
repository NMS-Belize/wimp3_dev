from multiprocessing import context
from pyexpat.errors import messages
from django.contrib import messages

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
from django_tables2 import RequestConfig

from django.contrib.auth.decorators import login_required, permission_required
from requests import request

#from alerts.utils.cap_rss import fetch_cap_alerts
from wimp import serializers

#from .forms import *
from .models import CAPAlerts, CAPAlertDetails, TropicalWeatherAlerts, TropicalWeatherAlertsCategory
from .tables import CAPAlertsTable, TropicalWeatherALertsCategoryTable, TropicalWeatherALertsTable
from .forms import TropicalWeatherAlertsCategoryForm, TropicalWeatherAlertsForm
from .serializers import  CAPAlertsSerializer, CAPAlertDetailsSerializer, CAPAlertsAllSerializer, TropicalAlertsSerializer, TropicalAlertsCategoriesSerializer

from rest_framework import viewsets

def index(request):
    context = {
        'page_name': "Alerts Dashboard",
    }
    return render(request, 'alerts_home.html', context)

def cap_alerts_list(request, id=None):

    page_name   = "CAP Alerts List"
    qs          = CAPAlerts.objects.all().order_by(
                        "-details__expires",
                        "-pubdate"
                    )
    table       = CAPAlertsTable(qs)

    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    
    if id is not None:
        entry = get_object_or_404(CAPAlerts, guid=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': "Alerts Dashboard",
        'table': table,
        'new_url': reverse('alerts:cap_alerts_import'),
        'back_url': reverse('alerts:index'),
        'api_url': reverse('cap-list'),
    }
    return render(request, 'cap_list_template.html', context)

def cap_alerts_import(request, id=None):
    try:
        # Run the fetch function
        fetch_cap_alerts()
        messages.success(request, "CAP alerts fetched successfully!")
    except Exception as e:
        # Ensure we pass a string to messages
        messages.error(request, f"Failed to fetch CAP alerts: {str(e)}")

    return redirect("alerts:cap_alerts_list")

def cap_alerts_details(request, id=None):

    main_entry = None
    entry_details = None

    if id is not None:
        main_entry   = get_object_or_404(CAPAlerts, id=id)
        guid = main_entry.guid

        entry_details = CAPAlertDetails.objects.filter(identifier=main_entry.guid).first()

    context = {
        'page_name': "CAP Alerts Details",
        'prev_page': 'CAP Alerts List',
        'main_entry': main_entry,
        'entry_details': entry_details,
        'back_url': reverse('alerts:cap_alerts_list'),
    }
    return render(request, 'cap/table_list_details.html', context)

def cap_alert_toggle_is_published(request, id):

    record = get_object_or_404(CAPAlerts, id=id)
    record.is_published = not record.is_published
    record.save(update_fields=["is_published"])

    status = "published" if record.is_published else "unpublished"
    messages.success(request, f"Record {status} successfully.")

    return redirect("alerts:cap_alerts_list")

def tropical_alerts_category_list(request, id=None):

    page_name = "Tropical Weather Alerts Categories"
    qs = TropicalWeatherAlertsCategory.objects.all().order_by('id')
    table = TropicalWeatherALertsCategoryTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None

    context = {
        'entry': entry,  
        'page_name': page_name,
        'prev_page': 'Alerts Dashboard',
        'table': table,
        'new_url':  reverse('alerts:tropical_alerts_category_entry'),
        'back_url': reverse('alerts:index'),
    }
    return render(request, 'tropical-alerts/parameters_table_list.html', context)

@login_required
def tropical_alerts_category_entry(request, id=None):

    page_name = "Instructions Entry"

    if id:
        entry = get_object_or_404(TropicalWeatherAlertsCategory, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = TropicalWeatherAlertsCategoryForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save(commit=False)

            # New record only
            if entry is None:
                saved_entry.created_by = request.user

            # New and updated records
            saved_entry.updated_by = request.user
            saved_entry.save()
            return redirect('alerts:tropical_alerts_category_list', saved_entry.id)
        
    else:
        form = TropicalWeatherAlertsCategoryForm(instance=entry)

    return render(request, 'tropical-alerts/parameters_entry_form.html', {
        'page_name':    page_name,
        'prev_page':    'District Forecast Instructions',
        'new_url':      reverse('alerts:tropical_alerts_category_list'),
        'details_url':  "",
        'back_url':     reverse('alerts:tropical_alerts_category_list'),
        #'api_url':      "/api/pest-risk/",
        'form': form,
        'entry': entry
    })

def tropical_alerts_category_delete(request, id):

    entry = get_object_or_404(TropicalWeatherAlertsCategory, id=id)
    
    qs = TropicalWeatherAlertsCategory.objects.all().order_by('id')
    qs = qs.order_by('id')
    
    page_name = "Tropical Weather Alert Category Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('alerts:tropical_alerts_category_list')  # redirect anywhere you prefer

    return render(request, "tropical-alerts/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('alerts:tropical_alerts_category_list'),
        'details': qs
    })

def tropical_alerts_list(request, id=None):

    page_name = "Tropical Weather Alerts"
    qs = TropicalWeatherAlerts.objects.all().order_by('id')
    table = TropicalWeatherALertsTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None

    context = {
        #'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': 'Alerts Dashboard',
        'table': table,
        'new_url':  reverse('alerts:tropical_alerts_entry'),
        'back_url': reverse('alerts:index'),
        #'api_url': "/api/pest-risk/",
    }
    return render(request, 'tropical-alerts/parameters_table_list.html', context)

@login_required
def tropical_alerts_entry(request, id=None):

    page_name = "Tropical Weather Alert Entry"

    if id:
        entry = get_object_or_404(TropicalWeatherAlerts, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = TropicalWeatherAlertsForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save(commit=False)

            # New record only
            if entry is None:
                saved_entry.created_by = request.user

            # New and updated records
            saved_entry.updated_by = request.user
            saved_entry.save()
            return redirect('alerts:tropical_alerts_list', saved_entry.id)
        
    else:
        form = TropicalWeatherAlertsForm(instance=entry)

    return render(request, 'tropical-alerts/parameters_entry_form.html', {
        'page_name':    page_name,
        'prev_page':    'Tropical Weather Alerts',
        'new_url':      reverse('alerts:tropical_alerts_list'),
        'back_url':     reverse('alerts:tropical_alerts_list'),
        #'api_url':      "/api/pest-risk/",
        'form': form
    })

def tropical_alerts_delete(request, id):
    entry = get_object_or_404(TropicalWeatherAlerts, id=id)
    
    qs = TropicalWeatherAlerts.objects.all().order_by('id')
    qs = qs.order_by('id')
    
    page_name = "District Forecast Instructions Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('alerts:tropical_alerts_list')  # redirect anywhere you prefer

    return render(request, "tropical-alerts/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('alerts:tropical_alerts_list'),
        'details': qs
    })

def tropical_alerts_toggle_is_published(request, id):

    record = get_object_or_404(TropicalWeatherAlerts, id=id)
    record.is_published = not record.is_published
    record.save(update_fields=["is_published"])

    status = "published" if record.is_published else "unpublished"
    messages.success(request, f"Record {status} successfully.")

    return redirect("alerts:tropical_alerts_list")

#API endpoint that allows groups to be viewed or edited.
class CAPAlertsAllViewSet(viewsets.ModelViewSet):
   queryset = CAPAlerts.objects.all()
   serializer_class = CAPAlertsAllSerializer
   http_method_names = ['get', 'head','options']

class CAPAlertsViewSet(viewsets.ModelViewSet):
   queryset = CAPAlerts.objects.filter(is_published=True)
   serializer_class = CAPAlertsSerializer
   http_method_names = ['get', 'head','options']

class CAPAlertDetailsViewSet(viewsets.ModelViewSet):
   queryset = CAPAlertDetails.objects.all()
   serializer_class = CAPAlertDetailsSerializer
   http_method_names = ['get', 'head','options']