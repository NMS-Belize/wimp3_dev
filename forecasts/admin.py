from django.contrib import admin

from forecasts.models import DistrictForecast, DistrictForecastInstructions, Severity, Probability, ForecastGeneral

# Register your models here.
admin.site.register(DistrictForecast)
admin.site.register(DistrictForecastInstructions)

admin.site.register(ForecastGeneral)