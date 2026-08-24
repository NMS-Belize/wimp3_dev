import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings

from system_core.models import District, Zone, Months, AlertLevel

# Create your models here.

class Sector(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=20)
    published_date = models.DateTimeField(auto_now=True,null=True)
    updated_datetime = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"

    def __str__(self): return self.description

class Commodity(models.Model):
    id          = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=100)
    sector      = models.ForeignKey(Sector, related_name='sector', on_delete=models.CASCADE,null=True)
    published_date      = models.DateTimeField(auto_now=True,null=True)
    updated_datetime    = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "Commodity"
        verbose_name_plural = "Commodities"

    def __str__(self): return f"{self.description} {self.id}"

class PestAlertLevel(models.Model):
    id                  = models.BigAutoField(primary_key=True)
    description         = models.CharField(max_length=50)
    color_hex           = models.CharField(max_length=7,null=True)
    published_date      = models.DateTimeField(auto_now=True,null=True)
    updated_datetime    = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "Pest Alert Level"
        verbose_name_plural = "Pest Alert Levels"

    def __str__(self): return self.description

class DroughtAlertLevel(models.Model):
    id                  = models.BigAutoField(primary_key=True)
    title               = models.CharField(max_length=50,null=True)
    description         = models.CharField(max_length=50,null=True)
    action_level        = models.TextField(null=True)
    color_hex           = models.CharField(max_length=7,null=True)
    published_date      = models.DateTimeField(auto_now=True,null=True)
    updated_datetime    = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "Drought Alert Level"
        verbose_name_plural = "Drought Alert Levels"

    def __str__(self): return self.title

class PestRiskEffect(models.Model):
    id                  = models.BigAutoField(primary_key=True)
    effect_description  = models.TextField(blank=False,null=False)
    #sector              = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='pest_risk_effect_category', blank=True, null=True)
    commodity           = models.ForeignKey(Commodity, on_delete=models.CASCADE,related_name='pest_risk_effect_commodity',null=True)
    published_date      = models.DateTimeField(auto_now=True,null=True)
    updated_datetime    = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "Pest Risk Effect"
        verbose_name_plural = "Pest Risk Effects"

        constraints = [
            models.UniqueConstraint(
                fields=['commodity', 'effect_description'],
                name='unique_commodity_effect_description'
            )
        ]

    def __str__(self): return self.effect_description

class PestRiskAction(models.Model):
    id                  = models.BigAutoField(primary_key=True)
    action_description  = models.TextField(blank=False,null=False)
    #sector              = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='pest_risk_actions_category', blank=True, null=True)
    commodity           = models.ForeignKey(Commodity, on_delete=models.CASCADE,related_name='pest_risk_actions_commodity',null=True)
    published_date      = models.DateTimeField(auto_now=True,null=True)
    updated_datetime    = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "Pest Risk Action"
        verbose_name_plural = "Pest Risk Actions"

    def __str__(self): return self.action_description

class PestRiskInfo(models.Model):
    id                  = models.BigAutoField(primary_key=True)
    info_description    = models.TextField(blank=False,null=False)
    commodity           = models.ForeignKey(Commodity, on_delete=models.CASCADE,related_name='pest_risk_info_commodity',null=True)
    published_date      = models.DateTimeField(auto_now=True,null=True)
    updated_datetime    = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "Pest Risk Info"
        verbose_name_plural = "Pest Risk Info"

        constraints = [
            models.UniqueConstraint(
                fields=['commodity', 'info_description'],
                name='unique_commodity_info_description'
            )
        ]

    def __str__(self): return self.info_description

class PestRisk(models.Model):
    id              = models.BigAutoField(primary_key=True)
    months          = models.JSONField(null=True)   # to store multiple months (checkbox list)
    year            = models.IntegerField(default=0)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="pest_risk_created")
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="pest_risk_updated")
    created_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "Pest Risk"
        verbose_name_plural = "Pest Risk"

    def __str__(self): return f"{self.year}"

class PestRiskEntryMainListing(models.Model):
    id          = models.BigAutoField(primary_key=True)
    months      = models.JSONField()   # to store multiple months (checkbox list)
    year        = models.IntegerField(default=0)
    commodity   = models.ForeignKey(Commodity, on_delete=models.CASCADE,related_name='Commodity',null=True)
    is_published = models.BooleanField(default=False)
    #def __str__(self): return f"[{self.id}] {self.year} {self.months} - {self.commodity}"

    class Meta:
        verbose_name = "Pest Risk Entry"
        verbose_name_plural = "Pest Risk Entries"

    def __str__(self):
        return f"[{self.id}] {self.year}: {self.get_month_names()} - {self.commodity}"

    def get_month_names(self):
        MONTH_CHOICES = {
            1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
            7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"
        }
        return ", ".join([MONTH_CHOICES.get(m, str(m)) for m in self.months])

class PestRiskEntryDetails(models.Model):
    id                      = models.BigAutoField(primary_key=True)
    pest_risk_id            = models.ForeignKey(PestRisk, on_delete=models.CASCADE,related_name='pest_risk_entries')
    commodity_id            = models.ForeignKey(Commodity, on_delete=models.CASCADE,null=True,related_name='pr_commodity')
    district_id             = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    pest_alert_lvl_id       = models.ForeignKey("system_core.AlertLevel", on_delete=models.CASCADE, blank=True, null=True)
    drought_alert_lvl_id    = models.ForeignKey(DroughtAlertLevel, on_delete=models.CASCADE, blank=True, null=True)
    temp_min                = models.DecimalField(default=0.00,max_digits=5,decimal_places=2, blank=True, null=True)
    temp_max                = models.DecimalField(default=0.00,max_digits=5,decimal_places=2, blank=True, null=True)
    precip_min              = models.DecimalField(default=0.0,max_digits=20,decimal_places=1, blank=True, null=True)
    precip_max              = models.DecimalField(default=0.0,max_digits=20,decimal_places=1, blank=True, null=True)
    effect                  = models.ManyToManyField(PestRiskEffect, blank=True)
    info                    = models.ManyToManyField(PestRiskInfo, blank=True)
    actions                 = models.ManyToManyField(PestRiskAction, blank=True)
    is_published            = models.BooleanField(default=False)
    updated_by              = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="pest_risk_item_updated")
    updated_datetime        = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "Pest Risk Detail"
        verbose_name_plural = "Pest Risk Details"

    def __str__(self): return f"{self.id}"