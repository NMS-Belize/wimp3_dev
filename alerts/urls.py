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

    ## CAP ALERTS
    path('cap-alerts-list/', views.cap_alerts_list, name="cap_alerts_list"),
    path('cap-alerts-import/', views.cap_alerts_import, name="cap_alerts_import"),
    path('cap-alerts-details/<str:guid>/', views.cap_alerts_details, name="cap_alerts_details"),
    path('cap-alerts-toggle-is-published/<str:guid>/', views.cap_alert_toggle_is_published, name="cap_alert_toggle_is_published"),
]