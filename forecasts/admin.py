from django.contrib import admin

from forecasts.models import District, DistrictForecast, DistrictForecastInstructions, Severity, Probability, RiskLevel

# Register your models here.
admin.site.register(District)
admin.site.register(DistrictForecast)
admin.site.register(DistrictForecastInstructions)