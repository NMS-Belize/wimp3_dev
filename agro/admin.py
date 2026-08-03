from django.contrib import admin

# Register your models here.
from .models import Commodity, Sector, PestAlertLevel, DroughtAlertLevel, PestRiskEntryDetails, PestRiskEffect, PestRiskAction, PestRisk

admin.site.register(Sector)

admin.site.register(PestAlertLevel)
admin.site.register(DroughtAlertLevel)
#admin.site.register(Livestock)

admin.site.register(PestRisk)
admin.site.register(PestRiskEntryDetails)
admin.site.register(PestRiskEffect)
admin.site.register(PestRiskAction)

@admin.register(Commodity)

class CommodityTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'sector', 'published_date', 'updated_datetime')
    search_fields = ('description','sector')