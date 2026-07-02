from django.urls import path
from . import views

app_name = 'forecasts'

urlpatterns = [
    path('index', views.index, name='index'),
    #path('new/', views.inventory_entry, name='inventory_entry'),
    #path('edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),

    ## DISTRICT FORECASTS: District
    path('district-forecast/district/list/', views.district_list, name="district_list"),
    path('district-forecast/district/list/<int:id>/', views.district_list, name='district_list'),
    path('district-forecast/district/entry/', views.district_entry, name="district_entry"),
    path('district-forecast/district/entry/<int:id>/', views.district_entry, name='district_entry'),
    path('district-forecast/district/entry/<int:id>/delete/', views.district_delete, name='district_delete'),

    ## DISTRICT FORECASTS: Alert Level
    path('district-forecast/alert-level/list/', views.alert_level_list, name="alert_level_list"),
    path('district-forecast/alert-level/list/<int:id>/', views.alert_level_list, name='alert_level_list'),
    path('district-forecast/alert-level/entry/', views.alert_level_entry, name="alert_level_entry"),
    path('district-forecast/alert-level/entry/<int:id>/', views.alert_level_entry, name='alert_level_entry'),
    path('district-forecast/alert-level/entry/<int:id>/delete/', views.alert_level_delete, name='alert_level_delete'),

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

    ## DISTRICT FORECASTS: Risk Level
    path('district-forecast/risk-level-list/', views.risk_level_list, name="risk_level_list"),
    path('district-forecast/risk-level-list/<int:id>/', views.risk_level_list,name='risk_level_list'),
    path('district-forecast/risk-level-entry/', views.risk_level_entry, name="risk_level_entry"),
    path('district-forecast/risk-level-entry/<int:id>/', views.risk_level_entry,name='risk_level_entry'),
    path('district-forecast/risk-level-entry/<int:id>/delete/', views.risk_level_delete,name='risk_level_delete'),

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

    ## DISTRICT FORECASTS: District Forecast
    path('district-forecast/list/', views.district_forecast_list, name="district_forecast_list"),
    path('district-forecast/list/<int:id>/', views.district_forecast_list,name='district_forecast_list'),

    path('district-forecast/entry/', views.district_forecast_entry, name="district_forecast_entry"),
    path('district-forecast/entry/<int:id>/', views.district_forecast_entry,name='district_forecast_entry'),
    path('district-forecast/entry/<int:id>/delete/', views.district_forecast_delete,name='district_forecast_delete'),
    path('district-forecast/entry/<int:id>/toggle-publish/', views.district_forecast_toggle_is_published, name='district_forecast_toggle_is_published'),
    path('district-forecast/entry/<int:id>/toggle-publish-ajax/', views.district_forecast_toggle_is_published_ajax, name='district_forecast_toggle_is_published_ajax'),

    path('district-forecast/entry/<int:id>/generate-pdf/', views.generate_pdf, name="generate_pdf"),

    path('district-forecast/entry/<int:id>/details/',views.district_forecast_details_entry,name='district_forecast_details_entry'),
    path('district-forecast/entry/<int:fk>/item/<int:id>/', views.district_forecast_details_entry_item, name='district_forecast_details_entry_item'),

    path('district-forecast/entry/details-list/',           views.district_forecast_details_list, name="district_forecast_details_list"),
    path('district-forecast/entry/details-list/<int:id>/',  views.district_forecast_details_list, name="district_forecast_details_list_id"),

    #path('district-forecast/forecast-entry/<int:fk>/details/entry/',views.district_forecast_details_entry,name='district_forecast_details_entry'),
    #path('district-forecast/forecast-entry/<int:fk>/details/entry/<int:id>/',views.district_forecast_details_entry,name='district_forecast_details_entry'),
    #path('district-forecast/forecast-entry/<int:id>/details/',views.district_forecast_details_entry,name='district_forecast_details_entry'),
    #path('district-forecast/forecast-entry/<int:fk>/details/<int:id>/delete/',views.district_forecast_details_delete,name='district_forecast_details_delete'),
    #path('district-forecast/entry/<int:fk>/item/<int:id>/',views.district_forecast_details_entry_item,name='district_forecast_details_entry_item'),
]