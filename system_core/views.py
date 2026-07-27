from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from django.urls import reverse
from django_tables2 import RequestConfig

from .models import JobTitle, DepartmentSection, OfficeLocation
from .tables import DepartmentSectionTable, JobTitleTable, OfficeLocationTable
from .forms import DepartmentSectionForm, JobTitleForm, OfficeLocationForm

# Create your views here.

def index(request):
    context = {
        'page_name': 'System Parameters',
    }
    return render(request, 'system_home.html', context)

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
        "prev_page": 'Inventory Management',
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
        "prev_page": 'Inventory Management',
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
        "prev_page": 'Inventory Management',
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