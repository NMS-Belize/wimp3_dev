from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from rest_framework import serializers
from rest_framework.routers import DefaultRouter
from agro.views import CommodityTypeViewSet

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("pest-risk-list/", views.pest_risk_list, name="pest_risk_list"), 
    path("pest-risk-entry/new/", views.pest_risk_entry_new, name="pest_risk_entry_new"),
    #path("pest-risk-entry/edit/<int:entry_id>", views.edit_pest_risk_entry, name="edit_pest_risk_entry"), 

    path("pest-risk-entry/add/", views.pest_risk_entry_add, name="pest_risk_entry_add"),
    path("pest-risk-entry/update/", views.pest_risk_entry_update, name="pest_risk_entry_update"), 

    
    
    path('pest-risk-entry/<int:entry_id>/', views.pest_risk_details, name='pest_risk_details'),
    path('pest-risk-entry/<int:entry_id>/add/', views.pest_risk_add_details, name='pest_risk_add_details'),
    path("pest-risk-entry-details/<int:entry_id>/", views.pest_risk_details_list, name="pest_risk_details_list"), 

    
    ## PEST RISK VARIABLE: Commodity
    path("pest-risk/commodity-list/", views.commodity_list, name="commodity_list"),

    ## PEST RISK VARIABLE: Pest Alert Level
    path("pest-risk/pest-alert-level-list/", views.pest_alert_level_list, name="pest_alert_level_list"),
    path("pest-risk/pest-alert-level-update/<int:entry_id>/", views.pest_alert_level_update, name="pest_alert_level_update"),
    path("pest-risk/pest-alert-level-delete/<int:entry_id>/", views.pest_alert_level_update, name="pest_alert_level_update"),


    ## PEST RISK VARIABLE: Drought Alert Level
    path("pest-risk/drought-alert-level-list/", views.drought_alert_level_list, name="drought_alert_level_list"),

    ## PEST RISK VARIABLE: Action Items
    path("pest-risk/action-items-list/", views.action_items_list, name="action_items_list"),

    ## PEST RISK VARIABLE: Effect Items
    path("pest-risk/effect-items-list/", views.effect_items_list, name="effect_items_list"),

    #path("add-pest-risk-entry/add/", views.add_pest_risk_entry_add, name="add_pest_risk_entry_add"), 
    path("livestock-entry/", views.livestock_entry, name="livestock_entry"),
    path('admin/', admin.site.urls)
]