from django.contrib import admin

from forecasts.models import DistrictForecast, DistrictForecastDetails, DistrictForecastInstructionsCategory, DistrictForecastInstructions, ForecastGeneral, ForescastGeneralCategory

# Register your models here.
admin.site.register(DistrictForecast)
admin.site.register(DistrictForecastDetails)
admin.site.register(DistrictForecastInstructionsCategory)
admin.site.register(DistrictForecastInstructions)

admin.site.register(ForecastGeneral)
admin.site.register(ForescastGeneralCategory)