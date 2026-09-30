from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

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
    path('district-forecast/entry/details/<int:id>/',views.district_forecast_details_entry,name='district_forecast_details_entry'),
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
    path('district-forecast/instructions/category/list/', views.instructions_category_list, name="instructions_category_list"),
    path('district-forecast/instructions/category/list/<int:id>/', views.instructions_category_list, name='instructions_category_list'),
    path('district-forecast/instructions/category/entry/', views.instructions_category_entry, name="instructions_category_entry"),
    path('district-forecast/instructions/category/entry/<int:id>/', views.instructions_category_entry, name='instructions_category_entry'),
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

    ## GENERAL WEATHER FORECAST
    path('general-weather-forecast/list/', views.general_forecast_list, name="general_forecast_list"),
    path('general-weather-forecast/list/<int:id>/', views.general_forecast_list, name='general_forecast_list'),
    path('general-weather-forecast/entry/', views.general_forecast_entry, name="general_forecast_entry_new"),
    path('general-weather-forecast/entry/<int:id>/', views.general_forecast_entry, name='general_forecast_entry'),
    path('general-weather-forecast/entry/<int:id>/delete/', views.general_forecast_delete, name='general_forecast_delete'),
    path('general-weather-forecast/entry/<int:id>/generate-pdf/', views.general_forecast_generate_pdf, name="general_forecast_generate_pdf"),
    path('general-weather-forecast/entry/<int:id>/toggle-publish/', views.general_forecast_toggle_is_published, name='general_forecast_toggle_is_published'),
    path('general-weather-forecast/entry/<int:id>/toggle-publish-ajax/', views.general_forecast_toggle_is_published_ajax, name='general_forecast_toggle_is_published_ajax'),
    path("general-weather-forecast/<int:id>/image/",views.general_forecast_image,name="general_forecast_image"),

    path('general-weather-forecast/category/list/', views.general_forecast_category_list, name="general_forecast_category_list"),
    path('general-weather-forecast/category/list/<int:id>/', views.general_forecast_category_list, name='general_forecast_category_list'),
    path('general-weather-forecast/category/entry/', views.general_forecast_category_entry, name="general_forecast_category_entry"),
    path('general-weather-forecast/category/entry/<int:id>/', views.general_forecast_category_entry, name="general_forecast_category_entry"),
    path('general-weather-forecast/category/entry/<int:id>/delete/', views.general_forecast_category_delete, name='general_forecast_category_delete'),
    path('general-weather-forecast/import-data/', views.import_general_weather_forecast_categories, name="import_general_weather_forecast_categories"),

    ## MARINE FORECAST
    path('marine-forecast/list/', views.marine_forecast_list, name="marine_forecast_list"),
    #path('marine-forecast/category/list/<int:id>/', views.marine_forecast_category_list, name='marine_forecast_category_list'),
    path('marine-forecast/entry/', views.marine_forecast_entry, name="marine_forecast_entry"),
    path('marine-forecast/entry/<int:id>/', views.marine_forecast_entry, name="marine_forecast_entry"),
    path('marine-forecast/entry/<int:id>/delete/', views.marine_forecast_delete, name='marine_forecast_delete'),
    path('marine-forecast/entry/<int:id>/toggle-publish/', views.marine_forecast_toggle_is_published, name='marine_forecast_toggle_is_published'),
    #path("marine-forecast/import-data/", views.import_marine_forecast_categories, name="import_marine_forecast_categories"),'''
    
    
    path('marine-forecast/category/list/', views.marine_forecast_category_list, name='marine_forecast_category_list'),
    path('marine-forecast/category/entry/', views.marine_forecast_category_entry, name="marine_forecast_category_entry"),
    path('marine-forecast/category/entry/<int:id>/', views.marine_forecast_category_entry, name="marine_forecast_category_entry"),
    #path('marine-forecast/category/entry/<int:id>/delete/', views.general_forecast_category_delete, name='general_forecast_category_delete'),
    #path('marine-forecast/import-data/', views.import_general_weather_forecast_categories, name="import_general_weather_forecast_categories"),

    path('marine-forecast/details-category/list/', views.marine_forecast_details_category_list, name='marine_forecast_details_category_list'),
    path('marine-forecast/details-category/list/<int:id>/', views.marine_forecast_details_category_list, name='marine_forecast_details_category_list'),
    path('marine-forecast/details-category/entry/', views.marine_forecast_details_category_entry, name="marine_forecast_details_category_entry"),
    path('marine-forecast/details-category/entry/<int:id>/', views.marine_forecast_details_category_entry, name="marine_forecast_details_category_entry_id"),
    path('marine-forecast/details-category/entry/<int:id>/delete/', views.marine_forecast_details_category_delete, name='marine_forecast_details_category_delete'),


    path('marine-forecast/wind-direction/list/', views.wind_direction_list, name='wind_direction_list'),
    path('marine-forecast/wind-direction/list/<int:id>/', views.wind_direction_list, name='wind_direction_list'),
    path('marine-forecast/wind-direction/entry/', views.wind_direction_entry, name="wind_direction_entry"),
    path('marine-forecast/wind-direction/entry/<int:id>/', views.wind_direction_entry, name="wind_direction_entry"),
    path('marine-forecast/wind-direction/<int:id>/delete/', views.wind_direction_delete, name='wind_direction_delete'),

    path('marine-forecast/wind-condition/list/', views.wind_condition_list, name='wind_condition_list'),
    path('marine-forecast/wind-condition/list/<int:id>/', views.wind_condition_list, name='wind_condition_list'),
    path('marine-forecast/wind-condition/entry/', views.wind_condition_entry, name="wind_condition_entry"),
    path('marine-forecast/wind-condition/entry/<int:id>/', views.wind_condition_entry, name="wind_condition_entry"),
    path('marine-forecast/wind-condition/<int:id>/delete/', views.wind_condition_delete, name='wind_condition_delete'),

    path('marine-forecast/tides/<int:id>/delete/', views.tide_delete, name='tide_delete'),

    path('marine-forecast/tide/level/category/list/', views.tide_level_category_list, name='tide_level_category_list'),
    path('marine-forecast/tide/level/category/list/', views.tide_level_category_list, name='tide_level_category_list'),
    path('marine-forecast/tide/level/category/entry/', views.tide_level_category_entry, name="tide_level_category_entry"),
    path('marine-forecast/tide/level/category/entry/<int:id>/', views.tide_level_category_entry, name="tide_level_category_entry"),
    path('marine-forecast/tide/level/category/<int:id>/delete/', views.tide_level_category_delete, name='tide_level_category_delete'),

    path('marine-forecast/tide/day/category/list/', views.tide_day_category_list, name='tide_day_category_list'),
    path('marine-forecast/tide/day/category/list/', views.tide_day_category_list, name='tide_day_category_list'),
    path('marine-forecast/tide/day/category/entry/', views.tide_day_category_entry, name="tide_day_category_entry"),
    path('marine-forecast/tide/day/category/entry/<int:id>/', views.tide_day_category_entry, name="tide_day_category_entry"),
    path('marine-forecast/tide/day/category/<int:id>/delete/', views.tide_day_category_delete, name='tide_day_category_delete'),


    path('marine-forecast/sun/day/category/list/', views.sun_day_category_list, name='sun_day_category_list'),
    path('marine-forecast/sun/day/category/list/<int:id>/', views.sun_day_category_list, name='sun_day_category_list'),
    path('marine-forecast/sun/day/category/entry/', views.sun_day_category_entry, name="sun_day_category_entry"),
    path('marine-forecast/sun/day/category/entry/<int:id>/', views.sun_day_category_entry, name="sun_day_category_entry"),
    path('marine-forecast/sun/day/category/<int:id>/delete/', views.sun_day_category_delete, name='sun_day_category_delete'),
    
    path('marine-forecast/sun/move/category/list/', views.sun_move_category_list, name='sun_move_category_list'),
    path('marine-forecast/sun/move/category/list/<int:id>/', views.sun_move_category_list, name='sun_move_category_list'),
    path('marine-forecast/sun/move/category/entry/', views.sun_move_category_entry, name="sun_move_category_entry"),
    path('marine-forecast/sun/move/category/entry/<int:id>/', views.sun_move_category_entry, name="sun_move_category_entry"),
    path('marine-forecast/sun/move/category/<int:id>/delete/', views.sun_move_category_delete, name='sun_move_category_delete'),

    path("marine-forecast/sun/inline-update/",views.sun_inline_update,name="sun_inline_update"),
    path("marine-forecast/sun/inline-update/<int:id>/",views.sun_inline_update,name="sun_inline_update"),

    path('marine-forecast/moon/day/category/list/', views.moon_day_category_list, name='moon_day_category_list'),
    path('marine-forecast/moon/day/category/list/', views.moon_day_category_list, name='moon_day_category_list'),
    path('marine-forecast/moon/day/category/entry/', views.moon_day_category_entry, name="moon_day_category_entry"),
    path('marine-forecast/moon/day/category/entry/<int:id>/', views.moon_day_category_entry, name="moon_day_category_entry"),
    path('marine-forecast/moon/day/category/<int:id>/delete/', views.moon_day_category_delete, name='moon_day_category_delete'),

    path('marine-forecast/moon/move/category/list/', views.moon_move_category_list, name='moon_move_category_list'),
    path('marine-forecast/moon/move/category/list/', views.moon_move_category_list, name='moon_move_category_list'),
    path('marine-forecast/moon/move/category/entry/', views.moon_move_category_entry, name="moon_move_category_entry"),
    path('marine-forecast/moon/move/category/entry/<int:id>/', views.moon_move_category_entry, name="moon_move_category_entry"),
    path('marine-forecast/moon/move/category/<int:id>/delete/', views.moon_move_category_delete, name='moon_move_category_delete'),

    path("marine-forecast/moon/inline-update/",views.moon_inline_update,name="moon_inline_update"),
    path("marine-forecast/moon/inline-update/<int:id>/",views.moon_inline_update,name="moon_inline_update"),

    path('marine-forecast/details/entry/', views.marine_forecast_details_entry, name="marine_forecast_details_entry"),
    path('marine-forecast/details/entry/<int:id>/', views.marine_forecast_details_entry, name="marine_forecast_details_entry"),
    path("marine-forecast/details/inline-update/",views.marine_forecast_details_inline_update,name="marine_forecast_details_inline_update"),
    path("marine-forecast/details/inline-update/<int:id>/",views.marine_forecast_details_inline_update,name="marine_forecast_details_inline_update"),
    path("marine-forecast/tides/inline-update/",views.marine_forecast_tides_inline_update,name="marine_forecast_tides_inline_update"),
    path("marine-forecast/tides/inline-update/<int:id>/",views.marine_forecast_tides_inline_update,name="marine_forecast_tides_inline_update"),

    ## FORECAST DISCUSSION
    path('forecast-discussion/list/', views.discussion_list, name="discussion_list"),
    path('forecast-discussion/entry/', views.discussion_entry, name="discussion_entry"),
    path('forecast-discussion/entry/<int:id>/', views.discussion_entry, name="discussion_entry"),
    path('forecast-discussion/entry/<int:id>/delete/', views.discussion_delete, name='discussion_delete'),

    #path('district-forecast/forecast-entry/<int:fk>/details/entry/',views.district_forecast_details_entry,name='district_forecast_details_entry'),
    #path('district-forecast/forecast-entry/<int:fk>/details/entry/<int:id>/',views.district_forecast_details_entry,name='district_forecast_details_entry'),
    #path('district-forecast/forecast-entry/<int:id>/details/',views.district_forecast_details_entry,name='district_forecast_details_entry'),
    #path('district-forecast/forecast-entry/<int:fk>/details/<int:id>/delete/',views.district_forecast_details_delete,name='district_forecast_details_delete'),
    #path('district-forecast/entry/<int:fk>/item/<int:id>/',views.district_forecast_details_entry_item,name='district_forecast_details_entry_item'),

    
]