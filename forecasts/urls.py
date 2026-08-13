from django.urls import path
from . import views
from forecasts.views import WIMP2FilesAPIView

app_name = 'forecasts'

urlpatterns = [
    path('index', views.index, name='index'),
    #path('new/', views.inventory_entry, name='inventory_entry'),
    #path('edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),

    ## DISTRICT FORECASTS
    path('district-forecast/list/', views.district_forecast_list, name="district_forecast_list"),
    path('district-forecast/list/<int:id>/', views.district_forecast_list,name='district_forecast_list'),

    path('district-forecast/entry/', views.district_forecast_entry, name="district_forecast_entry"),
    path('district-forecast/entry/<int:id>/', views.district_forecast_entry,name='district_forecast_entry'),
    path('district-forecast/entry/<int:id>/delete/', views.district_forecast_delete,name='district_forecast_delete'),
    path('district-forecast/entry/<int:id>/generate-pdf/', views.district_forecast_generate_pdf, name="district_forecast_generate_pdf"),
    path('district-forecast/entry/<int:id>/toggle-publish/', views.district_forecast_toggle_is_published, name='district_forecast_toggle_is_published'),
    path('district-forecast/entry/<int:id>/toggle-publish-ajax/', views.district_forecast_toggle_is_published_ajax, name='district_forecast_toggle_is_published_ajax'),

    path('district-forecast/entry/<int:fk>/item/<int:id>/', views.district_forecast_details_entry_item, name='district_forecast_details_entry_item'),

    ## DISTRICT FORECASTS: Details
    path('district-forecast/entry/<int:id>/details/',views.district_forecast_details_entry,name='district_forecast_details_entry'),
    path('district-forecast/entry/details-list/',           views.district_forecast_details_list, name="district_forecast_details_list"),
    path('district-forecast/entry/details-list/<int:id>/',  views.district_forecast_details_list, name="district_forecast_details_list_id"),
    
    ## DISTRICT FORECASTS: Instructions
    path('district-forecast/instructions/list/', views.instructions_list, name="instructions_list"),
    path('district-forecast/instructions/list/<int:id>/', views.instructions_list, name='instructions_list'),
    path('district-forecast/instructions/entry/', views.instructions_entry, name="instructions_entry"),
    path('district-forecast/instructions/entry/<int:id>/', views.instructions_entry, name='instructions_entry'),
    path('district-forecast/instructions/entry/<int:id>/delete/', views.instructions_delete, name='instructions_delete'),

    path("district-forecast/instructions/ajax/add/", views.district_forecast_instructions_ajax_add,name="district_forecast_instructions_ajax_add"),

    ## DISTRICT FORECASTS: Instructions Category
    path('district-forecast/instructions-category/list/', views.instructions_category_list, name="instructions_category_list"),
    path('district-forecast/instructions-category/list/<int:id>/', views.instructions_category_list, name='instructions_category_list'),
    path('district-forecast/instructions-category/entry/', views.instructions_category_entry, name="instructions_category_entry"),
    path('district-forecast/instructions-category/entry/<int:id>/', views.instructions_category_entry, name='instructions_category_entry'),
    #path('district-forecast/instructions-category/entry/<int:id>/delete/', views.instructions_category_delete, name='instructions_category_delete'),

    ## DISTRICT FORECASTS: Severity
    path('district-forecast/severity-list/', views.severity_list, name="severity_list"),
    path('district-forecast/severity-list/<int:id>/', views.severity_list,name='severity_list'),
    path('district-forecast/severity-entry/', views.severity_entry, name="severity_entry"),
    path('district-forecast/severity-entry/<int:id>/', views.severity_entry,name='severity_entry'),
    path('district-forecast/severity-entry/<int:id>/delete/', views.severity_delete,name='severity_delete'),

    ## DISTRICT FORECASTS: Probability
    path('district-forecast/probability-list/', views.probability_list, name="probability_list"),
    path('district-forecast/probability-list/<int:id>/', views.probability_list,name='probability_list'),
    path('district-forecast/probability-entry/', views.probability_entry, name="probability_entry"),
    path('district-forecast/probability-entry/<int:id>/', views.probability_entry,name='probability_entry'),
    path('district-forecast/probability-entry/<int:id>/delete/', views.probability_delete,name='probability_delete'),

    ## GENERAL WEATHER FORECASTS: District
    path('general-weather-forecast/list/', views.general_forecast_list, name="general_forecast_list"),
    path('general-weather-forecast/list/<int:id>/', views.general_forecast_list, name='general_forecast_list'),
    path('general-weather-forecast/entry/', views.general_forecast_entry, name="general_forecast_entry"),
    path('general-weather-forecast/entry/<int:id>/', views.general_forecast_entry, name='general_forecast_entry'),
    #path('general-weather-forecast/entry/<int:id>/delete/', views.general_forecast_delete, name='general_forecast_delete'),

    path('general-weather-forecast/category/list/', views.general_forecast_category_list, name="general_forecast_category_list"),
    path('general-weather-forecast/category/list/<int:id>/', views.general_forecast_category_list, name='general_forecast_category_list'),
    path('general-weather-forecast/category/entry/', views.general_forecast_category_entry, name="general_forecast_category_entry"),
    path('general-weather-forecast/category/entry/<int:id>/', views.general_forecast_category_entry, name="general_forecast_category_entry"),
    path('general-weather-forecast/category/entry/<int:id>/delete/', views.general_forecast_category_delete, name='general_forecast_category_delete'),
    path("general-weather-forecast/import-data/", views.import_general_weather_forecast_categories, name="import_general_weather_forecast_categories"),

    
    

    #path('district-forecast/forecast-entry/<int:fk>/details/entry/',views.district_forecast_details_entry,name='district_forecast_details_entry'),
    #path('district-forecast/forecast-entry/<int:fk>/details/entry/<int:id>/',views.district_forecast_details_entry,name='district_forecast_details_entry'),
    #path('district-forecast/forecast-entry/<int:id>/details/',views.district_forecast_details_entry,name='district_forecast_details_entry'),
    #path('district-forecast/forecast-entry/<int:fk>/details/<int:id>/delete/',views.district_forecast_details_delete,name='district_forecast_details_delete'),
    #path('district-forecast/entry/<int:fk>/item/<int:id>/',views.district_forecast_details_entry_item,name='district_forecast_details_entry_item'),
]