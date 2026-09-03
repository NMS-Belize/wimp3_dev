

from django.contrib import admin
from django.urls import include, path 
from django.conf.urls.static import static

from . import views

from rest_framework import serializers
from rest_framework.routers import DefaultRouter

app_name = 'company'

urlpatterns = [
    path('', views.index, name="index"),
    path('list/', views.company_list, name="company_list"),
    path('list/<int:id>/', views.company_list, name="company_list"),
    path('entry/', views.company_entry, name="company_entry"),
    path('entry/<int:id>/', views.company_entry,name='company_entry_id'),
]