from django.urls import path
from . import views

app_name = 'system_core'

urlpatterns = [
    path('index', views.index, name='index'),

    ## DISTRICT FORECASTS: District
    path('district/list/', views.district_list, name="district_list"),
    path('district/list/<int:id>/', views.district_list, name='district_list'),
    path('district/entry/', views.district_entry, name="district_entry"),
    path('district/entry/<int:id>/', views.district_entry, name='district_entry'),
    path('district/entry/<int:id>/delete/', views.district_delete, name='district_delete'),

    ## Alert Level
    path('alert-level/list/', views.alert_level_list, name="alert_level_list"),
    path('alert-level/list/<int:id>/', views.alert_level_list, name='alert_level_list'),
    path('alert-level/entry/', views.alert_level_entry, name="alert_level_entry"),
    path('alert-level/entry/<int:id>/', views.alert_level_entry, name='alert_level_entry'),
    path('alert-level/entry/<int:id>/delete/', views.alert_level_delete, name='alert_level_delete'),

    ## Risk Level
    path('risk-level-list/', views.risk_level_list, name="risk_level_list"),
    path('risk-level-list/<int:id>/', views.risk_level_list,name='risk_level_list'),
    path('risk-level-entry/', views.risk_level_entry, name="risk_level_entry"),
    path('risk-level-entry/<int:id>/', views.risk_level_entry,name='risk_level_entry'),
    path('risk-level-entry/<int:id>/delete/', views.risk_level_delete,name='risk_level_delete'),

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