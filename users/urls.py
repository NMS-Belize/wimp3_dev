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

app_name = 'users'

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('dashboard/', views.user_dashboard, name="user_dashboard"),


    path('list/', views.user_list, name="user_list"),
    path('entry/', views.user_entry, name="user_entry"),

    path('entry-details/<int:id>/', views.user_entry_details, name="user_entry_details"),
    path('entry/<int:id>/', views.user_entry, name="user_entry"),

    path('entry/<int:id>/toggle-active/', views.user_active_toggle, name='user_active_toggle'),
    path('entry/delete/<int:id>/', views.user_delete, name="user_delete"),

    path('employee/list/<int:id>/', views.employee_list, name="employee_list"),
    path('employee/list/', views.employee_list, name="employee_list"),
    path('employee/entry/', views.employee_entry, name="employee_entry"),
    path('employee/entry/<int:id>/', views.employee_entry, name="employee_entry"),
    path('employee/entry/delete/<int:id>/', views.employee_delete, name="employee_delete"),

    #path('entry-details/<int:id>/', views.user_entry_details, name="user_entry_details"),
    #path('entry/<int:id>/', views.user_entry, name="user_entry"),
    #path('entry/<int:id>/toggle-active/', views.user_active_toggle, name='user_active_toggle'),
    #path('entry/delete/<int:id>/', views.user_delete, name="user_delete"),
]