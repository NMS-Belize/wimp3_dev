from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from rest_framework import serializers
from rest_framework.routers import DefaultRouter
from agro.views import CommodityTypeViewSet

from . import views

app_name = 'agro'

urlpatterns = [
    path("", views.index, name="index"),

    ## PEST RISK ENTRY
    path("pest-risk/pest-risk-list/", views.pest_risk_list, name="pest_risk_list"),
    path('pest-risk-list/<int:id>/', views.pest_risk_list,name='pest_risk_list'),

    path("pest-risk-entry/", views.pest_risk_entry, name="pest_risk_entry"),    
    path('pest-risk-entry/<int:id>/', views.pest_risk_entry, name='pest_risk_entry'),
    path('pest-risk-enrty/<int:id>/delete/', views.pest_risk_delete,name='pest_risk_delete'),

    path("pest-risk-entry/details-list/", views.pest_risk_details_list, name="pest_risk_details_list"),
    path("pest-risk-entry/details-list/<int:id>/", views.pest_risk_details_list, name="pest_risk_details_list"),
    path('pest-risk-entry/<int:fk>/details/entry/',views.pest_risk_details_create,name='pest_risk_details_create'),
    path('pest-risk-entry/<int:fk>/details/<int:id>/',views.pest_risk_details_entry,name='pest_risk_details_entry'),
    path('pest-risk-entry/<int:fk>/details/<int:id>/delete/',views.pest_risk_details_delete,name='pest_risk_details_delete'),

    path('pest-risk-entry/<int:fk>/details/<int:id>/duplicate/', views.pest_risk_details_entry_duplicate,name='pest_risk_details_entry_duplicate'),
    path('pest-risk-entry/<int:id>/toggle-publish/',views.pest_risk_toggle_is_published,name='pest_risk_toggle_is_published'),

    #path("pest-risk-entry/add/", views.pest_risk_entry_add, name="pest_risk_entry_add"),
    #path("pest-risk-entry/update/", views.pest_risk_entry_update, name="pest_risk_entry_update"), 
    #path('pest-risk-entry/<int:entry_id>/add/', views.pest_risk_add_details, name='pest_risk_add_details'),
    
    ## PEST RISK VARIABLE: Zone Area
    path("pest-risk/sector-list/", views.sector_list, name="sector_list"),
    path('pest-risk/sector-list/<int:id>/', views.sector_list,name='sector_list'),
    path("pest-risk/sector-entry/", views.sector_entry, name="sector_entry"),
    path('pest-risk/sector-entry/<int:id>/', views.sector_entry,name='sector_entry'),
    path('pest-risk/sector-entry/<int:id>/delete/', views.sector_delete,name='sector_delete'),

    ## PEST RISK VARIABLE: Zone Area
    path("pest-risk/zone-area-list/", views.zone_area_list, name="zone_area_list"),
    path('pest-risk/zone-area-list/<int:id>/', views.zone_area_list,name='zone_area_list'),
    path("pest-risk/zone-area-entry/", views.zone_area_entry, name="zone_area_entry"),
    path('pest-risk/zone-area-entry/<int:id>/', views.zone_area_entry,name='zone_area_entry'),
    path('pest-risk/zone-area-entry/<int:id>/delete/', views.zone_area_delete,name='zone_area_delete'),

    ## PEST RISK VARIABLE: District/Zone
    path("pest-risk/district-zone-list/", views.district_zone_list, name="district_zone_list"),
    path('pest-risk/district-zone-list/<int:id>/', views.district_zone_list,name='district_zone_list'),
    path("pest-risk/district-zone-entry/", views.district_zone_entry, name="district_zone_entry"),
    path('pest-risk/district-zone-entry/<int:id>/', views.district_zone_entry,name='district_zone_entry'),
    path('pest-risk/district-zone-entry/<int:id>/delete/', views.district_zone_delete,name='district_zone_delete'),

    ## PEST RISK VARIABLE: Commodity
    path("pest-risk/commodity-list/", views.commodity_list, name="commodity_list"),
    path('pest-risk/commodity-list/<int:id>/', views.commodity_list,name='commodity_list'),
    path("pest-risk/commodity-entry/", views.commodity_entry, name="commodity_entry"),
    path('pest-risk/commodity-entry/<int:id>/', views.commodity_entry,name='commodity_entry'),
    path('pest-risk/commodity-entry/<int:id>/delete/', views.commodity_type_delete,name='commodity_type_delete'),

    ## PEST RISK VARIABLE: Pest Alert Level
    path("pest-risk/pest-alert-level-list/", views.pest_alert_level_list, name="pest_alert_level_list"),
    path('pest-risk/pest-alert-level-list/<int:id>/', views.pest_alert_level_list,name='pest_alert_level_list'),
    path("pest-risk/pest-alert-level-entry/", views.pest_alert_level_entry, name="pest_alert_level_entry"),
    path('pest-risk/pest-alert-level-entry/<int:id>/', views.pest_alert_level_entry,name='pest_alert_level_entry'),
    path('pest-risk/pest-alert-level-entry/<int:id>/delete/', views.pest_alert_level_delete,name='pest_alert_level_delete'),

    ## PEST RISK VARIABLE: Drought Alert Level
    path("pest-risk/drought-alert-level-list/", views.drought_alert_level_list, name="drought_alert_level_list"),
    path('pest-risk/drought-alert-level-list/<int:id>/', views.drought_alert_level_list,name='drought_alert_level_list'),
    path("pest-risk/drought-alert-level-entry/", views.drought_alert_level_entry, name="drought_alert_level_entry"),
    path('pest-risk/drought-alert-level-entry/<int:id>/', views.drought_alert_level_entry,name='drought_alert_level_entry'),
    path('pest-risk/drought-alert-level-entry/<int:id>/delete/', views.drought_alert_level_delete,name='drought_alert_level_delete'),

    ## PEST RISK VARIABLE: Action Items
    path("pest-risk/action-items-list/", views.action_items_list, name="action_items_list"),
    path('pest-risk/action-items-list/<int:id>/', views.action_items_list,name='action_items_list'),
    path("pest-risk/action-items-entry/", views.action_items_entry, name="action_items_entry"),
    path('pest-risk/action-items-entry/<int:id>/', views.action_items_entry,name='action_items_entry'),
    path('pest-risk/action-items-entry/<int:id>/delete/', views.action_items_delete,name='action_items_delete'),
    path('pest-risk/action-items-entry/<int:id>/duplicate/', views.action_items_entry_duplicate,name='action_items_entry_duplicate'),

    ## PEST RISK VARIABLE: Effect Items
    path("pest-risk/effect-items-list/", views.effect_items_list, name="effect_items_list"),
    path('pest-risk/effect-items-list/<int:id>/', views.effect_items_list,name='effect_items_list'),
    path("pest-risk/effect-items-entry/", views.effect_items_entry, name="effect_items_entry"),
    path('pest-risk/effect-items-entry/<int:id>/', views.effect_items_entry,name='effect_items_entry'),
    path('pest-risk/effect-items-entry/<int:id>/delete/', views.effect_items_delete,name='effect_items_delete'),
    path('pest-risk/effect-items-entry/<int:id>/duplicate/', views.effect_items_entry_duplicate,name='effect_items_entry_duplicate'),

    #path("add-pest-risk-entry/add/", views.add_pest_risk_entry_add, name="add_pest_risk_entry_add"), 
    #path("livestock-entry/", views.livestock_entry, name="livestock_entry"),
    path('admin/', admin.site.urls)
]