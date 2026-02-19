from django.db import models

# Create your models here.
class CAPAlerts(models.Model):
    guid        = models.CharField(max_length=100, primary_key=True)
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
    identifier = models.ForeignKey(
        CAPAlerts,
        to_field="guid",
        db_column="identifier",
        on_delete=models.CASCADE
    )
    sender      = models.CharField(max_length=200)
    sent        = models.CharField(max_length=100)
    status      = models.CharField(max_length=25)
    message_type        = models.CharField(max_length=25)
    scope       = models.CharField(max_length=25)
    language    = models.CharField(max_length=5)
    category    = models.CharField(max_length=10)
    event       = models.CharField(max_length=50)
    response_type       = models.CharField(max_length=20)
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