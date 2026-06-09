from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('index', views.index, name='index'),
    #path('new/', views.inventory_entry, name='inventory_entry'),
    #path('edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),

    ## INVENTORY: Items
    path('inventory/list/', views.inventory_list, name="inventory_list"),
    path('inventory-list/<int:id>/', views.inventory_list,name='inventory_list'),
    path('inventory/entry/', views.inventory_entry, name="inventory_entry"),
    path('inventory/entry/<int:id>/', views.inventory_entry,name='inventory_entry'),
    path('inventory/entry/<int:id>/delete/', views.inventory_delete,name='inventory_delete'),

    path('inventory/category/list/', views.inventory_category_list, name="inventory_category_list"),
    path('inventory/category/list/<int:id>', views.inventory_category_list, name="inventory_category_list"),
    path('inventory/category/entry/', views.inventory_category_entry, name="inventory_category_entry"),
    path('inventory/category/entry/<int:id>/', views.inventory_category_entry,name='inventory_category_entry'),
    path('inventory/category/entry/<int:id>/delete/', views.inventory_category_delete,name='inventory_category_delete'),

    path('inventory/device-type/list/', views.device_type_list, name="device_type_list"),
    path('inventory/device-type/list/<int:id>', views.device_type_list, name="device_type_list"),
    path('inventory/device-type/entry/', views.device_type_entry, name="device_type_entry"),
    path('inventory/device-type/entry/<int:id>/', views.device_type_entry,name='device_type_entry'),
    path('inventory/device-type/entry/<int:id>/delete/', views.device_type_delete,name='device_type_delete'),

    path('inventory/department/list/', views.department_section_list, name="department_section_list"),
    path('inventory/department/list/<int:id>', views.department_section_list, name="department_section_list"),
    path('inventory/department/entry/', views.department_section_entry, name="department_section_entry"),
    path('inventory/department/entry/<int:id>/', views.department_section_entry, name="department_section_entry"),
    path('inventory/department/entry/<int:id>/delete/', views.department_section_delete, name='department_section_delete'),

    path('inventory/manufacturer/list/', views.manufacturer_list, name="manufacturer_list"),
    path('inventory/manufacturer/list/<int:id>', views.manufacturer_list, name="manufacturer_list"),
    path('inventory/manufacturer/entry/', views.manufacturer_entry, name="manufacturer_entry"),
    path('inventory/manufacturer/entry/<int:id>/', views.manufacturer_entry, name="manufacturer_entry"),
    path('inventory/manufacturer/entry/<int:id>/delete/', views.manufacturer_delete, name='manufacturer_delete'),

    path('inventory/vendor/list/', views.vendor_list, name="vendor_list"),
    path('inventory/vendor/list/<int:id>', views.vendor_list, name="vendor_list"),
    path('inventory/vendor/entry/', views.vendor_entry, name="vendor_entry"),
    path('inventory/vendor/entry/<int:id>/', views.vendor_entry, name="vendor_entry"),
    path('inventory/vendor/entry/<int:id>/delete/', views.vendor_delete, name='vendor_delete'),
]