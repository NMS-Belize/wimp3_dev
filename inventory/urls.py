from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('index', views.index, name='index'),
    #path('new/', views.inventory_entry, name='inventory_entry'),
    #path('edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),

    ## INVENTORY: Items
    path('inventory-list/', views.inventory_list, name="inventory_list"),
    #path('inventory-list/<int:id>/', views.inventory_list,name='inventory_list'),
    path('inventory-entry/', views.inventory_entry, name="inventory_entry"),
    path('inventory-entry/<int:id>/', views.inventory_entry,name='inventory_entry'),
    path('inventory-entry/<int:id>/delete/', views.inventory_delete,name='inventory_delete'),

    path('inventory-category-list/', views.inventory_category_list, name="inventory_category_list"),
    path('inventory-category-entry/', views.inventory_category_entry, name="inventory_category_entry"),
    path('inventory-category-entry/<int:id>/', views.inventory_category_entry,name='inventory_category_entry'),
    path('inventory-category-entry/<int:id>/delete/', views.inventory_category_delete,name='inventory_category_delete'),
]