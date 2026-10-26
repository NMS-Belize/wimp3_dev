from django.db import transaction
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django_tables2 import RequestConfig
from django.contrib import messages
from django.templatetags.static import static

from pathlib import Path

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets

from .models    import WeatherIcons, WeatherCodes
from .tables    import WeatherIconsTable, WeatherCodesTable
from .forms     import WeatherIconsForm, WeatherCodeForm
from .serializers import WeatherCodeSerializer


# Create your views here.
def index(request):

    buttons_main = [
        {
            "url_view": reverse("observations:weather_icon_list"),
            "url_add": reverse("observations:weather_icon_entry"),
            "image": static("/button_icons/cloudy2.png"),
            "text": "Weather Icons",
            "permission_view": "observations.view_weathericon",
            "permission_add": "observations.add_weathericon",
        },
        {
            "url_view": reverse("observations:weather_code_list"),
            "url_add": reverse("observations:weather_code_entry"),
            "image": static("/button_icons/binary-code.png"),
            "text": "Weather Codes",
            "permission_view": "observations.view_weathercode",
            "permission_add": "observations.add_weathercode",
        }
    ]

    # Add permission status to each button
    for button in buttons_main:
        button["has_permission_view"] = request.user.has_perm(button["permission_view"])
        button["has_permission_add"] = request.user.has_perm(button["permission_add"])

    context = {
        'page_name': "Weather Observations",
        'buttons_view': buttons_main,
        'buttons_add':  buttons_main,
    }
    return render(request, 'observations_home.html', context)

############# WEATHER ICONS
def weather_code_list(request, id=None):
    page_name = "Weather Codes"
    qs = WeatherCodes.objects.all().order_by('id')
    table = WeatherCodesTable(qs)
    RequestConfig(request).configure(table)
    table.empty_text = "No records available"

    context = {
        'id' : id,
        'page_name': page_name,
        'prev_page': 'Weather Observations',
        'table': table,
        'new_url': reverse('observations:weather_code_entry'),
        'back_url': reverse('observations:index'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'observations/table_list_main.html', context)

def weather_code_entry(request, id=None):

    page_name = "Weather Code Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(WeatherCodes, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = WeatherCodeForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('observations:weather_code_list', saved_entry.id)
    else:
        form = WeatherCodeForm(instance=entry)

    return render(request, 'observations/entry_form_codes.html', {
        'page_name': page_name,
        'prev_page': 'Weather Codes',
        'new_url':  reverse('observations:weather_code_entry'),
        'back_url': reverse('observations:weather_code_list'),
        'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })

############# WEATHER ICONS
def weather_icon_list(request, id=None):
    page_name = "Weather Icons"
    qs = WeatherIcons.objects.all().order_by('id')
    table = WeatherIconsTable(qs)
    RequestConfig(request).configure(table)
    table.empty_text = "No records available"

    icon_dir = Path(settings.BASE_DIR) / "static" / "weather_icons"

    allowed_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}

    icons = []

    if icon_dir.exists():
        for file in sorted(icon_dir.iterdir()):
            if file.is_file() and file.suffix.lower() in allowed_extensions:
                icons.append({
                    "name": file.name,
                    "url": f"{settings.STATIC_URL}weather_icons/{file.name}",
                    "extension": file.suffix.lower(),
                })

    context = {
        'id' : id,
        "icons": icons, 
        'page_name': page_name,
        'prev_page': 'Weather Observations',
        'table': table,
        'new_url': reverse('observations:weather_icon_entry'),
        'back_url': reverse('observations:index'),
        #'api_url': reverse('sectors-list'),
    }
    return render(request, 'observations/icon_grid.html', context)

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
            return redirect('observations:weather_icon_list')
    else:
        form = WeatherIconsForm(instance=entry)

    return render(request, 'observations/entry_form.html', {
        'page_name': page_name,
        'prev_page': 'Weather Icons',
        'new_url':  reverse('observations:weather_icon_entry'),
        'back_url': reverse('observations:weather_icon_list'),
        'api_url':  reverse('sectors-list'),
        'form': form,
        'entry': entry
    })

def weather_icon_delete(request, id):
    
    entry = get_object_or_404(WeatherIcons, id=id)

    qs = WeatherIcons.objects.all().order_by('id')
    qs = qs.order_by('id')
    
    page_name = "DELETE Weather Icon Entry"

    if request.method == "POST":
        entry.delete()
        messages.success(request, f"Record {id} deleted successfully.")
        return redirect('observations:weather_icon_list')  # redirect anywhere you prefer
        
    return render(request, "observations/parameters_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'details': qs
    })
@api_view(['GET'])
def get_weather_icon(request, code):

    try:
        weather = WeatherCodes.objects.select_related('icon_day','icon_night').get(code=code)

    except WeatherCodes.DoesNotExist:
        return Response(
            {
                'success': False,
                'message': 'Weather code not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = WeatherCodeSerializer(weather,context={'request': request})

    return Response({
        'success': True,
        'data': serializer.data
    })

class WeatherCodesViewSet(viewsets.ModelViewSet):
    queryset = WeatherCodes.objects.all().order_by("-code")
    serializer_class = WeatherCodeSerializer
    pagination_class = None
    http_method_names = ['get', 'head','options']

