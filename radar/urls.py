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

app_name = 'radar'

urlpatterns = [
    path("", views.index, name="index"),

    path('radar-images/', views.radar_image_entry, name="radar_image_entry"),
    path('radar-images/<int:id>/', views.radar_image_entry,name='radar_image_entry'),
    path('radar-images-list/', views.radar_images_list, name="radar_images_list"),
    path('radar-images-list/<int:id>/', views.radar_images_list,name='radar_images_list'),
    path('radar-images/<int:id>/delete/', views.radar_image_delete,name='radar_image_delete'),
]