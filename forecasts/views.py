import calendar, io
import os
from django.contrib import messages
from sqlite3 import IntegrityError

from django.conf import settings as jsettings
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from django_tables2 import RequestConfig
from rest_framework import settings, status, viewsets

from reportlab.platypus import Image, SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from forecasts.forms import DistrictForecastDetailsForm, DistrictForecastForm, DistrictForecastInstructionsForm, DistrictForecastPublishForm, RiskLevelForm, SeverityForm, ProbabilityForm, DistrictForm, AlertLevelForm
from forecasts.tables import AlertLevelTable, DistrictForecastDetailsTable, DistrictForecastTable, RiskLevelTable, SeverityTable, ProbabilityTable, DistrictTable, InstructionsTable
from forecasts.models import AlertLevel, District, DistrictForecastDetails, RiskLevel, Severity, Probability, DistrictForecast, DistrictForecastInstructions

from . import serializers as sx

# Create your views here.
def index(request):
    context = {
        'page_name': 'Weather Forecasts',
    }
    return render(request, 'forecasts_home.html', context)

############# DISTRICT FORECASTS: District Entry #############
def district_list(request, id=None):
    page_name = "District Entries"
    qs = District.objects.all().order_by('id')
    table = DistrictTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(District, id=id)

    return render(request, 'district-forecast/parameters_table_list.html', {
        'id' : id, 
        'entry': entry, 
        'page_name': page_name,
        'prev_page': 'Weather Forecasts', 
        'table' : table,
        'new_url':  reverse('forecasts:district_entry'),
        'back_url': reverse('forecasts:index'),
        #'api_url': "/api/pest-risk/",
    })

def district_entry(request, id=None):

    page_name = "District Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(District, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = DistrictForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('forecasts:district_list', saved_entry.id)
    else:
        form = DistrictForm(instance=entry)

    return render(request, 'district-forecast/parameters_entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('forecasts:district_entry'),
        'back_url': reverse('forecasts:district_list'),
        #'api_url': reverse('zones-list'),
        'form': form,
        'entry': entry
    })

def district_delete(request, id):
    
    entry = get_object_or_404(District, id=id)

    qs = District.objects.all().order_by('id')
    # Filter details by parent listing
    qs = qs.order_by('id')
    
    page_name = "District Entry"

    if request.method == "POST":
        entry.delete()
        
        return redirect('forecasts:district_list')  # redirect anywhere you prefer

    return render(request, "district-forecast/parameters_delete_district.html", {
        "entry": entry,
        'page_name': page_name,
        'details': qs
    })

############# DISTRICT FORECATSTS: Alert Level Entry #############
def alert_level_list(request, id=None):
    page_name = "Alert Level Entries"
    qs = AlertLevel.objects.all().order_by('-id')
    table = AlertLevelTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    '''if id is not None:
        entry = get_object_or_404(PestRiskEntryMainListing, id=id)'''

    context = {
        'entry': entry,  
        'page_name': page_name,
        'prev_page': 'Weather Forecasts',
        'table': table,
        'new_url':  reverse('forecasts:alert_level_entry'),
        'back_url': reverse('forecasts:index'),
        #'api_url': "/api/pest-risk/",
    }
    return render(request, 'district-forecast/parameters_table_list.html', context)

def alert_level_entry(request, id=None):

    page_name = "Alert Level Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(AlertLevel, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = AlertLevelForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('forecasts:alert_level_list', saved_entry.id)
        
    else:
        #form = PestRiskMainListingForm(instance=entry)
        form = AlertLevelForm(instance=entry)

    return render(request, 'district-forecast/parameters_entry_form.html', {
        'page_name':    page_name,
        'new_url':      reverse('forecasts:alert_level_list'),
        'details_url':  "",
        #'back_url':     reverse('forecasts:alert_level_list'),
        'api_url':      "/api/pest-risk/",
        'form': form,
        'entry': entry
    })

def alert_level_delete(request, id):
    
    entry = get_object_or_404(AlertLevel, id=id)

    qs = AlertLevel.objects.all().order_by('id')
    # Filter details by parent listing
    qs = qs.order_by('id')
    
    page_name = "Alert Level Entry"

    if request.method == "POST":
        entry.delete()
        
        return redirect('forecasts:alert_level_list')  # redirect anywhere you prefer

    return render(request, "district-forecast/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'details': qs
    })

############# DISTRICT FORECATSTS: Risk Level Entry #############
def instructions_list(request, id=None):
    page_name = "Instructions Entries"
    qs = DistrictForecastInstructions.objects.all().order_by('-id')
    table = InstructionsTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    '''if id is not None:
        entry = get_object_or_404(PestRiskEntryMainListing, id=id)'''

    context = {
        #'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': 'District Forecast Instructions',
        'table': table,
        'new_url':  reverse('forecasts:instructions_entry'),
        'back_url': reverse('forecasts:index'),
        #'api_url': "/api/pest-risk/",
    }
    return render(request, 'district-forecast/parameters_table_list.html', context)

def instructions_entry(request, id=None):

    page_name = "Instructions Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(DistrictForecastInstructions, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = DistrictForecastInstructionsForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('forecasts:instructions_list', saved_entry.id)
        
    else:
        form = DistrictForecastInstructionsForm(instance=entry)

    return render(request, 'district-forecast/parameters_entry_form.html', {
        'page_name':    page_name,
        'new_url':      reverse('forecasts:instructions_list'),
        'details_url':  "",
        #'back_url':     reverse('forecasts:risk_level_list'),
        'api_url':      "/api/pest-risk/",
        'form': form,
        'entry': entry
    })

def instructions_delete(request, id):
    
    entry = get_object_or_404(DistrictForecastInstructions, id=id)

    qs = DistrictForecastInstructions.objects.all().order_by('id')
    # Filter details by parent listing
    qs = qs.order_by('id')
    
    page_name = "District Forecast Instructions Entry"

    if request.method == "POST":
        entry.delete()
        
        return redirect('forecasts:instructions_list')  # redirect anywhere you prefer

    return render(request, "district-forecast/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'details': qs
    })

@require_POST
def district_forecast_instructions_ajax_add(request):
    description = request.POST.get("description", "").strip()

    if not description:
        return JsonResponse({
            "success": False,
            "error": "Description is required."
        })

    item = DistrictForecastInstructions.objects.create(description=description)

    return JsonResponse({
        "success": True,
        "id": item.id,
        "description": str(item)
    })

############# DISTRICT FORECATSTS: Risk Level Entry #############
def risk_level_list(request, id=None):
    page_name = "Risk Level Entries"
    qs = RiskLevel.objects.all().order_by('-id')
    table = RiskLevelTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    '''if id is not None:
        entry = get_object_or_404(PestRiskEntryMainListing, id=id)'''

    context = {
        #'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': 'Weather Forecasts',
        'table': table,
        'new_url':  reverse('forecasts:risk_level_entry'),
        'back_url': reverse('forecasts:index'),
        #'api_url': "/api/pest-risk/",
    }
    return render(request, 'district-forecast/parameters_table_list.html', context)

def risk_level_entry(request, id=None):

    page_name = "Risk Level Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(RiskLevel, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = RiskLevelForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('forecasts:risk_level_list', saved_entry.id)
        
    else:
        #form = PestRiskMainListingForm(instance=entry)
        form = RiskLevelForm(instance=entry,initial={'months': True})

    return render(request, 'district-forecast/parameters_entry_form.html', {
        'page_name':    page_name,
        'new_url':      reverse('forecasts:risk_level_list'),
        'details_url':  "",
        #'back_url':     reverse('forecasts:risk_level_list'),
        'api_url':      "/api/pest-risk/",
        'form': form,
        'entry': entry
    })

def risk_level_delete(request, id):
    
    entry = get_object_or_404(RiskLevel, id=id)

    qs = RiskLevel.objects.all().order_by('id')
    # Filter details by parent listing
    qs = qs.order_by('id')
    
    page_name = "Risk Level Entry"

    if request.method == "POST":
        entry.delete()
        
        return redirect('forecasts:risk_level_list')  # redirect anywhere you prefer

    return render(request, "district-forecast/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'details': qs
    })

############# DISTRICT FORECASTS: Severity #############
def severity_list(request, id=None):
    page_name = "Severity Entries"
    qs = Severity.objects.all().order_by('-id')
    table = SeverityTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(Severity, id=id)

    
    return render(request, 'district-forecast/parameters_table_list.html', {
       'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': 'Weather Forecasts',
        'table': table,
        'new_url':  reverse('forecasts:severity_entry'),
        'back_url': reverse('forecasts:index'),
        #'api_url': "/api/pest-risk/",
    })

def severity_entry(request, id=None):

    page_name = "Severity Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(Severity, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = SeverityForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('forecasts:severity_list', saved_entry.id)
    else:
        form = SeverityForm(instance=entry)

    return render(request, 'district-forecast/parameters_entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('forecasts:severity_entry'),
        'back_url': reverse('forecasts:severity_list'),
        #'api_url': reverse('zones-list'),
        'form': form,
        'entry': entry
    })

def severity_delete(request, id):
    
    entry = get_object_or_404(Severity, id=id)

    qs = Severity.objects.all().order_by('id')
    # Filter details by parent listing
    qs = qs.order_by('id')
    
    page_name = "Severity Entry"

    if request.method == "POST":
        entry.delete()
        
        return redirect('forecasts:severity_list')  # redirect anywhere you prefer

    return render(request, "district-forecast/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'details': qs
    })

############# DISTRICT FORECASTS: Probability #############
def probability_list(request, id=None):
    page_name = "Probability Entries"
    qs = Probability.objects.all().order_by('-id')
    table = ProbabilityTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(Probability, id=id)

    
    return render(request, 'district-forecast/parameters_table_list.html', {
       'id' : id,
        'entry': entry,  
        'page_name': page_name,
        "prev_page": 'Weather Forecasts',
        'table': table,
        'new_url':  reverse('forecasts:probability_entry'),
        'back_url': reverse('forecasts:index'),
        #'api_url': "/api/pest-risk/",
    })

def probability_entry(request, id=None):

    page_name = "Probability Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(Probability, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = ProbabilityForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('forecasts:probability_list', saved_entry.id)
    else:
        form = ProbabilityForm(instance=entry)

    return render(request, 'district-forecast/parameters_entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('forecasts:probability_entry'),
        'back_url': reverse('forecasts:probability_list'),
        #'api_url': reverse('zones-list'),
        'form': form,
        'entry': entry
    })

def probability_delete(request, id):
    
    entry = get_object_or_404(Probability, id=id)

    qs = Probability.objects.all().order_by('id')
    # Filter details by parent listing
    qs = qs.order_by('id')
    
    page_name = "Probability Entry"

    if request.method == "POST":
        entry.delete()
        
        return redirect('forecasts:probability_list')  # redirect anywhere you prefer

    return render(request, "district-forecast/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'details': qs
    })

############# DISTRICT FORECASTS: Main Entries #############
def district_forecast_list(request, id=None):
    page_name = "District Level Forecasts"
    qs = DistrictForecast.objects.all().order_by('-id')
    table = DistrictForecastTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(DistrictForecast, id=id)

    return render(request, 'district-forecast/district_forecast_table_list_main.html', {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': 'Weather Forecasts',
        'table': table,
        'new_url':  reverse('forecasts:district_forecast_entry'),
        'back_url': reverse('forecasts:index'),
        #'api_url':  reverse('forecasts:district-forecast-list'),
    })

def district_forecast_entry(request, id=None):

    page_name = "District Forecast Entry"

    if id:
        entry = get_object_or_404(DistrictForecast, id=id)
    else:
        entry = None

    if request.method == 'POST':
        
        form = DistrictForecastForm(request.POST, instance=entry)

        '''is_new = entry is None'''

        if form.is_valid():

            saved_entry = form.save()

            districts = District.objects.all().order_by("id")[:6]

            for district in districts:
                DistrictForecastDetails.objects.get_or_create(
                    forecast=saved_entry,
                    district=district
                )
            return redirect('forecasts:district_forecast_details_entry', saved_entry.id)
        else:
            print(form.errors)  # shows what field failed validation  
    else:
        form = DistrictForecastForm(instance=entry)

    return render(request, 'district-forecast/entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('forecasts:district_forecast_entry'),
        'back_url': reverse('forecasts:district_forecast_list'),

        #'api_url': reverse('zones-list'),
        'form': form,
        'entry': entry
    })

def district_forecast_delete(request, id):
    
    entry = get_object_or_404(DistrictForecast, id=id)

    qs = DistrictForecast.objects.all().order_by('id')
    #qs = qs.order_by('id')
    
    page_name = "DELETE District Forecast Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('forecasts:district_forecast_list')  # redirect anywhere you prefer

    return render(request, "district-forecast/district_forecast_delete.html", {
        "entry": entry,
        'page_name': page_name,
        #'details': qs
    })

def district_forecast_toggle_is_published(request, id):
    record = get_object_or_404(DistrictForecast, id=id)

    if not record.is_published:
        # Unpublish ALL records first
        DistrictForecast.objects.filter(is_published=True).update(is_published=False)

        # Publish selected
        record.is_published = True
        status = "published"

    else:
        # If already published → unpublish it
        record.is_published = False
        status = "unpublished"

    record.save(update_fields=["is_published"])

    messages.success(request, f"Record {status} successfully.")
    return redirect("forecasts:district_forecast_list")

@require_POST
def district_forecast_toggle_is_published_ajax(request, id):
    record = get_object_or_404(DistrictForecast, id=id)

    is_published = request.POST.get("is_published") == "true"

    if is_published:
        DistrictForecast.objects.exclude(id=record.id).update(is_published=False)

    record.is_published = is_published
    record.save(update_fields=["is_published"])

    return JsonResponse({
        "success": True,
        "is_published": record.is_published
    })

############# DISTRICT FORECASTS: Details List #############
def district_forecast_details_list(request, id=None, fk=None):

    #print(fk);
    page_name = "District Forecast Entry"

    #qs = DistrictForecastDetails.objects.all().order_by('id')

    # Parent forecast
    parent_entry = get_object_or_404(DistrictForecast, id=id)

    # Get only details for this forecast
    qs = DistrictForecastDetails.objects.filter(forecast_id=id).order_by('id')
    table = DistrictForecastDetailsTable(qs)
    RequestConfig(request).configure(table)

    print("Forecast ID:", id)
    print("Details count:", qs.count())
    print(qs.query)

    '''if id is not None:
        entry = get_object_or_404(DistrictForecast, id=id)

        # Filter details by parent listing
        qs = qs.filter(forecast_id=fk)
        qs = qs.order_by('-id')'''

    #Child object (details)
    #entry = None
    
    #if id:
    #    entry = get_object_or_404(DistrictForecastDetails,id=id)

    return render(request, 'district-forecast/district_forecast_table_list_details.html', {
        'id' : id,
        #'fk': fk,
        'page_name': page_name,
        'table': table,
        #'entry': entry,
        'parent_entry': parent_entry,
        'new_url': reverse('forecasts:district_forecast_details_entry'),
        'back_url': reverse('forecasts:district_forecast_list'),
        'details_url': reverse('forecasts:district_forecast_details_entry', kwargs={'id': id}),
    })

def district_forecast_details_entry(request, id):

    page_name = "District Forecast Details"
    qs = DistrictForecastDetails.objects.filter(forecast_id=id).order_by('id')

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(DistrictForecast, id=id)
    else:
        entry = None

    table = DistrictForecastDetailsTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)
    
    if request.method == 'POST':
        form = DistrictForecastPublishForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('forecasts:district_forecast_details_entry', saved_entry.id)
    else:
        form = DistrictForecastPublishForm(instance=entry)

    return render(request, 'district-forecast/district_forecast_details_entry_table_form.html', {
        'page_name': page_name,
        'forecast_id': id,
        'new_url':  reverse('forecasts:district_forecast_entry'),
        'prev_page': 'District Forecasts',
        'back_url': reverse('forecasts:district_forecast_list'),
        #'details_url': reverse('forecasts:district_forecast_details_entry', kwargs={'id': id}),
        #'api_url': reverse('zones-list'),
        'form': form,
        'entry': entry,
        'table':    table,
    })

def district_forecast_details_entry_item(request, id=None, fk=None):

    page_name = "District Forecast Details Item"
    
    # If fk exists => update, else => create new
    if fk:
        main_entry = get_object_or_404(DistrictForecast, id=fk)
    else:
        main_entry = None
    
    # If id exists => update, else => create new
    if id:
        item_entry = get_object_or_404(DistrictForecastDetails, id=id, forecast_id=fk)
    else:
        item_entry = None

    if request.method == 'POST':
        form = DistrictForecastDetailsForm(request.POST, instance=item_entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates

            # Save & Close button
            if 'btn_submit_close' in request.POST:
                return redirect('forecasts:district_forecast_details_entry',fk)

            # Regular Save button
            return redirect('forecasts:district_forecast_details_entry_item',fk,saved_entry.id)
    else:
        form = DistrictForecastDetailsForm(instance=item_entry)

    return render(request, 'district-forecast/district_forecast_details_entry_form.html', {
        'page_name': page_name,
        'id': id,
        'forecast_id': fk,
        'main_entry': main_entry,
        'item_entry': item_entry,
        'form': form,
        'forecast_id': fk,
        'back_url': reverse('forecasts:district_forecast_details_entry', kwargs={'id': fk}),
    })

def generate_pdf(request, id=None):

    forecast = get_object_or_404(DistrictForecast, id=id)

    # Create a file-like buffer to receive PDF data
    #buffer = io.BytesIO()

    # Folder where PDF will be saved
    folder_path = os.path.join(jsettings.DOCS_ROOT, "District_Forecasts")
    os.makedirs(folder_path, exist_ok=True)

    # Full PDF file path
    filename = f"District_Forecast_{forecast.forecast_date}.pdf"
    file_path = os.path.join(folder_path, filename)

    letterhead = Image("static/images/letterhead/nms_wafs.png")
    letterhead.drawHeight = 2 * inch
    letterhead.drawWidth = 8.5 * inch

    # Create PDF directly on server
    #p = canvas.Canvas(file_path, pagesize=letter)

    doc = SimpleDocTemplate(
        file_path, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elements = []

    


    '''p = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter

    details = DistrictForecastDetails.objects.filter(
        forecast=forecast
    ).select_related(
        "district",
        "prob_temp_min", "sev_temp_min", "ins_temp_min",
        "prob_temp_max", "sev_temp_max", "ins_temp_max",
        "prob_precip_max", "sev_precip_max", "ins_precip_max",
        "prob_winds", "sev_winds", "ins_winds",
        "prob_weather_conditions", "sev_weather_conditions", "ins_weather_conditions",
    ).order_by("district__district_name")

     # Header
    p.setFont("Helvetica-Bold", 22)
    p.drawString(0.75 * inch, height - 1 * inch, "District Forecast")

    p.setFont("Helvetica", 13)
    p.drawString(0.75 * inch, height - 1.3 * inch, f"Forecast Date: {forecast.forecast_date}")
    #p.drawString(1 * inch, height - 1.5 * inch, f"Published: {'Yes' if forecast.is_published else 'No'}")

    # Table headings
    y = height - 2 * inch

    p.setFont("Helvetica-Bold", 11)
    p.drawString(0.75 * inch, y, "DISTRICT")
    p.drawString(2 * inch, y, "TEMP (MIN)")
    p.drawString(3 * inch, y, "TEMP (MAX)")
    p.drawString(4 * inch, y, "RAINFALL")
    p.drawString(5 * inch, y, "WIND")
    p.drawString(6.0 * inch, y, "WEATHER CONDITIONS")

    y -= 0.25 * inch
    p.setFont("Helvetica", 9)

    for item in details:
        if y < 60:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 9)

        district = item.district.district_name if item.district else "N/A"
        temp_min = f"{item.temp_min:.1f} °F" if item.temp_min is not None else ""
        temp_max = f"{item.temp_max:.1f} °F" if item.temp_max is not None else ""
        precip = f"{item.precip_max:.1f} in" if item.precip_max is not None else ""
       
        winds = ""
        if item.winds_min is not None and item.winds_max is not None:
            winds = f"{item.winds_min:.1f}-{item.winds_max:.1f} mph"

        conditions = item.weather_conditions or ""

        p.setFont("Helvetica-Bold", 9)
        p.drawString(55, y, district)

        p.setFont("Helvetica", 9)
        p.drawString(145, y, temp_min)
        p.drawString(215, y, temp_max)
        p.drawString(290, y, precip)
        p.drawString(360, y, winds)
        p.drawString(430, y, conditions[:25])

        y -= 18

    p.showPage()
    p.save()

    buffer.seek(0)'''

    details = DistrictForecastDetails.objects.filter(
        forecast=forecast
    ).select_related("district").order_by("district__district_name")

    data = [
        ["DISTRICT","TEMP (MIN)","TEMP (MAX)","RAINFALL","WIND","WEATHER CONDITIONS"]
    ]

    for item in details:
        wind = ""
        if item.winds_min is not None and item.winds_max is not None:
            wind = f"{item.winds_min:.1f} - {item.winds_max:.1f} mph"

        data.append([
            item.district.district_name if item.district else "",
            f"{item.temp_min:.1f} °F" if item.temp_min is not None else "",
            f"{item.temp_max:.1f} °F" if item.temp_max is not None else "",
            f"{item.precip_max:.1f} in" if item.precip_max is not None else "",
            wind,
            item.weather_conditions or "",
        ])

    table = Table(
        data,
        colWidths=[
            1.5 * inch,
            1.0 * inch,
            1.0 * inch,
            1.0 * inch,
            1.3 * inch,
            3.5 * inch,
        ],
        repeatRows=1
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (1, 1), (4, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    elements.append(letterhead)
    elements.append(Paragraph("District Level Forecast",styles["Title"]))
    elements.append(Paragraph(f"Forecast Date: {forecast.forecast_date}", styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Forecaster: {forecast.created_by}", styles["Normal"]))

    doc.build(elements)

    #buffer.seek(0)

    # Display in browser
    '''return FileResponse(
        buffer,
        content_type='application/pdf'
    )'''

    # Return saved PDF as download
    return FileResponse(
        open(file_path, "rb"),
        as_attachment=False,
        filename=filename
    )

class DistrictForecastDetailsViewSet(viewsets.ModelViewSet):
   queryset = DistrictForecastDetails.objects.all().order_by('id')
   serializer_class = sx.DistrictForecastDetailsSerializer

class DistrictForecastAllViewSet(viewsets.ModelViewSet):
    queryset = DistrictForecast.objects.all().order_by("-forecast_date").prefetch_related("district_forecast_details")
    serializer_class = sx.DistrictForecastSerializer
    pagination_class = None

class DistrictForecastViewSet(viewsets.ModelViewSet):
   queryset = DistrictForecast.objects.filter(is_published=True).prefetch_related("district_forecast_details")
   serializer_class = sx.DistrictForecastSerializer
   pagination_class = None