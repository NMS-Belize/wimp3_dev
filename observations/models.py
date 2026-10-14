from django.db import models

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

import os

# Create your models here.
class WeatherIcons(models.Model):
    
    name        = models.CharField(max_length=100, unique=True)
    icon_file   = models.FileField(upload_to='static/weather_icons/')
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="weather_icon_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="weather_icon_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Weather Icons'

    def __str__(self):
        return self.name

class WeatherCodes(models.Model):
    
    code        = models.CharField(max_length=2,unique=True,validators=[RegexValidator(regex=r"^[0-9]{2}$",message="Enter two digits, such as 00, 01, or 02.")])
    description = models.TextField(blank=True, null=True)
    icon_day    = models.ForeignKey(WeatherIcons, on_delete=models.SET_NULL, related_name='day_icons', blank=True, null=True)
    icon_night  = models.ForeignKey(WeatherIcons, on_delete=models.SET_NULL, related_name='night_icons', blank=True, null=True)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="weather_code_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="weather_code_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        ordering = ['code']
        verbose_name_plural = 'Weather Codes'

    def __str__(self):
        return self.code