from django.urls import path
from . import views

app_name = 'observations'

urlpatterns = [
    path('index', views.index, name='index'),
    #path('new/', views.inventory_entry, name='inventory_entry'),
    #path('edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),

    ## WEATHER ICONS
    path('weather-icon-list/', views.weather_icon_list, name="weather_icon_list"),
    path('weather-icon-list/<int:id>/', views.weather_icon_list,name='weather_icon_list'),
    path('weather-icon-entry/', views.weather_icon_entry, name="weather_icon_entry"),
    path('weather-icon-entry/<int:id>/', views.weather_icon_entry,name='weather_icon_entry'),
    #path('weather-icon-entry/<int:id>/delete/', views.weather_icon_delete,name='weather_icon_delete'),

]