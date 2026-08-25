import os, json
from click import style

from django.conf import settings
from django.contrib import messages
from django.core.management import call_command
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from django_tables2 import RequestConfig
from reportlab.lib import styles
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from forecasts.forms import DistrictForecastDetailsForm, DistrictForecastForm, DistrictForecastInstructionsCategoryForm, DistrictForecastInstructionsForm, DistrictForecastPublishForm, SeverityForm, ProbabilityForm, GeneralForecastCategoryForm, ForecastGeneralForm
from forecasts.tables import DistrictForecastDetailsTable, DistrictForecastTable, InstructionsCategoryTable, SeverityTable, ProbabilityTable, InstructionsTable, ForecastGeneralTable, ForecastGeneralCategoryTable
from forecasts.models import (
    ForecastGeneral, ForescastGeneralCategory, WindDirection, WindCondition, SeaState,
    DistrictForecast, DistrictForecastInstructions, DistrictForecastDetails, DistrictForecastInstructionsCategory, 
    Severity, Probability
)

from forecasts.filters import ForecastGeneralFilter
from system_core.models import District

from forecasts.serializers import DistrictForecastSerializer, DistrictForecastDetailsSerializer, GeneralForecastSerializer

PAGE_WIDTH, PAGE_HEIGHT = letter

pdfmetrics.registerFont(TTFont("OpenSans-Regular","static/fonts/OpenSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans-Light","static/fonts/OpenSans-Light.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans-SemiBold","static/fonts/OpenSans-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("OpenSans-Bold","static/fonts/OpenSans-Bold.ttf"))

def index(request):
    context = {
        'page_name': 'Weather Forecasts',
    }
    return render(request, 'forecasts_home.html', context)

############# GENERAL WEATHER FORECASTS: Main Entries #############
def general_forecast_list(request, id=None):
    page_name = "General Weather Forecasts"
    qs = ForecastGeneral.objects.all().order_by('forecast_date', 'forecast_time')

    filterset = ForecastGeneralFilter(request.GET, queryset=qs)
        
    table = ForecastGeneralTable(filterset.qs)    
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(ForecastGeneral, id=id)

    return render(request, 'general-weather-forecast/table_list_main.html', {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': 'Weather Forecasts',
        'table': table,
        "filter": filterset,
        'new_url':  reverse('forecasts:district_forecast_entry'),
        'back_url': reverse('forecasts:index'),
        'webpage_url': "forecast/general-weather-forecast/",
        'api_url':  reverse('general-weather-forecast-list'),
    })

def general_forecast_entry(request, id=None):

    page_name = "General Forecast Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(ForecastGeneral, id=id)
    else:
        entry = None

    previous_entry  = (ForecastGeneral.objects.filter(id__lt=entry.id).order_by('-id').first())
    next_entry      = (ForecastGeneral.objects.filter(id__gt=entry.id).order_by('id').first())

    audio_url = None

    # 1. Current FileField upload
    if entry.audio_file:
        try:
            if os.path.exists(entry.audio_file.path):
                audio_url = entry.audio_file.url
        except (ValueError, OSError):
            pass

    # 2. Check legacy/pre-stored audio file
    if not audio_url and entry.forecast_date and entry.forecast_time:

        legacy_filename = (f"{entry.forecast_date}_{entry.forecast_time.strftime('%H%M_%p')}_NMS_BZ.mp3")

        legacy_path = os.path.join(settings.MEDIA_ROOT, "forecast", "general", "audio", legacy_filename)

        if os.path.exists(legacy_path):
            audio_url = (f"{settings.MEDIA_URL}forecast/general/audio/{legacy_filename}")

    if request.method == 'POST':
        form = ForecastGeneralForm(request.POST, request.FILES, instance=entry)

        if form.is_valid():
            saved_entry = form.save(commit=False)
            saved_entry.save()
            form.save_m2m()
            messages.success(request, "Forecast Deatils saved successfully.")
        
            return redirect('forecasts:general_forecast_list', saved_entry.id)
        else:
            messages.error(request, f"Form could not be saved: {form.errors.as_text()}")

    else:
        form = ForecastGeneralForm(instance=entry)

    return render(request, 'general-weather-forecast/entry_form.html', {
        'page_name':    page_name,
        'prev_page':    'General Weather Forecast',
        'new_url':      reverse('forecasts:general_forecast_list'),
        'back_url':     reverse('forecasts:general_forecast_list'),
        'form': form,
        'entry': entry,
        "audio_url": audio_url,
        'previous_entry': previous_entry,
        'next_entry': next_entry,
    })

############# GENERAL FORECASTS: Category #############
def general_forecast_category_list(request, id=None):
    page_name = "General Forecast Categories"
    qs = ForescastGeneralCategory.objects.all().order_by('id')

    table = ForecastGeneralCategoryTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None

    context = {
        #'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': 'Weather Forecasts',
        'table': table,
        'new_url':  reverse('forecasts:general_forecast_category_entry'),
        'back_url': reverse('forecasts:index'),
        #'api_url': "/api/pest-risk/",
    }
    return render(request, 'district-forecast/parameters_table_list.html', context)

def general_forecast_category_entry(request, id=None):

    page_name = "General Forecast Category Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(ForescastGeneralCategory, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = GeneralForecastCategoryForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('forecasts:general_forecast_category_list', saved_entry.id)
        
    else:
        form = GeneralForecastCategoryForm(instance=entry)

    return render(request, 'district-forecast/parameters_entry_form.html', {
        'page_name':    page_name,
        'prev_page':    'General Weather Forecast Categories',
        'new_url':      reverse('forecasts:general_forecast_category_entry'),
        'details_url':  "",
        'back_url':     reverse('forecasts:general_forecast_category_list'),
        'form': form,
        'entry': entry
    })

def general_forecast_category_delete(request, id):
    
    entry = get_object_or_404(ForescastGeneralCategory, id=id)

    qs = ForescastGeneralCategory.objects.all().order_by('id')
    qs = qs.order_by('id')
    
    page_name = "General Forecast Categories Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('forecasts:general_forecast_category_list')  # redirect anywhere you prefer

    return render(request, "district-forecast/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('forecasts:general_forecast_category_list'),
        'details': qs
    })

def general_forecast_generate_pdf(request, id=None):

    forecast = get_object_or_404(ForecastGeneral, id=id)
    print(forecast.wind_direction_m2m)

    # Folder where PDF will be saved
    folder_path = os.path.join(settings.MEDIA_ROOT, "forecast", "general", "doc", "test")
    os.makedirs(folder_path, exist_ok=True)

    # Full PDF file path
    filename = f"General_Waether_Forecast_{forecast.forecast_date}_{forecast.forecast_time}_NMS_BZ.pdf"
    file_path = os.path.join(folder_path, filename)

    doc = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=0.5 * inch, rightMargin=0.5 * inch, topMargin=1.8 * inch, bottomMargin=0.5 * inch)

    styles = getSampleStyleSheet()
    elements = []

    main_title  = ParagraphStyle("MainTitle",   parent = styles["Title"],   fontName = "OpenSans-SemiBold", fontSize = 14, leading = 20, alignment = TA_LEFT, textColor = "#00537A", spaceAfter = 4)
    date_title   = ParagraphStyle("SubTitle",    parent = styles["Title"],   fontName = "OpenSans-Bold",     fontSize = 10, leading = 10, alignment = TA_RIGHT, textColor = "#235558", spaceAfter = 0)

    sub_title   = ParagraphStyle("SubTitle",    parent = styles["Title"],   fontName = "OpenSans-Bold",     fontSize = 10, leading = 14, alignment = TA_LEFT, textColor = "#000000", spaceAfter = 2)

    # ALERT TITLES
    alert_title     = ParagraphStyle("SubTitle",    parent = styles["Title"],   fontName = "OpenSans-Bold",     fontSize = 10, leading = 16, alignment = TA_LEFT, backColor=colors.HexColor("#f8e5e5"), textColor = "#82312f", spaceAfter = 2)
    talert_title    = ParagraphStyle("SubTitle",    parent = styles["Title"],   fontName = "OpenSans-Bold",     fontSize = 10, leading = 16, alignment = TA_LEFT, backColor=colors.HexColor("#ddf2f3"), textColor = "#2c676c", spaceAfter = 2)

    # ALERT SUBTITLES
    cat_title   = ParagraphStyle("SubTitle",    parent = styles["Title"],   fontName = "OpenSans-Bold",     fontSize = 9, leading = 12, alignment = TA_LEFT, textColor = "#82312f", spaceAfter = 2)
    tcat_title  = ParagraphStyle("SubTitle",    parent = styles["Title"],   fontName = "OpenSans-Bold",     fontSize = 9, leading = 12, alignment = TA_LEFT, textColor = "#235558", spaceAfter = 2)

    main_text   = ParagraphStyle("MainText",    parent = styles["Normal"],  fontName = "OpenSans-Regular",  fontSize = 9, leading = 14, alignment = TA_LEFT, textColor = "#000000", spaceAfter = 5)

    foot_text   = ParagraphStyle("FootText",    parent = styles["Normal"],  fontName = "OpenSans-Regular",  fontSize = 8, leading = 12, alignment = TA_LEFT, textColor = "#000000", spaceAfter = 2)
    table_head  = ParagraphStyle("TableHeader", parent = styles["Normal"],  fontName = "OpenSans-Bold",     fontSize = 9, leading = 9, spaceAfter = 0, textColor = "#000000", )
    table_first = ParagraphStyle("TableCol1",   parent = styles["Normal"],  fontName ="OpenSans-Bold",       fontSize = 10 )
    table_body  = ParagraphStyle("TableBody",   parent = styles["Normal"],  fontName = "OpenSans-Regular",  fontSize = 10, leading = 12, spaceAfter = 0 )
    risk_text   = ParagraphStyle("RiskText",    parent = styles["Normal"],  fontName = "OpenSans-Bold",     fontSize = 10, spaceAfter = 40 )

    wind = ""

    # New M2M data: WIND DIRECTION
    if forecast.wind_direction_m2m.exists():
        wind += "-".join(forecast.wind_direction_m2m.values_list("description",flat=True))
    # Legacy JSON/string data
    elif forecast.wind_direction:
        try:
            direction_ids = json.loads(forecast.wind_direction)
            wind += "-".join(WindDirection.objects.filter(id__in=direction_ids).values_list("description",flat=True))
        except (json.JSONDecodeError, TypeError):
            wind += str(forecast.wind_direction)

    # WIND SPEED
    if forecast.wind_speed is not None:
        wind += ", "
        wind += f"{forecast.wind_speed} kts"

    # New M2M data: WIND CONDITION
    if forecast.wind_condition_m2m.exists():
        wind += " | "
        wind += "-".join(forecast.wind_condition_m2m.values_list("description",flat=True))
    # Legacy JSON/string data
    elif forecast.wind_condition:
        try:
            condition_ids = json.loads(forecast.wind_condition)
            wind += " | "
            wind += "-".join(WindCondition.objects.filter(id__in=condition_ids).values_list("description",flat=True))
        except (json.JSONDecodeError, TypeError):
            wind += str(forecast.wind_condition)

    # New M2M data: WIND SHIFT DIRECTION
    if forecast.wind_shift_direction_m2m.exists():
        wind += " BECOMING "
        wind += "-".join(forecast.wind_shift_direction_m2m.values_list("description",flat=True))
    # Legacy JSON/string data
    elif forecast.wind_shift_direction:
        try:
            sdirection_ids = json.loads(forecast.wind_shift_direction)
            wind += " BECOMING "
            wind += "-".join(WindDirection.objects.filter(id__in=sdirection_ids).values_list("description",flat=True))
        except (json.JSONDecodeError, TypeError):
            wind += str(forecast.wind_shift_direction)

    wind_shift = ""

    # WIND SHIFT SPEED
    if forecast.wind_shift_speed is not None and forecast.wind_shift_speed.strip():
        wind_shift += ", "
        wind_shift += f"{forecast.wind_shift_speed} kts"

    # New M2M data
    if forecast.wind_shift_condition_m2m.exists():
        wind_shift += "-".join(forecast.wind_direction_shift_m2m.values_list("description",flat=True))
    # Legacy JSON/string data
    elif forecast.wind_shift_condition:
        try:
            shdirection_ids = json.loads(forecast.wind_shift_condition)
            wind_shift += "-".join(WindCondition.objects.filter(id__in=shdirection_ids).values_list("description",flat=True))
        except (json.JSONDecodeError, TypeError):
            wind_shift += str(forecast.wind_shift_condition)

    sea = ""

    # New M2M data: SEA STATE
    if forecast.sea_state_m2m.exists():
        sea += "-".join(forecast.sea_state_m2m.values_list("description",flat=True))
    # Legacy JSON/string data
    elif forecast.sea_state:
        try:
            sea_state_ids = json.loads(forecast.sea_state)
            sea += "-".join(SeaState.objects.filter(id__in=sea_state_ids).values_list("description",flat=True))
        except (json.JSONDecodeError, TypeError):
            sea += str(forecast.sea_state)

    waves = ""
    
    # WAVES
    if forecast.wave is not None and forecast.wave.strip():
        waves += f"{forecast.wave} kts"

    # WAVES SHIFT
    if forecast.wave_shift is not None and forecast.wave_shift.strip():
        waves += " BECOMING "
        waves += f"{forecast.wave_shift} kts"

    if wind_shift:
        wind += wind_shift

    available_width = doc.width

    data_head = [[ Paragraph("General Weather Forecast", main_title), Paragraph(f"{forecast.forecast_date.strftime('%B %d, %Y')}, "f"{forecast.forecast_time.strftime('%I:%M %p')}", date_title) ]]

    header_table = Table(data_head, colWidths=[ available_width * 0.5, available_width * 0.5 ])

    data = [[Paragraph("WINDS", table_head), Paragraph("SEA CONDITIONS", table_head), Paragraph("WAVES <font size='8'>(MIN)</font>", table_head) ]]
    data.append([ Paragraph(wind, table_body), Paragraph(sea, table_body), Paragraph(waves, table_body) ])

    table = Table(data, colWidths=[ available_width * 0.32, available_width * 0.35, available_width * 0.32 ], repeatRows = 1)

    style = TableStyle([
        #("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ffffff")),
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
    
    forecaster = ""
    if forecast.created_by:
        forecaster = forecast.created_by.get_full_name() or forecast.created_by.username

    header_table.setStyle(style)
    elements.append(header_table)
    elements.append(Spacer(1, 6))

    elements.append(Paragraph(f"General Situation", sub_title))
    elements.append(Paragraph(f"{forecast.general_situation}", main_text))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph(f"24-Hour Forecast", sub_title))
    elements.append(Paragraph(f"{forecast.twenty_four_hour_forecast}", main_text))
    elements.append(Spacer(1, 6))

    table.setStyle(style)
    elements.append(Paragraph(f"Marine Conditions", sub_title))
    elements.append(table)
    elements.append(Spacer(1, 12))
            
    # New M2M data: Tropical Weather Outlook
    if forecast.cap_alerts.exists():

        elements.append(Paragraph(f"&nbsp;&nbsp;*** Alerts & Advisories ***", alert_title))

        for alert in forecast.cap_alerts.all():
            elements.append(Paragraph(f"{alert.headline}", cat_title))

            if alert.description:
                elements.append(Paragraph(f"{alert.description}", main_text))

            elements.append(Spacer(1, 6))

    elements.append(Paragraph(f"Outlook", sub_title))
    elements.append(Paragraph(f"{forecast.outlook}", main_text))
    elements.append(Spacer(1, 6))

    tropical_weather_outlook = ""
        
    # New M2M data: Tropical Weather Outlook
    if forecast.tropical_alerts.exists():

        elements.append(Paragraph("&nbsp;&nbsp;*** Tropical Weather Outlook ***", talert_title))

        for storm in forecast.tropical_alerts.all():

            # Storm name
            if storm.storm_name or storm.storm_category:
                elements.append(Paragraph(f"<b>{storm.storm_category}, {storm.storm_name}</b>", tcat_title))

            # Description
            if storm.description:
                elements.append(Paragraph(f"{storm.description}", main_text))

            # Space between storms
            elements.append(Spacer(1, 6))
        
    elements.append(Paragraph(f"Forecaster: {forecaster} | Date Created: {forecast.created_datetime.strftime('%B %d, %Y, %I:%M %p')} | Last Updated: {forecast.updated_datetime.strftime('%B %d, %Y, %I:%M %p')}", foot_text))

    doc.build(elements,
        onFirstPage=add_background_wafs_full,
        onLaterPages=add_background_wafs_full
    )
    available_width = doc.width

    # Return saved PDF as download
    return FileResponse(open(file_path, "rb"), as_attachment=False, filename=filename)

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
@require_POST
def import_general_weather_forecast_categories(request):
    try:
        call_command("import_forecast_general_category")
        messages.success(request,"General Weather Forecast Categories imported successfully.")

    except Exception as error:
        messages.error(request,f"General Weather Forecast Categories import failed: {error}")

    return redirect("forecasts:index")

############# DISTRICT FORECATSTS: Risk Level Entry #############
def instructions_list(request, id=None):
    page_name = "Instructions Entries"
    qs = DistrictForecastInstructions.objects.select_related("category").order_by(
            "category__category_name",
            "description",
        )
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
        'prev_page': 'District Forecast',
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
        'prev_page':    'District Forecast Instructions',
        'new_url':      reverse('forecasts:instructions_list'),
        'details_url':  "",
        'back_url':     reverse('forecasts:instructions_list'),
        'api_url':      "/api/pest-risk/",
        'form': form,
        'entry': entry
    })

def instructions_delete(request, id):
    
    entry = get_object_or_404(DistrictForecastInstructions, id=id)

    qs = DistrictForecastInstructions.objects.all().order_by('id')
    qs = qs.order_by('id')
    
    page_name = "District Forecast Instructions Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('forecasts:instructions_list')  # redirect anywhere you prefer

    return render(request, "district-forecast/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('forecasts:instructions_list'),
        'details': qs
    })

@require_POST
def district_forecast_instructions_ajax_add(request):
    description = request.POST.get("description", "").strip()
    category = request.POST.get("category", "").strip()

    if not description:
        return JsonResponse({
            "success": False,
            "error": "Description is required."
        })

    if not category:
        return JsonResponse({
            "success": False,
            "error": "Category is required."
        })

    item = DistrictForecastInstructions.objects.create(description=description, category_id=category)

    return JsonResponse({
        "success": True,
        "id": item.id,
        "description": str(item),
        "category": item.category.category_name if item.category else None
    })

############# DISTRICT FORECASTS: Instructions Category #############
def instructions_category_list(request, id=None):
    page_name = "Instructions Category Entries"
    qs = DistrictForecastInstructionsCategory.objects.all().order_by('-id')
    table = InstructionsCategoryTable(qs)
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
        'new_url':  reverse('forecasts:instructions_category_entry'),
        'back_url': reverse('forecasts:index'),
        #'api_url': "/api/pest-risk/",
    }
    return render(request, 'district-forecast/parameters_table_list.html', context)

def instructions_category_entry(request, id=None):

    page_name = "Instructions Category Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(DistrictForecastInstructionsCategory, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = DistrictForecastInstructionsCategoryForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('forecasts:instructions_category_list', saved_entry.id)
        
    else:
        form = DistrictForecastInstructionsCategoryForm(instance=entry)

    return render(request, 'district-forecast/parameters_entry_form.html', {
        'page_name':    page_name,
        'new_url':      reverse('forecasts:instructions_list'),
        'details_url':  "",
        'back_url':     reverse('forecasts:instructions_list'),
        'api_url':      "/api/pest-risk/",
        'form': form,
        'entry': entry
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

    return render(request, 'district-forecast/table_list_main.html', {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': 'Weather Forecasts',
        'table': table,
        'new_url':  reverse('forecasts:district_forecast_entry'),
        'back_url': reverse('forecasts:index'),
        'api_url':  reverse('district-forecast-list'),
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
        'prev_page': "District Forecast",
        'new_url':  reverse('forecasts:district_forecast_entry'),
        'back_url':  reverse('forecasts:district_forecast_list'),
        'form': form,
        'entry': entry,
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

def district_forecast_generate_pdf(request, id=None):

    forecast = get_object_or_404(DistrictForecast, id=id)

    # Create a file-like buffer to receive PDF data
    #buffer = io.BytesIO()

    # Folder where PDF will be saved
    folder_path = os.path.join(settings.MEDIA_ROOT, "forecast", "district","doc")
    os.makedirs(folder_path, exist_ok=True)

    # Full PDF file path
    filename = f"District_Forecast_{forecast.forecast_date}_NMS_BZ.pdf"
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
        
        weather_prob_text   = (f"<font size='8' color='{weather_color}'>{weather_prob}</font>") if weather_prob else ""
        temp_min_prob_text  = (f"<font size='8' color='{temp_min_color}'>{temp_min_prob}</font>") if temp_min_prob else ""
        temp_max_prob_text  = (f"<font size='8' color='{temp_max_color}'>{temp_max_prob}</font>") if temp_max_prob else ""
        precip_prob_text    = (f"<font size='8' color='{precip_color}'>{precip_prob}</font>") if precip_prob else ""
        wind_prob_text      = (f"<font size='8' color='{wind_color}'>{wind_prob}</font>") if wind_prob else ""

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

    # Return saved PDF as download
    return FileResponse(open(file_path, "rb"), as_attachment=False, filename=filename)

############# DISTRICT FORECASTS: Details List #############
def district_forecast_details_list(request, id=None, fk=None):

    #print(fk);
    page_name = "District Forecast Entry"

    # Parent forecast
    parent_entry = get_object_or_404(DistrictForecast, id=id)

    # Get only details for this forecast
    qs = DistrictForecastDetails.objects.filter(forecast_id=id).order_by('id')
    table = DistrictForecastDetailsTable(qs)
    RequestConfig(request).configure(table)

    print("Forecast ID:", id)
    print("Details count:", qs.count())
    print(qs.query)

    return render(request, 'district-forecast/table_list_details.html', {
        'id' : id,
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
        print(request.POST)
        form = DistrictForecastPublishForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            messages.success(request, "Record saved successfully.")
            #return redirect('forecasts:district_forecast_details_entry', saved_entry.id)            

            # Save & Close button
            #if 'btn_submit_close' in request.POST:
            #   return redirect('forecasts:district_forecast_list')

            # Regular Save button
            return redirect('forecasts:district_forecast_details_entry', saved_entry.id)  
            
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)  # check terminal
    else:
        form = DistrictForecastPublishForm(instance=entry)

    return render(request, 'district-forecast/table_list_details_entry_form.html', {
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
            messages.success(request, "Record saved successfully.")

            # Save & Close button
            if 'btn_submit_close' in request.POST:
                return redirect('forecasts:district_forecast_details_entry',fk)

            # Regular Save button
            return redirect('forecasts:district_forecast_details_entry_item',fk,saved_entry.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DistrictForecastDetailsForm(instance=item_entry)

    return render(request, 'district-forecast/details_entry_form.html', {
        'page_name': page_name,
        'prev_page': 'District Forecasts',
        'id': id,
        'forecast_id': fk,
        'main_entry': main_entry,
        'item_entry': item_entry,
        'form': form,
        'forecast_id': fk,
        'back_url': reverse('forecasts:district_forecast_details_entry', kwargs={'id': fk}),
    })

'''def district_forecast_details_instructions_ajax_add(request):
    if request.method == "POST":
        description = request.POST.get("description")
        category_id = request.POST.get("category")

        if not description:
            return JsonResponse({
                "success": False,
                "error": "Instruction description is required."
            })

        if not category_id:
            return JsonResponse({
                "success": False,
                "error": "Instruction category is required."
            })

        instruction = DistrictForecastInstructions.objects.create(
            description=description,
            category_id=category_id
        )

        return JsonResponse({
            "success": True,
            "id": instruction.id,
            "description": instruction.description,
            "category": instruction.category_id,
        })'''

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



class WIMP2FilesAPIView(APIView):

    #permission_classes = [AllowAny]
    http_method_names = ['get', 'head','options']

    def get(self, request):
        audio_dir   = os.path.join(settings.MEDIA_ROOT, "forecast", "general", "audio")
        gen_pdf_dir = os.path.join(settings.MEDIA_ROOT, "forecast", "general", "doc")
        mar_pdf_dir = os.path.join(settings.MEDIA_ROOT, "forecast", "marine", "doc")
        avi_pdf_dir = os.path.join(settings.MEDIA_ROOT, "forecast", "aviation", "doc")
        day_pdf_dir = os.path.join(settings.MEDIA_ROOT, "forecast", "daily", "doc")

        audio_url = None
        gen_pdf_url = None
        mar_pdf_url = None
        avi_pdf_url = None
        day_pdf_url = None

        # Find newest audio file
        if os.path.exists(audio_dir):
            audio_files = [
                f for f in os.listdir(audio_dir)
                if f.lower().endswith(".mp3")
            ]

            if audio_files:
                newest_audio = max(audio_files, key=lambda f: os.path.getmtime(os.path.join(audio_dir, f)))
                audio_url = request.build_absolute_uri(settings.MEDIA_URL + "forecast/general/audio/" + newest_audio)

        # Find newest General / PDF file
        if os.path.exists(gen_pdf_dir):
            gen_pdf_url = [
                f for f in os.listdir(gen_pdf_dir)
                if f.lower().endswith(".pdf")
            ]

            if gen_pdf_url:
                newest_pdf_gen  = max(gen_pdf_url, key=lambda f: os.path.getmtime(os.path.join(gen_pdf_dir, f)))
                gen_pdf_url     = request.build_absolute_uri(settings.MEDIA_URL + "forecast/general/doc/" + newest_pdf_gen)

        # Find newest Marine / PDF file
        if os.path.exists(mar_pdf_dir):
            mar_pdf_url = [
                f for f in os.listdir(mar_pdf_dir)
                if f.lower().endswith(".pdf")
            ]

            if mar_pdf_url:
                newest_pdf_mar  = max(mar_pdf_url, key=lambda f: os.path.getmtime(os.path.join(mar_pdf_dir, f)))
                mar_pdf_url     = request.build_absolute_uri(settings.MEDIA_URL + "forecast/marine/doc/" + newest_pdf_mar)

        # Find newest Aviation / PDF file
        if os.path.exists(avi_pdf_dir):
            avi_pdf_url = [
                f for f in os.listdir(avi_pdf_dir)
                if f.lower().endswith(".pdf")
            ]

            if avi_pdf_url:
                newest_pdf_avi  = max(avi_pdf_url, key=lambda f: os.path.getmtime(os.path.join(avi_pdf_dir, f)))
                avi_pdf_url     = request.build_absolute_uri(settings.MEDIA_URL + "forecast/aviation/doc/" + newest_pdf_avi)


        # Find newest Daily (4-Day) / PDF file
        if os.path.exists(day_pdf_dir):
            day_pdf_url = [
                f for f in os.listdir(day_pdf_dir)
                if f.lower().endswith(".pdf")
            ]

            if day_pdf_url:
                newest_pdf_day  = max(day_pdf_url, key=lambda f: os.path.getmtime(os.path.join(day_pdf_dir, f)))
                day_pdf_url     = request.build_absolute_uri(settings.MEDIA_URL + "forecast/daily/doc/" + newest_pdf_day)

        return Response({
            "audio":        audio_url,
            "general_pdf":  gen_pdf_url,
            "marine_pdf":   mar_pdf_url,
            "aviation_pdf": avi_pdf_url,
            "daily_pdf":    day_pdf_url
        })
    
class DistrictForecastDetailsViewSet(viewsets.ModelViewSet):
   queryset = DistrictForecastDetails.objects.all().order_by('id')
   serializer_class = DistrictForecastDetailsSerializer
   http_method_names = ['get', 'head','options']

class DistrictForecastAllViewSet(viewsets.ModelViewSet):
    queryset = DistrictForecast.objects.all().order_by("-forecast_date").prefetch_related("district_forecast_details")
    serializer_class = DistrictForecastSerializer
    pagination_class = None
    http_method_names = ['get', 'head','options']

class DistrictForecastViewSet(viewsets.ModelViewSet):
    queryset = DistrictForecast.objects.filter(is_published=True).prefetch_related("district_forecast_details")
    serializer_class = DistrictForecastSerializer
    pagination_class = None
    http_method_names = ['get', 'head','options']

class GeneralForecastAllViewSet(viewsets.ModelViewSet):
    queryset = ForecastGeneral.objects.all().order_by("-forecast_date","-forecast_time")
    serializer_class = GeneralForecastSerializer
    pagination_class = None
    http_method_names = ['get', 'head','options']

class GeneralForecastViewSet(viewsets.ModelViewSet):
    queryset = ForecastGeneral.objects.filter(is_published=True)
    serializer_class = GeneralForecastSerializer
    pagination_class = None
    http_method_names = ['get', 'head','options']