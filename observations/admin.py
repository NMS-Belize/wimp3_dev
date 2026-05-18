from django.contrib import admin

from observations.models import WeatherIcons

# Register your models here.
@admin.register(WeatherIcons)
class WeatherIconsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)