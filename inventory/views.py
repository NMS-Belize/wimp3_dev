from unittest import loader

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from django_tables2 import RequestConfig

from system_core.models import OfficeLocation
from users.models import Employee

from .forms     import InventoryCategoryForm, InventoryItemPhotoFormSet, HardwareSpecificationsForm, NetworkDetailsForm, ManufacturerForm, InventoryItemForm, DeviceTypeForm, VendorForm
from .models    import DeviceType, InventoryCategory, InventoryItem, Manufacturer, Vendor
from .tables    import InventoryCategoryTable, InventoryTable, ManufacturerTable, DeviceTypeTable, VendorTable

from .filters import InventoryItemFilter

def index(request):
    context = {
        'page_name': 'Inventory Home',
    }
    return render(request, 'inventory_home.html', context) 

############# INVENTORY - Items
def inventory_list(request, id=None):
    page_name = "Inventory List"
    qs = InventoryItem.objects.all().order_by('id')

    filterset = InventoryItemFilter(
        request.GET,
        queryset=qs
    )
    
    table = InventoryTable(filterset.qs)
    table.empty_text = "No records available"
    #RequestConfig(request).configure(table)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)


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
        "filter": filterset,
        'new_url': reverse('inventory:inventory_entry'),
        'back_url': reverse('inventory:index'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'inventory_table_list.html', context)

def inventory_entry(request, id=None):

    page_name = "Inventory Item Entry"

    # If an ID exists, update the record.
    # Otherwise, create a new InventoryItem instance.
    if id:
        entry = get_object_or_404(InventoryItem, id=id)
    else:
        entry = InventoryItem()

    if request.method == "POST":

        form_main       = InventoryItemForm(request.POST, request.FILES, instance=entry)
        form_hardware   = HardwareSpecificationsForm(request.POST, request.FILES, instance=entry)
        form_network    = NetworkDetailsForm(request.POST, request.FILES, instance=entry)
        form_photos     = InventoryItemPhotoFormSet(request.POST,request.FILES,instance=entry,prefix="photos")

        main_valid = form_main.is_valid()
        hardware_valid = form_hardware.is_valid()
        network_valid = form_network.is_valid()
        photos_valid = form_photos.is_valid()

        print("Main valid:", main_valid)
        print("Main errors:", form_main.errors)
        print("Main changed data:", form_main.changed_data)

        print("Hardware valid:", hardware_valid)
        print("Hardware errors:", form_hardware.errors)

        print("Network valid:", network_valid)
        print("Network errors:", form_network.errors)

        print("Photos valid:", photos_valid)
        print("Photo errors:", form_photos.errors)
        print("Photo non-form errors:", form_photos.non_form_errors())

        if form_main.is_valid() and form_photos.is_valid() and form_hardware.is_valid() and form_network.is_valid():
            try:
                with transaction.atomic():

                    saved_entry = form_main.save(commit=False)

                    # Set user tracking fields.
                    if not saved_entry.pk:
                        saved_entry.created_by = request.user

                    saved_entry.updated_by = request.user
                    saved_entry.save()

                    # Connect other forms to the saved inventory item.
                    form_hardware.instance = saved_entry
                    form_hardware.save()

                    form_network.instance = saved_entry
                    form_network.save()

                    form_photos.instance = saved_entry
                    form_photos.save()

                messages.success(request, "Inventory record and details saved successfully.")

                # Save and Close button.
                if "btn_submit_close" in request.POST:
                    return redirect("inventory:inventory_list")

                # Regular Save button.
                return redirect("inventory:inventory_entry",id=saved_entry.id)

            except Exception as error:
                messages.error(request, "The inventory record could not be saved.")
                print("Inventory save error:", error)

        else:
            messages.error(request, "Please correct the errors below.")
            messages.error(request, "Inventory errors:", form_main.errors)
            messages.error(request, "Hardware errors:", form_hardware.errors)
            messages.error(request, "Network errors:", form_network.errors)
            #print("Photo errors:", form_photos.errors.as_json())
            messages.error(request, "Photo non-form errors:",form_photos.non_form_errors())

    else:
        form_main = InventoryItemForm(instance=entry)
        form_hardware = HardwareSpecificationsForm(instance=entry,prefix="hardware")
        form_network = NetworkDetailsForm(instance=entry,prefix="network")
        form_photos = InventoryItemPhotoFormSet(instance=entry,prefix="photos")

    return render(request,"inventory/entry_form.html",{
            "page_name":    page_name,
            "new_url":      reverse("inventory:inventory_entry"),
            "back_url":     reverse("inventory:inventory_list"),
            "prev_page":    "Inventory Management",
            "api_url":      reverse("sectors-list"),
            "form":         form_main,
            "form_photos":  form_photos,
            "form_hardware": form_hardware,
            "form_network": form_network,
            "entry":        entry
        }
    )

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
    return render(request, 'inventory/parameters_table_list.html', context)

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

@require_GET
def get_placement_floor(request):
    placement_id = request.GET.get("placement_id")

    if not placement_id:
        return JsonResponse({
            "success": False,
            "floor": "",
            "error": "No placement was selected.",
        })

    try:
        placement = OfficeLocation.objects.get(pk=placement_id)

        return JsonResponse({
            "success": True,
            "floor": placement.floor or "",
        })

    except OfficeLocation.DoesNotExist:
        return JsonResponse({
            "success": False,
            "floor": "",
            "error": "Placement was not found.",
        }, status=404)

@require_GET
def get_assigned_details(request):
    
    user_id = request.GET.get("user_id")
    print(user_id)
    if not user_id:
        return JsonResponse({ "success": False, "department": "", "error": "No User was selected." })

    try:
        employee = Employee.objects.get(pk=user_id)
        return JsonResponse({ 
            "success": True, 
            "department": employee.department_id or ""
        })
    
    except Employee.DoesNotExist:
        return JsonResponse({ "success": False, "department": "", "error": "Department was not found." }, status=404)
    
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
    return render(request, 'inventory/parameters_table_list.html', context)

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

