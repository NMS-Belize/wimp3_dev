from django.contrib import admin
from .models import InventoryCategory, OfficeLocationPlacement, InventoryItem


admin.site.register(InventoryCategory)
admin.site.register(InventoryItem)

'''@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name')

@admin.register(InventoryCategory)
class OfficeLocationPlacementAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'room')
    search_fields = ('name', 'building', 'room')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = (
        'device_label',
    )
    #list_filter = ('category', 'is_active', 'placement')
    search_fields = ('device_label')'''