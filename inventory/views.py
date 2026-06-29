from unittest import loader

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django_tables2 import RequestConfig

from .forms     import InventoryCategoryForm, DepartmentSectionForm, ManufacturerForm, InventoryItemForm, DeviceTypeForm, VendorForm
from .models    import DepartmentSection, DeviceType, InventoryCategory, InventoryItem, Manufacturer, Vendor
from .tables    import DepartmentSectionTable, InventoryCategoryTable, InventoryTable, ManufacturerTable, DeviceTypeTable, VendorTable

def index(request):
    context = {
        'page_name': 'Inventory Home',
    }
    return render(request, 'inventory_home.html', context) 

############# INVENTORY - Items
def inventory_list(request, id=None):
    page_name = "Inventory List"
    qs = InventoryItem.objects.all().order_by('id')
    table = InventoryTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(InventoryItem, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        "prev_page": 'Inventory Management',
        'table': table,
        'new_url': reverse('inventory:inventory_entry'),
        'back_url': reverse('inventory:index'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'inventory_table_list.html', context)

def inventory_entry(request, id=None):

    page_name = "Inventory Item Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(InventoryItem, id=id)
    else:
        entry = None

    #print(entry.category_id)  # check terminal

    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            messages.success(request, "Record saved successfully.")

            # Save & Close button
            if 'btn_submit_close' in request.POST:
                return redirect('inventory:inventory_list')

            # Regular Save button
            return redirect('inventory:inventory_entry',saved_entry.id)
            #return redirect('inventory:inventory_list', saved_entry.id)
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)  # check terminal
    else:
        form = InventoryItemForm(instance=entry)

    return render(request, 'inventory/entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('inventory:inventory_entry'),
        'back_url': reverse('inventory:inventory_list'),
        "prev_page": 'Inventory Management',
        'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })

def inventory_delete(request, id):
    
    entry = get_object_or_404(InventoryItem, id=id)
    
    page_name = "Inventory Entry"

    if request.method == "POST":
        entry.delete()
        messages.success(request, "deleted")  # acts like True
        return redirect('inventory:inventory_list')  # redirect anywhere you prefer
    
    return render(request, "inventory_delete.html", {
        "entry": entry,
        'page_name': page_name,
    })

def inventory_category_list(request, id=None):
    page_name = "Inventory Category List"
    qs = InventoryCategory.objects.all().order_by('id')
    table = InventoryCategoryTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(InventoryCategory, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        "prev_page": 'Inventory Management',
        'table': table,
        'new_url': reverse('inventory:inventory_category_entry'),
        'back_url': reverse('inventory:index'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'inventory_table_list.html', context)

def inventory_category_entry(request, id=None):
    entry = None

    page_name = "Inventory Category Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(InventoryCategory, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = InventoryCategoryForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('inventory:inventory_category_list', saved_entry.id)
    else:
        form = InventoryCategoryForm(instance=entry)

    return render(request, 'inventory/parameters_entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('inventory:inventory_category_entry'),
        'back_url': reverse('inventory:inventory_category_list'),
        'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })

def inventory_category_delete(request, id):
    
    entry = get_object_or_404(InventoryCategory, id=id)
    
    page_name = "Inventory Category"

    if request.method == "POST":
        entry.delete()
        messages.success(request, "deleted")  # acts like True
        return redirect('inventory:inventory_category_list')  # redirect anywhere you prefer
    
    return render(request, "inventory/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('inventory:inventory_category_list'),
    })

def device_type_list(request, id=None):
    page_name = "Device Type List"
    qs = DeviceType.objects.all().order_by('id')
    table = DeviceTypeTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(DeviceType, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        "prev_page": 'Inventory Management',
        'table': table,
        'new_url': reverse('inventory:device_type_entry'),
        'back_url': reverse('inventory:index'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'inventory_table_list.html', context)

def device_type_entry(request, id=None):
    entry = None

    page_name = "Device Type Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(DeviceType, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = DeviceTypeForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            messages.success(request, f"Record {saved_entry.name} was updated successfully.")
            return redirect('inventory:device_type_list', saved_entry.id)
    else:
        form = DeviceTypeForm(instance=entry)

    return render(request, 'inventory/parameters_entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('inventory:device_type_entry'),
        'back_url': reverse('inventory:device_type_list'),
        'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })

def device_type_delete(request, id):
    
    entry = get_object_or_404(DeviceType, id=id)
    page_name = "Device Type"

    if request.method == "POST":
        entry.delete()
        messages.success(request, f"Record {entry.name} was deleted successfully.")
        return redirect('inventory:device_type_list')
    
    return render(request, "inventory/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('inventory:device_type_list'),
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
        'new_url': reverse('inventory:department_section_entry'),
        'back_url': reverse('inventory:index'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'inventory_table_list.html', context)

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
            return redirect('inventory:department_section_list', saved_entry.id)
    else:
        form = DepartmentSectionForm(instance=entry)

    return render(request, 'inventory/parameters_entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('inventory:department_section_entry'),
        'back_url': reverse('inventory:department_section_list'),
        'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })

def department_section_delete(request, id):
    
    entry = get_object_or_404(DepartmentSection, id=id)
    
    page_name = "Department Section"

    if request.method == "POST":
        entry.delete()
        messages.success(request, "deleted")  # acts like True
        return redirect('inventory:department_section_list')  # redirect anywhere you prefer
    
    return render(request, "inventory/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('inventory:department_section_list'),
    })

def manufacturer_list(request, id=None):
    page_name = "Manufacturer List"
    qs = Manufacturer.objects.all().order_by('id')
    table = ManufacturerTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(Manufacturer, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        "prev_page": 'Inventory Management',
        'table': table,
        'new_url': reverse('inventory:manufacturer_entry'),
        'back_url': reverse('inventory:index'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'inventory_table_list.html', context)

def manufacturer_entry(request, id=None):
    entry = None

    page_name = "Manufacturer Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(Manufacturer, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = ManufacturerForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            messages.success(request, f"Record {saved_entry.name} was updated successfully.")
            return redirect('inventory:manufacturer_list', saved_entry.id)
    else:
        form = ManufacturerForm(instance=entry)

    return render(request, 'inventory/parameters_entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('inventory:manufacturer_entry'),
        'back_url': reverse('inventory:manufacturer_list'),
        'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })

def manufacturer_delete(request, id):
    
    entry = get_object_or_404(Manufacturer, id=id)
    page_name = "Manufacturer"

    if request.method == "POST":
        entry.delete()
        messages.success(request, f"Record {entry.name} was deleted successfully.")
        return redirect('inventory:manufacturer_list')
    
    return render(request, "inventory/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('inventory:manufacturer_list'),
    })

def vendor_list(request, id=None):
    page_name = "Vendor List"
    qs = Vendor.objects.all().order_by('id')
    table = VendorTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(Vendor, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        "prev_page": 'Inventory Management',
        'table': table,
        'new_url': reverse('inventory:vendor_entry'),
        'back_url': reverse('inventory:index'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'inventory_table_list.html', context)

def vendor_entry(request, id=None):
    entry = None

    page_name = "Vendor Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(Vendor, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = VendorForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            messages.success(request, f"Record {saved_entry.name} was updated successfully.")
            return redirect('inventory:vendor_list', saved_entry.id)
    else:
        form = VendorForm(instance=entry)

    return render(request, 'inventory/parameters_entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('inventory:vendor_entry'),
        'back_url': reverse('inventory:vendor_list'),
        'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })

def vendor_delete(request, id):
    
    entry = get_object_or_404(Vendor, id=id)
    page_name = "Vendor"

    if request.method == "POST":
        entry.delete()
        messages.success(request, f"Record {entry.name} was deleted successfully.")
        return redirect('inventory:vendor_list')
    
    return render(request, "inventory/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('inventory:vendor_list'),
    })

