from django.contrib import admin

# Register your models here.
from .models import Months, District, Zone, CommodityType, CommodityCategory, PestAlertLevel, DroughtAlertLevel, PestRiskEntryMainListing, PestRiskEntryDetails, PestRiskEffect, PestRiskAction

admin.site.register(Months)
admin.site.register(District)
admin.site.register(Zone)
admin.site.register(CommodityCategory)

admin.site.register(PestAlertLevel)
admin.site.register(DroughtAlertLevel)
#admin.site.register(Livestock)

admin.site.register(PestRiskEntryMainListing)
admin.site.register(PestRiskEntryDetails)
admin.site.register(PestRiskEffect)
admin.site.register(PestRiskAction)

@admin.register(CommodityType)

class CommodityTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'commodity_category', 'published_date', 'updated_datetime')
    search_fields = ('description','commodity_category')