from django.db import models
from django.conf import settings

class TropicalWeatherAlertsCategory(models.Model):
    category_name = models.CharField(max_length=200)

    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="tropical_alerts_category_created")
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="tropical_alerts_category_updated")
    created_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "Tropical Weather Alerts Category"
        verbose_name_plural = "Tropical Weather Alerts Categories"

    def __str__(self):
        return str(self.category_name)

class TropicalWeatherAlerts(models.Model):
    storm_name      = models.CharField(max_length=25)
    storm_category  = models.ForeignKey(TropicalWeatherAlertsCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="tropical_alerts_storm_category")
    description     = models.TextField()

    is_published    = models.BooleanField(default=False)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="tropical_alerts_created")
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="tropical_alerts_updated")
    created_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "Tropical Weather Alerts"
        verbose_name_plural = "Tropical Weather Alerts"

    def __str__(self): return (f"{self.storm_category}-{self.storm_name}")

class CAPAlerts(models.Model):
    id          = models.AutoField(primary_key=True)
    guid        = models.CharField(max_length=100, unique=True,db_index=True)
    title       = models.CharField(max_length=30)
    link        = models.URLField(max_length=300)
    description = models.TextField()
    author      = models.CharField(max_length=100)
    category    = models.CharField(max_length=25)
    pubdate     = models.CharField(max_length=50)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(auto_now=True,null=True)
    updated_datetime = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "CAP Alert"
        verbose_name_plural = "CAP Alerts"

    def __str__(self): return self.title

class CAPAlertDetails(models.Model):
    identifier  = models.ForeignKey(CAPAlerts, to_field="guid", db_column="identifier", on_delete=models.CASCADE)
    sender      = models.CharField(max_length=200)
    sent        = models.CharField(max_length=100)
    status      = models.CharField(max_length=25)
    message_type = models.CharField(max_length=25)
    scope       = models.CharField(max_length=25)
    language    = models.CharField(max_length=5)
    category    = models.CharField(max_length=10)
    event       = models.CharField(max_length=50)
    response_type = models.CharField(max_length=20)
    severity    = models.CharField(max_length=20)
    certainty   = models.CharField(max_length=20)
    event_code  = models.CharField(max_length=50)
    value_name  = models.CharField(max_length=15)
    value       = models.CharField(max_length=10)
    onset       = models.CharField(max_length=50)
    expires     = models.CharField(max_length=50)
    sender_name = models.CharField(max_length=30)
    headline    = models.CharField(max_length=100)
    description = models.TextField()
    instruction = models.TextField()
    area        = models.CharField(max_length=30)
    area_description    = models.CharField(max_length=30)
    polygon     = models.TextField()

    published_date      = models.DateTimeField(auto_now=True,null=True)
    updated_datetime    = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "CAP Alert Details"
        verbose_name_plural = "CAP Alert Details"

    def __str__(self): return self.headline