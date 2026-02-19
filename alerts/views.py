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

from alerts.utils.cap_rss import fetch_cap_alerts
from wimp import serializers

#from .forms import *
from .models import CAPAlerts, CAPAlertDetails
from .tables import CAPAlertsTable, CAPAlertsDetailsTable

from . import serializers as sx
from rest_framework import viewsets

def index(request):
    
    if not request.user.has_perm("alerts.view_capalerts"):
        return render(request, 'no_permission.html')
    
    template = loader.get_template('alerts_home.html')
    context = {'name': 'World'}  # Data to pass to the template
    return HttpResponse(template.render(context))

def cap_alerts_list(request, id=None):

    page_name   = "CAP Alerts List"
    qs          = CAPAlerts.objects.all().order_by('guid')
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
        'table': table,
        'new_url': reverse('alerts:cap_alerts_import')
        #'api_url': reverse('alerts:capalerts-list'),
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

def cap_alerts_details(request, guid=None):

    if guid is not None:
        entry   = get_object_or_404(CAPAlerts, guid=guid)
        qs      = CAPAlertDetails.objects.filter(identifier=guid)
        data    = data = qs.values().first()

        entry_details = JsonResponse(data, safe=False)
        
        #table = CAPAlertsDetailsTable(qs)
        #RequestConfig(request).configure(table)

    context = {
        #'table': table,
        'page_name': "CAP Alerts Details",
        'entry_details': entry_details,
    }
    return render(request, 'cap_details_template.html', context)

def cap_alert_toggle_is_published(request, id):
    record = get_object_or_404(CAPAlerts, id=id)

    record.is_published = not record.is_published
    record.save(update_fields=["is_published"])

    status = "published" if record.is_published else "unpublished"
    messages.success(request, f"Record {status} successfully.")

    return redirect("agro:pest_risk_list")

#API endpoint that allows groups to be viewed or edited.
class CAPAlertsViewSet(viewsets.ModelViewSet):
   queryset = CAPAlerts.objects.all()
   serializer_class = sx.CAPAlertsSerializer

class CAPAlertDetailsViewSet(viewsets.ModelViewSet):
   queryset = CAPAlertDetails.objects.all()
   serializer_class = sx.CAPAlertDetailsSerializer