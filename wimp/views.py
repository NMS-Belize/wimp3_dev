from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from django.templatetags.static import static

from rest_framework.decorators import api_view
from rest_framework.response import Response

from company.models import Company

def index(request):
    template = loader.get_template('entry_form_user_login.html')
    context = {'page_name': 'Home'}  
    return HttpResponse(template.render(context))

@login_required
def dashboard(request):

    id = 1

    if id:
        entry = get_object_or_404(Company, id=id)
    else:
        entry = None

    buttons_top = [
            {
                "url_view": "https://wimp.nms.gov.bz/",
                "image": static("/app_icons/wimp_thumb.png"),
                "text": "WIMP 2.0"
            },
            {
                "url_view": "https://nms.gov.bz/",
                "image": static("/app_icons/nms_logo.png"),
                "text": "NMS Website [LIVE]"
            },
            {
                "url_view": "https://website.nmsapps.gov.bz/",
                "image": static("/button_icons/world-wide-web.png"),
                "text": "NMS Website [TEST]"
            },
            {
                "url_view": "http://192.168.3.87",
                "image": static("/app_icons/radar_thumb.png"),
                "text": "Radar Imagery Display"
            }
        ]
            
    buttons_main = [
        {
            "url_view": reverse("forecasts:index"),
            #"url_add": reverse("observations:weather_icon_entry"),
            "image": static("/button_icons/atmospheric-conditions.png"),
            "text": "Weather Forecasts",
            "permission_view": "observations.view_weathericons",
            #"permission_add": "observations.add_weathericons",
        },
        {
            "url_view": reverse("observations:index"),
            "url_add": reverse("observations:weather_icon_entry"),
            "image": static("/button_icons/cloudy.png"),
            "text": "Weather Observations",
            "permission_view": "observations.view_weathericons",
            #"permission_add": "observations.add_weathericons",
        },
        {
            "url_view": reverse("alerts:index"),
            #"url_add": reverse("observations:weather_code_entry"),
            "image": static("/button_icons/rain-burst.png"),
            "text": "Weather Alerts",
            "permission_view": "alerts.view_capalerts",
            #"permission_add": "observations.add_weathercodes",
        },
        {
            "url_view": reverse("agro:index"),
            #"url_add": reverse("observations:weather_code_entry"),
            "image": static("/button_icons/agriculture.png"),
            "text": "Agricultural Services",
            "permission_view": "agro.view_pestrisk",
            #"permission_add": "observations.add_weathercodes",
        },
        {
            "url_view": reverse("radar:index"),
            #"url_add": reverse("radar:radar_images_list"),
            "image": static("/button_icons/radar.png"),
            "text": "Radar Images",
            "permission_view": "radar.view_radarimages",
            #"permission_add": "observations.add_weathercodes",
        }
    ]

    # Add permission status to each button
    for button in buttons_main:
        button["has_permission_view"] = request.user.has_perm(button["permission_view"])
        #button["has_permission_add"] = request.user.has_perm(button["permission_add"])

    context = {
        'page_name': 'Dashboard',
        'entry': entry,
        'buttons_view': buttons_main,
        'buttons_top':  buttons_top,
    }
    return render(request, 'dashboard.html', context)