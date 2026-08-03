from django.contrib import admin

# Register your models here.
from system_core.models import District, Months, RiskLevel, AlertLevel, JobTitle

# Register your models here.
admin.site.register(Months)
admin.site.register(District)
admin.site.register(RiskLevel)
admin.site.register(AlertLevel)
admin.site.register(JobTitle)