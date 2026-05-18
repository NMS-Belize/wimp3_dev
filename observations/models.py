from django.db import models

from django.core.exceptions import ValidationError
import os

# Create your models here.
class WeatherIcons(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    icon_file   = models.FileField(upload_to='static/weather_icons/')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Weather Icons'

    def __str__(self):
        return self.name

class WeatherCodes(models.Model):
    code        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon_day    = models.ForeignKey(WeatherIcons, on_delete=models.SET_NULL, related_name='day_icons', blank=True, null=True)
    icon_night  = models.ForeignKey(WeatherIcons, on_delete=models.SET_NULL, related_name='night_icons', blank=True, null=True)

    class Meta:
        ordering = ['code']
        verbose_name_plural = 'Weather Codes'

    def __str__(self):
        return self.code