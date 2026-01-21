from django.shortcuts import render, loader, get_object_or_404, redirect

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required


from django.urls import reverse
from django.http import HttpResponse

# Create your views here.

#@login_required
#@login_required
def index(request):
    template = loader.get_template('index.html')
    context = {
        'page_name': 'Home'
    }
    return HttpResponse(template.render(context))

@login_required
def user_dashboard(request):
    context = {
        'page_name': 'Home'
    }
    return render(request, 'home.html', context)

def login(request, id=None):
    page_name = "User Login"
   
    if request.method == 'POST':     
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request,form.get_user())
            return redirect('users:user_dashboard')
    else:
        form = AuthenticationForm()

    context = {
        'id' : id,
        'form': form,
        #'entry': entry,
        'page_name': page_name,
        #'table': table,
        #'new_url':  reverse('radar:radar_image_entry'),
        #'back_url': reverse('radar:radar_images_list'),
        #'api_url':  reverse('radarimages-list'),
    }
    return render(request, 'registration/login.html', context)

def user_entry(request, id=None):
    page_name = "Create New User"
   
    if request.method == 'POST':     
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('users:user_dashboard')
    else:
        form = UserCreationForm()

    context = {
        'id' : id,
        'form': form,
        #'entry': entry,
        'page_name': page_name,
        #'table': table,
        #'new_url':  reverse('radar:radar_image_entry'),
        #'back_url': reverse('radar:radar_images_list'),
        #'api_url':  reverse('radarimages-list'),
    }
    return render(request, 'entry_form_user_login.html', context)

def user_list(request, id=None):
    page_name = "Users"
    '''
    qs = RadarImages.objects.all().order_by('id')
    table = RadarImagesTable(qs)
    RequestConfig(request).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    
    if id is not None:
        entry = get_object_or_404(RadarImages, id=id)
'''
    context = {
        'id' : id,
        #'entry': entry,
        'page_name': page_name,
        #'table': table,
        #'new_url':  reverse('radar:radar_image_entry'),
        #'back_url': reverse('radar:radar_images_list'),
        #'api_url':  reverse('radarimages-list'),
    }
    return render(request, 'radar_table_list.html', context)

def logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('users:login')
