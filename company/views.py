from django.shortcuts import render
from django.urls import reverse
from django_tables2 import RequestConfig
from django.shortcuts import render, redirect, get_object_or_404

from company.forms import CompanyForm
from company.models import Company
from company.tables import CompanyTable

# Create your views here.
def index(request):
    context = {
        'page_name': "Company Dashboard",
    }
    return render(request, 'table_list_main.html', context)


############# COMPANY ENTRIES: #############
def company_list(request, id=None):

    page_name = "Companies"
    qs = Company.objects.order_by(
            #"category__category_name",
            "company_name",
        )

    table = CompanyTable(qs)
    table.empty_text = "No records available"
    RequestConfig(request).configure(table)

    context = {
        #'id' : id,
        #'entry': entry,  
        'page_name': page_name,
        'prev_page': 'System Parameters',
        'table': table,
        'new_url':      reverse('company:company_entry'),
        #'back_url': reverse('forecasts:index'),
        #'api_url': "/api/pest-risk/",
    }
    return render(request, 'table_list_main.html', context)

def company_entry(request, id=None):

    page_name = "Company Entry"

    # If id exists => update, else => create new
    if id:
        entry = get_object_or_404(Company, id=id)
    else:
        entry = None

    if request.method == 'POST':

        form = CompanyForm(request.POST, request.FILES, instance=entry)

        if form.is_valid():

            # Temporarily remove uploaded logo
            logo = request.FILES.get("logo")

            company = form.save(commit=False)

            # CREATE
            if entry is None:

                # Temporarily remove logo so company gets an ID first
                company.logo = None

                company.created_by = request.user
                company.updated_by = request.user

                company.save()

                # Now company.id exists
                if logo:
                    company.logo.save(
                        logo.name,
                        logo,
                        save=True
                    )

            # UPDATE
            else:

                company.updated_by = request.user

                # Save normally.
                # Since company already has an ID,
                # upload_to can use company/<id>/
                company.save()

            return redirect(
                "company:company_list"
            )
        
    else:
        form = CompanyForm(instance=entry)

    return render(request, 'company/entry_form.html', {
        'page_name':    page_name,
        'prev_page':    'Company List',
        'new_url':      reverse('company:company_entry'),
        'back_url':     reverse('company:company_list'),
        #'api_url':      "/api/pest-risk/",
        'form': form,
        'entry': entry
    })