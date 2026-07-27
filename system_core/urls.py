from django.urls import path
from . import views

app_name = 'system_core'

urlpatterns = [
    path('index', views.index, name='index'),
    path('job-title/list/', views.job_title_list, name="job_title_list"),
    path('job-title/entry/', views.job_title_entry, name="job_title_entry"),
    path('job-title/entry/<int:id>/', views.job_title_entry, name="job_title_entry"),
    #path('job-title/entry/', views.job_title_entry, name="job_title_entry"),
    path('job-title/delete/<int:id>/', views.job_title_delete, name="job_title_delete"),

    path('department/list/', views.department_section_list, name="department_section_list"),
    path('department/list/<int:id>', views.department_section_list, name="department_section_list"),
    path('department/entry/', views.department_section_entry, name="department_section_entry"),
    path('department/entry/<int:id>/', views.department_section_entry, name="department_section_entry"),
    path('department/entry/<int:id>/delete/', views.department_section_delete, name='department_section_delete'),

    path('office-location/list/', views.office_location_list, name="office_location_list"),
    path('office-location/list/<int:id>/', views.office_location_list, name="office_location_list"),
    path('office-location/entry/', views.office_location_entry, name="office_location_entry"),
    path('office-location/entry/<int:id>/', views.office_location_entry, name="office_location_entry"),
    path('office-location/entry/<int:id>/delete/', views.office_location_delete, name='office_location_delete'),
]