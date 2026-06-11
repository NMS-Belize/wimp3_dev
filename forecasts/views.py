import calendar, io
import os
from click import style
from click import style
from django.contrib import messages
from sqlite3 import IntegrityError

from django.conf import settings as jsettings
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from django_tables2 import RequestConfig
from reportlab.lib import styles
from rest_framework import settings, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


from forecasts.forms import DistrictForecastDetailsForm, DistrictForecastForm, DistrictForecastInstructionsForm, DistrictForecastPublishForm, RiskLevelForm, SeverityForm, ProbabilityForm, DistrictForm, AlertLevelForm
from forecasts.tables import AlertLevelTable, DistrictForecastDetailsTable, DistrictForecastTable, RiskLevelTable, SeverityTable, ProbabilityTable, DistrictTable, InstructionsTable
from forecasts.models import AlertLevel, District, DistrictForecastDetails, RiskLevel, Severity, Probability, DistrictForecast, DistrictForecastInstructions

from . import serializers as sx

PAGE_WIDTH, PAGE_HEIGHT = letter

pdfmetrics.registerFont(TTFont("OpenSans-Regular","static/fonts/OpenSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans-Light","static/fonts/OpenSans-Light.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans-SemiBold","static/fonts/OpenSans-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans-Bold","static/fonts/OpenSans-Bold.ttf"))

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

        if form.is_valid():

            saved_entry = form.save(commit=False)

            # New record only
            if entry is None:
                saved_entry.created_by = request.user

            # Every save/update
            saved_entry.updated_by = request.user

            # IMPORTANT: save before using in ForeignKey queries
            saved_entry.save()

            # If your form has many-to-many fields
            form.save_m2m()

            districts = District.objects.all().order_by("id")[:6]

            for district in districts:
                DistrictForecastDetails.objects.get_or_create(
                    forecast=saved_entry,
                    district=district
                )

            return redirect(
                'forecasts:district_forecast_details_entry',
                saved_entry.id
            )

        else:
            print(form.errors)

    else:
        form = DistrictForecastForm(instance=entry)

    return render(request, 'district-forecast/entry_form.html', {
        'page_name': page_name,
        'new_url': reverse('forecasts:district_forecast_entry'),
        'back_url': reverse('forecasts:district_forecast_list'),
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

def add_background_wafs_full(canvas, doc):
    canvas.saveState()
    canvas.drawImage("static/images/letterhead/nms_wafs_full.jpg",0,0,width=PAGE_WIDTH,height=PAGE_HEIGHT,preserveAspectRatio=False,mask='auto')
    canvas.restoreState()

def add_background_climat_full(canvas, doc):
    canvas.saveState()
    canvas.drawImage("static/images/letterhead/nms_clim_full.jpg",0,0,width=PAGE_WIDTH,height=PAGE_HEIGHT,preserveAspectRatio=False,mask='auto')
    canvas.restoreState()

def get_risk_color(level):
    if not level:
        return "#000000"

    if level == 1:
        return "#3CAEA3"      # Green
    elif level == 2:
        return "#FCBF49"      # Amber
    elif level == 3:
        return "#fd7e14"      # Orange
    elif level == 4:
        return "#D62828"      # Red

    return "#000000"

def generate_pdf(request, id=None):

    forecast = get_object_or_404(DistrictForecast, id=id)

    # Create a file-like buffer to receive PDF data
    #buffer = io.BytesIO()

    # Folder where PDF will be saved
    folder_path = os.path.join(jsettings.DOCS_ROOT, "District_Forecasts")
    os.makedirs(folder_path, exist_ok=True)

    # Full PDF file path
    filename = f"District_Forecast_NMS_BZ_{forecast.forecast_date}.pdf"
    file_path = os.path.join(folder_path, filename)

    doc = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=0.5 * inch, rightMargin=0.5 * inch, topMargin=2 * inch, bottomMargin=0.5 * inch)

    styles = getSampleStyleSheet()
    elements = []

    main_title  = ParagraphStyle("MainTitle",   parent = styles["Title"],   fontName = "OpenSans-SemiBold", fontSize = 22, leading = 26, alignment = TA_LEFT, textColor = "#00537A", spaceAfter = 10)
    sub_title   = ParagraphStyle("SubTitle",    parent = styles["Title"],   fontName = "OpenSans-Bold",     fontSize = 10, leading = 14, alignment = TA_LEFT, textColor = "#000000", spaceAfter = 10)
    main_text   = ParagraphStyle("MainText",    parent = styles["Normal"],  fontName = "OpenSans-Regular",  fontSize = 10, leading = 18, alignment = TA_LEFT, textColor = "#000000", spaceAfter = 6)
    foot_text   = ParagraphStyle("FootText",    parent = styles["Normal"],  fontName = "OpenSans-Regular",  fontSize = 8, leading = 12, alignment = TA_LEFT, textColor = "#000000", spaceAfter = 2)
    table_head  = ParagraphStyle("TableHeader", parent = styles["Normal"],  fontName = "OpenSans-Bold",     fontSize = 9, leading = 9, spaceAfter = 10 )
    table_first = ParagraphStyle("TableCol1",   parent = styles["Normal"],  fontName="OpenSans-Bold",       fontSize = 10 )
    table_body  = ParagraphStyle("TableBody",   parent = styles["Normal"],  fontName = "OpenSans-Regular",  fontSize = 10, leading = 12, spaceAfter = 0 )
    risk_text   = ParagraphStyle("RiskText",    parent = styles["Normal"],  fontName = "OpenSans-Bold",     fontSize = 10, spaceAfter = 40 )

    details = DistrictForecastDetails.objects.filter(forecast=forecast).select_related("district").order_by("district__district_name")

    data = [[
        Paragraph("DISTRICT", table_head),
        Paragraph("WEATHER CONDITIONS", table_head),
        Paragraph("TEMP<br/><font size='8'>(MIN)</font>", table_head),
        Paragraph("TEMP<br/><font size='8'>(MAX)</font>", table_head),
        Paragraph("RAINFALL<br/><font size='8'>(24HR)</font>", table_head),
        Paragraph("WINDS", table_head),
    ]]

    for item in details:
        wind = ""
        if item.winds_min is not None and item.winds_max is not None:
            wind = f"{item.winds_min}-{item.winds_max} kts"
        
        weather_prob    = item.prob_weather_conditions.description.upper() if item.prob_weather_conditions else ""
        temp_min_prob   = item.prob_temp_min.description.upper() if item.prob_temp_min else ""
        temp_max_prob   = item.prob_temp_max.description.upper() if item.prob_temp_max else ""
        precip_prob     = item.prob_precip_max.description.upper() if item.prob_precip_max else ""
        wind_prob       = item.prob_winds.description.upper() if item.prob_winds else ""

        weather_color   = get_risk_color(item.prob_weather_conditions_id)
        temp_min_color  = get_risk_color(item.prob_temp_min_id)
        temp_max_color  = get_risk_color(item.prob_temp_max_id)
        precip_color    = get_risk_color(item.prob_precip_max_id)
        wind_color      = get_risk_color(item.prob_winds_id)

        weather_text    = item.weather_conditions or ""
        temp_min_text   = f"{item.temp_min}°F" if item.temp_min is not None else ""
        temp_max_text   = f"{item.temp_max}°F" if item.temp_max is not None else ""
        precip_text     = f"{item.precip_max:.1f} in" if item.precip_max is not None else ""
        wind_text       = wind
        
        if weather_prob:
            weather_prob_text = (f"<font size='8' color='{weather_color}'>{weather_prob}</font>")

        if temp_min_prob:
            temp_min_prob_text = (f"<font size='8' color='{temp_min_color}'>{temp_min_prob}</font>")

        if temp_max_prob:
            temp_max_prob_text = (f"<font size='8' color='{temp_max_color}'>{temp_max_prob}</font>")

        if precip_prob:
            precip_prob_text = (f"<font size='8' color='{precip_color}'>{precip_prob}</font>")
        
        if wind_prob:
            wind_prob_text = (f"<font size='8' color='{wind_color}'>{wind_prob}</font>")

        data.append([
            Paragraph(item.district.district_name if item.district else "", table_first),
            Paragraph(weather_text, table_body),
            Paragraph(temp_min_text, table_body),
            Paragraph(temp_max_text, table_body),
            Paragraph(precip_text, table_body),
            Paragraph(wind_text, table_body),
        ])
        data.append([
            Paragraph("<font color='#000000' size='8'>Risk Level: </font>", table_body),
            Paragraph(weather_prob_text, risk_text),
            Paragraph(temp_min_prob_text, risk_text),
            Paragraph(temp_max_prob_text, risk_text),
            Paragraph(precip_prob_text, risk_text),
            Paragraph(wind_prob_text, risk_text),
        ])

    available_width = doc.width

    table = Table(
        data,
        colWidths=[
            available_width * 0.15,
            available_width * 0.38,
            available_width * 0.10,
            available_width * 0.10,
            available_width * 0.12,
            available_width * 0.15,
        ],
        repeatRows = 1
    )

    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#b2d9d0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (1, 1), (4, -1), "CENTER"),
        #("VALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),

        ("ALIGN", (0, 1), (-1, -1), "LEFT"),
        
        # Data rows
        ("VALIGN", (0, 1), (-1, -1), "TOP"),
        #("GRID", (0, 0), (-1, -1), 0.5, colors.white),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ])

    for row in range(2, len(data), 2):
        style.add("LINEBELOW",(0, row),(-1, row),0.5, colors.HexColor("#b2d9d0"))
    
    table.setStyle(style)

    forecaster = ""
    if forecast.created_by:
        forecaster = forecast.created_by.get_full_name() or forecast.created_by.username

    elements.append(Paragraph("District Level Forecast", main_title))
    elements.append(Paragraph(f"Forecast Date: {forecast.forecast_date.strftime('%B %d, %Y')}", sub_title))
    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Forecaster: {forecaster}", foot_text))
    elements.append(Paragraph(f"Date Created: {forecast.created_datetime.strftime('%B %d, %Y | %I:%M %p')}; Last Updated: {forecast.updated_datetime.strftime('%B %d, %Y | %I:%M %p')}", foot_text))

    doc.build(elements,
        onFirstPage=add_background_wafs_full,
        onLaterPages=add_background_wafs_full
    )
    available_width = doc.width

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = DistrictForecast.objects.filter(is_published=True).prefetch_related("district_forecast_details")
    serializer_class = sx.DistrictForecastSerializer
    pagination_class = None