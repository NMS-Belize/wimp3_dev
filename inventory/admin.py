from django.contrib import admin
from .models import InventoryCategory, OfficeLocationPlacement, InventoryItem

@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(OfficeLocationPlacement)
class OfficeLocationPlacementAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'room')
    search_fields = ('name', 'building', 'room')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'asset_tag',
        'category',
        'placement',
        'status',
        'is_active',
    )
    list_filter = ('category', 'status', 'is_active', 'placement')
    search_fields = ('name', 'asset_tag', 'serial_number', 'brand', 'model')