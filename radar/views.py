from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render, loader, get_object_or_404, redirect
from django.urls import reverse

from .models import RadarImages

from django.template import loader
from django_tables2 import RequestConfig

from .forms import RadarImageForm
from .models import RadarImages
from .tables import RadarImagesTable

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes

def index(request):
    template = loader.get_template('radar_home.html')
    context = {'name': 'World'}  # Data to pass to the template
    return HttpResponse(template.render(context))

@login_required
#@permission_required("radar.view_radarimages", raise_exception=True)
def radar_images_list(request, id=None):
    page_name = "Radar Images Listing"

    if not request.user.has_perm("radar.view_radarimages"):
        return render(request, 'no_permission.html', {'page_name': page_name})
    
    qs = RadarImages.objects.all().order_by('id')
    table = RadarImagesTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    
    if id is not None:
        entry = get_object_or_404(RadarImages, id=id)

    context = {
        'id' : id,
        'entry': entry,
        'page_name': page_name,
        'table': table,
        'new_url':  reverse('radar:radar_image_entry'),
        'back_url': reverse('site_home'),
        'api_url':  reverse('radarimages-list'),
    }
    return render(request, 'radar_table_list.html', context)

@permission_required("radar.add_radarimages", raise_exception=True)
def radar_image_entry(request, id=None):

    page_name = "Radar Image Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(RadarImages, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = RadarImageForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('radar:radar_images_list', saved_entry.id)
    else:
        form = RadarImageForm(instance=entry)

    return render(request, 'radar_entry_form.html', {
        'page_name': page_name,
        'new_url':  reverse('radar:radar_image_entry'),
        'back_url': reverse('radar:radar_images_list'),
        'api_url':  reverse('radarimages-list'),
        'form': form,
        'entry': entry
    })

def radar_image_delete(request, id):
    
    entry = get_object_or_404(RadarImages, id=id)
    
    page_name = "Radar Image Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('radar:radar_images_list')  # redirect anywhere you prefer

    return render(request, "radar_image_delete.html", {
        "entry": entry,
        'page_name': page_name,
    })