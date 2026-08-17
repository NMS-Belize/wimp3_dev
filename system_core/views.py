from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from django.urls import reverse
from django_tables2 import RequestConfig

from .models import JobTitle, DepartmentSection, OfficeLocation, AlertLevel, RiskLevel, District, Zone
from .tables import DepartmentSectionTable, JobTitleTable, OfficeLocationTable, DistrictTable, RiskLevelTable, AlertLevelTable, ZoneAreaTable
from .forms import DepartmentSectionForm, JobTitleForm, OfficeLocationForm, AlertLevelForm, DistrictForm, RiskLevelForm, ZoneAreaForm

from rest_framework import viewsets

from .serializers import DistrictSerializer, AlertLevelSerializer

# Create your views here.

def index(request):
    context = {
        'page_name': 'System Parameters',
    }
    return render(request, 'system_home.html', context)

############# District #############
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

    return render(request, 'system/parameters_table_list.html', {
        'id' : id, 
        'entry': entry, 
        'page_name': page_name,
        'prev_page': 'System Parameters', 
        'table' : table,
        'new_url':  reverse('system_core:district_entry'),
        'back_url': reverse('system_core:index'),
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
            return redirect('system_core:district_list', saved_entry.id)
    else:
        form = DistrictForm(instance=entry)

    return render(request, 'system/parameters_entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('system_core:district_entry'),
        'back_url': reverse('system_core:district_list'),
        'prev_page': 'Districts',
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

    return render(request, "system/parameters_delete_district.html", {
        "entry": entry,
        'page_name': page_name,
        'details': qs
    })

############# Zone/Area #############
def zone_area_list(request, id=None):
    page_name = "Zone/Area"
    qs = Zone.objects.all().order_by('id')
    table = ZoneAreaTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(Zone, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'prev_page': "System Parameters",
        'table': table,
        'new_url':  reverse('system_core:zone_area_entry'),
        'api_url':  reverse('zones-list'),
        'back_url': reverse('system_core:index'),
    }
    return render(request, 'pest-risk/parameters_table_list.html', context)

def zone_area_entry(request, id=None):

    page_name = "Zone/Area Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(Zone, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = ZoneAreaForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('system_core:zone_area_list', saved_entry.id)
    else:
        form = ZoneAreaForm(instance=entry)

    return render(request, 'entry_form.html', {
        'page_name': page_name,
        'prev_page': "Zone/Area List",
        'new_url':  reverse('system_core:zone_area_entry'),
        'back_url': reverse('system_core:zone_area_list'),
        'api_url': reverse('zones-list'),
        'form': form,
        'entry': entry
    })

def zone_area_delete(request, id):
    
    entry = get_object_or_404(Zone, id=id)
    
    page_name = "Zone/Area Entry"

    if request.method == "POST":
        entry.delete()
        messages.success(request, "deleted")  # acts like True
        return redirect('system_core:zone_area_list')  # redirect anywhere you prefer
    
    return render(request, "pest-risk/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
    })

#############  Alert Level #############
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
        'prev_page': 'System Parameters',
        'table': table,
        'new_url':  reverse('system_core:alert_level_entry'),
        'back_url': reverse('system_core:index'),
        #'api_url': "/api/pest-risk/",
    }
    return render(request, 'system/parameters_table_list.html', context)

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
            return redirect('system_core:alert_level_list', saved_entry.id)
        
    else:
        #form = PestRiskMainListingForm(instance=entry)
        form = AlertLevelForm(instance=entry)

    return render(request, 'system/parameters_entry_form.html', {
        'page_name':    page_name,
        'prev_page': 'Alert Levels',
        'new_url':      reverse('system_core:alert_level_entry'),
        'details_url':  "",
        'back_url':     reverse('system_core:alert_level_list'),
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
        
        return redirect('system_core:alert_level_list')  # redirect anywhere you prefer

    return render(request, "system/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'details': qs
    })

############# Risk Level #############
def risk_level_list(request, id=None):
    page_name = "Risk Level Entries"
    qs = RiskLevel.objects.all().order_by('-id')
    table = RiskLevelTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None

    context = {
        'entry': entry,  
        'page_name': page_name,
        'prev_page': 'System Parameters',
        'table': table,
        'new_url':  reverse('system_core:risk_level_entry'),
        'back_url': reverse('system_core:index'),
    }
    return render(request, 'system/parameters_table_list.html', context)

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
            return redirect('system_core:risk_level_list', saved_entry.id)
        
    else:
        #form = PestRiskMainListingForm(instance=entry)
        form = RiskLevelForm(instance=entry,initial={'months': True})

    return render(request, 'system/parameters_entry_form.html', {
        'page_name':    page_name,
        'new_url':      reverse('system_core:risk_level_list'),
        'details_url':  "",
        #'back_url':     reverse('system_core:risk_level_list'),
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
        
        return redirect('system_core:risk_level_list')  # redirect anywhere you prefer

    return render(request, "system/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'details': qs
    })

############# Job Title #############
def job_title_list(request, id=None):
    page_name = "Job Title List"
    qs = JobTitle.objects.all().order_by('id')
    table = JobTitleTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(JobTitle, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        "prev_page": 'System Parameters',
        'table': table,
        #'new_url': reverse('system_core:job_title_entry'),
        'back_url': reverse('system_core:index'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'system_table_list.html', context)

def job_title_entry(request, id=None):
    entry = None

    page_name = "Job Title Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(JobTitle, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = JobTitleForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('system_core:job_title_list', saved_entry.id)
    else:
        form = JobTitleForm(instance=entry)

    return render(request, 'system/parameters_entry_form.html', {
        'page_name': page_name,
        'prev_page': 'Job Titles',
        'new_url':  reverse('system_core:job_title_entry'),
        'back_url': reverse('system_core:job_title_list'),
        #'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })

def job_title_delete(request, id):
    
    entry = get_object_or_404(JobTitle, id=id)
    
    page_name = "Job Title Delete"

    if request.method == "POST":
        entry.delete()
        messages.success(request, "deleted")  # acts like True
        return redirect('system_core:job_title_list')  # redirect anywhere you prefer
    
    return render(request, "system/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('system_core:job_title_list'),
    })

############# Deaprtment #############
def department_section_list(request, id=None):
    page_name = "Department Section List"
    qs = DepartmentSection.objects.all().order_by('id')
    table = DepartmentSectionTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(DepartmentSection, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        "prev_page": 'System Parameters',
        'table': table,
        'new_url': reverse('system_core:department_section_entry'),
        'back_url': reverse('system_core:index'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'system_table_list.html', context)

def department_section_entry(request, id=None):
    entry = None

    page_name = "Department Section Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(DepartmentSection, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = DepartmentSectionForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('system_core:department_section_list', saved_entry.id)
    else:
        form = DepartmentSectionForm(instance=entry)

    return render(request, 'system/parameters_entry_form.html', {
        'page_name': page_name,
        'prev_page': 'Department Sections',
        'new_url':  reverse('system_core:department_section_entry'),
        'back_url': reverse('system_core:department_section_list'),
        #'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })

def department_section_delete(request, id):
    
    entry = get_object_or_404(DepartmentSection, id=id)
    
    page_name = "Department Section"

    if request.method == "POST":
        entry.delete()
        messages.success(request, "deleted")  # acts like True
        return redirect('system_core:department_section_list')  # redirect anywhere you prefer
    
    return render(request, "system/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('system_core:department_section_list'),
    })

############# Office Location/Placement #############
def office_location_list(request, id=None):
    page_name = "Office Location List"
    qs = OfficeLocation.objects.all().order_by('id')
    table = OfficeLocationTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(OfficeLocation, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        "prev_page": 'System Parameters',
        'table': table,
        'new_url': reverse('system_core:office_location_entry'),
        'back_url': reverse('system_core:index'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'system_table_list.html', context)

def office_location_entry(request, id=None):
    entry = None

    page_name = "Office Location Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(OfficeLocation, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = OfficeLocationForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('system_core:office_location_list', saved_entry.id)
    else:
        form = OfficeLocationForm(instance=entry)

    return render(request, 'system/parameters_entry_form.html', {
        'page_name': page_name,
        'prev_page': 'Office Locations',
        'new_url':  reverse('system_core:office_location_entry'),
        'back_url': reverse('system_core:office_location_list'),
        #'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })

def office_location_delete(request, id):
    
    entry = get_object_or_404(OfficeLocation, id=id)
    
    page_name = "Office Location"

    if request.method == "POST":
        entry.delete()
        messages.success(request, "deleted")  # acts like True
        return redirect('system_core:office_location_list')  # redirect anywhere you prefer
    
    return render(request, "system/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('system_core:office_location_list'),
    })

class DistrictViewSet(viewsets.ModelViewSet):
   queryset = District.objects.all().order_by('id')
   serializer_class = DistrictSerializer
   http_method_names = ['get', 'head','options']

class AlertLevelViewSet(viewsets.ModelViewSet):
   queryset = AlertLevel.objects.all().order_by('id')
   serializer_class = AlertLevelSerializer
   http_method_names = ['get', 'head','options']