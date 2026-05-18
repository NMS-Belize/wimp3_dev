from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django_tables2 import RequestConfig

from .models    import WeatherIcons
from .tables    import WeatherIconsTable
from .forms     import WeatherIconsForm

# Create your views here.
def index(request):
    context = {
        'page_name': 'Weather Observations Home',
    }
    return render(request, 'observations_home.html', context) 

############# WEATHER ICONS
def weather_icon_list(request, id=None):
    page_name = "Weather Icons List"
    qs = WeatherIcons.objects.all().order_by('id')
    table = WeatherIconsTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    if id is not None:
        entry = get_object_or_404(WeatherIcons, id=id)

    context = {
        'id' : id,
        'entry': entry,  
        'page_name': page_name,
        'table': table,
        'new_url': reverse('observations:weather_icon_entry'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'observations_table_list_template.html', context)

def weather_icon_entry(request, id=None):

    page_name = "Weather Icon Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(WeatherIcons, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = WeatherIconsForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('observations:weather_icon_list', saved_entry.id)
    else:
        form = WeatherIconsForm(instance=entry)

    return render(request, 'entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('observations:weather_icon_entry'),
        'back_url': reverse('observations:weather_icon_list'),
        'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })