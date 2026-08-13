from django.contrib import admin
from django.urls import include, path 
from django.conf.urls.static import static

#from rest_framework import serializers
#from rest_framework.routers import DefaultRouter
#from sensors.views import CommodityTypeViewSet

from . import views
#from ..radar import views

from rest_framework import serializers
from rest_framework.routers import DefaultRouter

app_name = 'alerts'

urlpatterns = [
    path('', views.index, name="index"),

    ## TROPICAL WEATHER ALERTS
    path('tropical-weather-alerts/list/', views.tropical_alerts_list, name="tropical_alerts_list"),
    path('tropical-weather-alerts/list/<int:id>/', views.tropical_alerts_list, name='tropical_alerts_list'),
    path('tropical-weather-alerts/entry/', views.tropical_alerts_entry, name="tropical_alerts_entry"),
    path('tropical-weather-alerts/entry/<int:id>/', views.tropical_alerts_entry, name='tropical_alerts_entry'),
    path('tropical-weather-alerts/entry/<int:id>/delete/', views.tropical_alerts_delete, name='tropical_alerts_delete'),
    path('tropical-weather-alerts/entry/toggle-publish/<int:id>/', views.tropical_alerts_toggle_is_published, name="tropical_alerts_toggle_is_published"),

    ## TROPICAL WEATHER ALERTS: Category
    path('tropical-weather-alerts/category/list/', views.tropical_alerts_category_list, name="tropical_alerts_category_list"),
    path('tropical-weather-alerts/category/list/<int:id>/', views.tropical_alerts_category_list, name='tropical_alerts_category_list'),
    path('tropical-weather-alerts/category/entry/', views.tropical_alerts_category_entry, name="tropical_alerts_category_entry"),
    path('tropical-weather-alerts/category/entry/<int:id>/', views.tropical_alerts_category_entry, name='tropical_alerts_category_entry'),
    path('tropical-weather-alerts/category/entry/<int:id>/delete/', views.tropical_alerts_category_delete, name='tropical_alerts_category_delete'),

    ## CAP ALERTS
    path('cap-alerts-list/', views.cap_alerts_list, name="cap_alerts_list"),
    path('cap-alerts-import/', views.cap_alerts_import, name="cap_alerts_import"),
    path('cap-alerts-details/<int:id>/', views.cap_alerts_details, name="cap_alerts_details"),
    path('cap-alerts-toggle-is-published/<int:id>/', views.cap_alert_toggle_is_published, name="cap_alert_toggle_is_published"),
]