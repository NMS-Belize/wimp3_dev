
from django.shortcuts import render, loader, get_object_or_404, redirect

from django.contrib import messages
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.http import HttpResponse, request, JsonResponse
from django_tables2 import RequestConfig

from users.forms import UserEntryForm, UserProfileForm, EmployeeForm
from users.models import UserProfile, Employee
from users.tables import UserTable, EmployeeTable

User = get_user_model()

# Create your views here.
def index(request):
    context = {
        'page_name': 'User Dashboard',
    }
    return render(request, 'home_users.html', context)

@login_required
def user_dashboard(request):
    context = {
        'page_name': 'Home'
    }
    return render(request, 'home.html', context)

def login(request, id=None):

    page_name = "User Login"

    # User is already logged in
    if request.user.is_authenticated:
        return redirect('site_home')  # Replace with your URL name
   
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
        'prev_page': 'User Dashboard',
        'table': table,
        'new_url':  reverse('users:user_entry'),
        'back_url': reverse('users:index'),
        #'api_url':  reverse('radarimages-list'),
    }
    return render(request, 'table_list_users.html', context)

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

def employee_list(request, id=None):

    page_name   = "Employee List"
    qs          = Employee.objects.all().order_by('id')
    table       = EmployeeTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request, paginate={"per_page": 25}).configure(table)

    context = {
        'id' : id,
        'page_name': page_name,
        'prev_page': 'User Dashboard',
        'table': table,
        'new_url':  reverse('users:employee_entry'),
        'back_url': reverse('users:index'),
        #'api_url':  reverse('radarimages-list'),
    }
    return render(request, 'table_list_users.html', context)

def employee_entry(request, id=None):

    page_name = "Employee Entry"

    if id:
        entry = get_object_or_404(Employee, id=id)
    else:
        entry = None

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=entry)

        if form.is_valid():
            saved_entry = form.save()    # Creates or updates
            return redirect('users:employee_list', saved_entry.id)
        else:
            print(form.errors)  # check terminal
    else:
        form = EmployeeForm(instance=entry)

    return render(request, 'employees/entry_form.html', {
        'page_name':    page_name,
        'prev_page':    'Employee List',
        'new_url':      reverse('users:employee_entry'),
        'back_url':     reverse('users:employee_list'),
        'form':         form,
        'entry':        entry
    })

def employee_delete(request, id):
    
    entry = get_object_or_404(Employee, id=id)

    qs = Employee.objects.all().order_by('id')
    qs = qs.order_by('id')
    
    page_name = "Employee Entry"

    if request.method == "POST":
        entry.delete()
        return redirect('users:employee_list')  # redirect anywhere you prefer

    return render(request, "employees/entry_delete.html", {
        'entry':        entry,
        'page_name':    page_name,
        'back_url':     reverse('users:employee_list'),
    })

def user_profile_data(request, user_id):

    user    = get_object_or_404(User, id=user_id)
    #profile = getattr(user, "userprofile", None)

    return JsonResponse({
        #"first_name": user.first_name or "",
        #"last_name": user.last_name or "",
        "email": user.email or "",
        "phone": user.phone if user else "",
        "department": user.department_id if user and user.department else "",
        "job_title": user.job_title_id if user and user.job_title else "",
        #"office_location": user.office_location_id if profile and profile.office_location else "",
    })