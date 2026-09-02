from django.shortcuts import render
from django_tables2 import RequestConfig
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from file_manager.models import Files
from file_manager.tables import FilesTable

def file_manager_list(request, id=None):
    page_name = "File Manager"
    qs = Files.objects.all().order_by('-id')

    table = FilesTable(qs)
    table.empty_text = "No records available"
    #table.order_by = ("-forecast_date", "-forecast_category")
    

    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    #if id is not None:
    #entry = get_object_or_404(Probability, id=id)
    
    return render(request, 'table_list_main.html', {
       'id' : id,
        'entry': entry,  
        'page_name': page_name,
        "prev_page": 'Dashboard',
        'table': table,
        'new_url':  reverse('forecasts:probability_entry'),
        'back_url': reverse('forecasts:index'),
        #'api_url': "/api/pest-risk/",
    })