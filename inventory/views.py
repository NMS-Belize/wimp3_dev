from unittest import loader

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django_tables2 import RequestConfig

from .forms     import InventoryCategoryForm
from .models    import InventoryCategory, InventoryItem
from .tables    import InventoryCategoryTable, InventoryTable

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
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(InventoryItem, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'table': table,
        'new_url': reverse('inventory:inventory_entry'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'table_list_template.html', context)

def inventory_entry(request, id=None):

    page_name = "Inventory Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(InventoryItem, id=id)
    else:
        entry = None

    '''if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('inventory:inventory_list', saved_entry.id)
    else:
        form = InventoryItemForm(instance=entry)

    return render(request, 'inventory_form.html', {
        'page_name': page_name,
        'new_url':  reverse('inventory:inventory_entry'),
        'back_url': reverse('inventory:inventory_list'),
        'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })'''

def inventory_delete(request, id):
    
    entry = get_object_or_404(InventoryItem, id=id)
    
    page_name = "Inventory Entry"

    if request.method == "POST":
        entry.delete()
        messages.success(request, "deleted")  # acts like True
        return redirect('inventory:inventory_list')  # redirect anywhere you prefer
    
    return render(request, "delete_inventory.html", {
        "entry": entry,
        'page_name': page_name,
    })


def inventory_category_list(request, id=None):
    page_name = "Inventory Category List"
    qs = InventoryCategory.objects.all().order_by('id')
    table = InventoryCategoryTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(InventoryCategory, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'table': table,
        'new_url': reverse('inventory:inventory_category_entry'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'inventory_table_list_template.html', context)

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
            return redirect('inventory:inventory_list', saved_entry.id)
    else:
        form = InventoryCategoryForm(instance=entry)

    return render(request, 'entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('inventory:inventory_entry'),
        'back_url': reverse('inventory:inventory_list'),
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
    
    return render(request, "delete_inventory_item.html", {
        "entry": entry,
        'page_name': page_name,
    })

