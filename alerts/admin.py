from django.contrib import admin

# Register your models here.
from .models import CAPAlerts, CAPAlertDetails

admin.site.register(CAPAlerts)
admin.site.register(CAPAlertDetails)