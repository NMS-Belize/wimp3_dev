
from django.shortcuts import render, loader, get_object_or_404, redirect

from django.contrib import messages
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.http import HttpResponse, request
from django_tables2 import RequestConfig

from users.forms import UserEntryForm, UserProfileForm
from users.models import UserProfile
from users.tables import UserTable

User = get_user_model()

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
            #return redirect('users:user_dashboard')
            return redirect('site_home')
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

    form = UserCreationForm(request.POST or None)

    # Customize the form once
    form.fields["username"].label = "Username"
    form.fields["password1"].help_text = ""
    form.fields["password2"].help_text = ""

    for field in form.fields.values():
        field.widget.attrs.update({"class": "form-control"})
   
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(request,"User account created. Enter the remaining user details.")
        return redirect('users:user_entry_details', id=user.id)

    context = {
        'id' : id,
        'form': form,
        'page_name': page_name,
        #'new_url':  reverse('radar:radar_image_entry'),
        #'back_url': reverse('radar:radar_images_list'),
        #'api_url':  reverse('radarimages-list'),
    }
    return render(request, 'entry_form_new_user.html', context)

def user_entry_details(request, id=None):

    page_name = "User Entry Details"

    user = get_object_or_404(User, pk=id)
    profile, created = UserProfile.objects.get_or_create(user=user)

    user_form       = UserEntryForm(request.POST or None, instance=user)
    profile_form    = UserProfileForm(request.POST or None,request.FILES or None, instance=profile)

    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"User details updated successfully.")
            return redirect('users:user_list')

    context = {
        'id' : id,
        "user_form": user_form,
        "profile_form": profile_form,
        #'entry': entry,
        'page_name': page_name,
        #'new_url':  reverse('radar:radar_image_entry'),
        'back_url': reverse('users:user_list'),
        #'api_url':  reverse('radarimages-list'),
    }
    return render(request, 'entry_form_user_profile.html', context)
        
def user_list(request, id=None):
    page_name = "Users"
    qs = User.objects.all().order_by('id')
    table = UserTable(qs)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)

    # Load entry ONLY if id is provided
    entry = None
    
    if id is not None:
        entry = get_object_or_404(User, id=id)

    context = {
        'id' : id,
        #'entry': entry,
        'page_name': page_name,
        'table': table,
        'new_url':  reverse('users:user_entry'),
        'back_url': reverse('users:user_list'),
        #'api_url':  reverse('radarimages-list'),
    }
    return render(request, 'table_list_main.html', context)

#@login_required
def user_delete(request, id):
    
    entry = get_object_or_404(User, id=id)
    page_name = "User"

    if request.method == "POST":

        if entry.is_superuser:
            messages.error(request, "Superuser accounts cannot be deleted.")
            return redirect("users:user_list")

        username = entry.username
        entry.delete()
        messages.success(request, f"Record {entry.username} was deleted successfully.")
        return redirect('users:user_list')
    
    return render(request, "users/user_delete.html", {
        "entry": entry,
        'page_name': page_name,
        'back_url': reverse('users:user_list'),
    })

def user_active_toggle(request, id):
    record = get_object_or_404(User, id=id)

    if not record.is_active:
        # Deactivate ALL records first
        #User.objects.filter(is_active=True).update(is_active=False)

        # Activate selected
        record.is_active = True
        status = "activated"
    else:
        # If already activated → deactivate it
        record.is_active = False
        status = "deactivated"

    record.save(update_fields=["is_active"])

    messages.success(request, f"Record {status} successfully.")
    return redirect("users:user_list")

def logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('users:login')
