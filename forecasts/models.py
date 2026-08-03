from time import timezone

from django.db import models
from django.conf import settings

from system_core.models import District, AlertLevel, RiskLevel

# Create your models here.
     
class Probability(models.Model):
    description = models.CharField(max_length=20)
    color       = models.CharField(max_length=20,default="",null=True, blank=True)

    def __str__(self):
        return self.description

class Severity(models.Model):
    description = models.CharField(max_length=20)
    color       = models.CharField(max_length=20,default="",null=True, blank=True)

    def __str__(self):
        return self.description

class DistrictForecastInstructionsCategory(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.category_name)
        
class DistrictForecastInstructions(models.Model):
    description = models.CharField(max_length=200)
    #category = models.ForeignKey(DistrictForecastInstructionsCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="instructions_category")
    category = models.ForeignKey(DistrictForecastInstructionsCategory,on_delete=models.CASCADE,related_name="instructions_category")

    def __str__(self):
        return str(self.description)

class DistrictForecast(models.Model):
    forecast_date   = models.DateField(unique=True)
    is_published    = models.BooleanField(default=False)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="district_forecasts_created")
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="district_forecasts_updated")
    created_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return f"{self.forecast_date}"
    
class DistrictForecastDetails(models.Model):
    forecast        = models.ForeignKey(DistrictForecast,on_delete=models.CASCADE,related_name="district_forecast_details")
    district        = models.ForeignKey(District,on_delete=models.CASCADE,related_name="forecast_details")

    temp_min        = models.IntegerField(default=0)
    prob_temp_max   = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="probability_temp_max")
    sev_temp_max    = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="severity_temp_max")
    risk_temp_max   = models.ForeignKey(RiskLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="risk_temp_max")
    ins_temp_max    = models.ForeignKey(DistrictForecastInstructions,on_delete=models.SET_NULL,null=True,blank=True,related_name="instructions_temp_max")

    temp_max        = models.IntegerField(default=0)
    prob_temp_min   = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="probability_temp_min")
    sev_temp_min    = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="severity_temp_min")
    risk_temp_min   = models.ForeignKey(RiskLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="risk_temp_min")
    ins_temp_min    = models.ForeignKey(DistrictForecastInstructions,on_delete=models.SET_NULL,null=True,blank=True,related_name="instructions_temp_min")

    winds_min       = models.IntegerField(default=0)
    winds_max       = models.IntegerField(default=0)
    prob_winds      = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="probability_winds")
    sev_winds       = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="severity_winds")
    risk_winds      = models.ForeignKey(RiskLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="risk_winds")
    ins_winds       = models.ForeignKey(DistrictForecastInstructions,on_delete=models.SET_NULL,null=True,blank=True,related_name="instructions_winds")

    precip_max      = models.DecimalField(default=0.00,max_digits=5,decimal_places=1)
    prob_precip_max = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="probability_precip_max")
    sev_precip_max  = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="severity_precip_max")
    risk_precip_max = models.ForeignKey(RiskLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="risk_precip_max")
    ins_precip_max  = models.ForeignKey(DistrictForecastInstructions,on_delete=models.SET_NULL,null=True,blank=True,related_name="instructions_precip_max")

    weather_conditions         = models.TextField(blank=True, null=True)
    prob_weather_conditions    = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="probability_weather_conditions")
    sev_weather_conditions     = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="severity_weather_conditions")
    risk_weather_conditions    = models.ForeignKey(RiskLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="risk_weather_conditions")
    ins_weather_conditions     = models.ForeignKey(DistrictForecastInstructions,on_delete=models.SET_NULL,null=True,blank=True,related_name="instructions_weather_conditions")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["forecast", "district"],
                name="unique_district_per_forecast"
            )
        ]

    def __str__(self):
        return f"{self.district} - {self.forecast.forecast_date}"

class ForecastGeneral(models.Model):
    forecast_date = models.DateField()
    forecast_time = models.TimeField(null=True, blank=True)
    forecast_type = models.IntegerField(null=True, blank=True)

    general_situation = models.CharField(max_length=255)
    thr_forecast = models.CharField(max_length=1000)

    light_variable = models.IntegerField(null=True, blank=True)

    wind_speed = models.CharField(max_length=10)
    wind_direction = models.CharField(max_length=50, null=True, blank=True)
    wind_condition = models.CharField(max_length=50, null=True, blank=True)

    wind_shift_speed = models.CharField(max_length=10, null=True, blank=True)
    wind_shift_direction = models.CharField(max_length=50, null=True, blank=True)
    wind_shift_condition = models.CharField(max_length=50, null=True, blank=True)

    sea_state = models.CharField(max_length=255)
    wave = models.CharField(max_length=10, null=True, blank=True)

    sea_state_shift = models.CharField(max_length=255, null=True, blank=True)
    wave_shift = models.CharField(max_length=10, null=True, blank=True)

    advisory = models.CharField(max_length=1000)
    outlook = models.CharField(max_length=1000)

    coast_high_f = models.IntegerField()
    coast_high_c = models.IntegerField(null=True, blank=True)

    coast_low_f = models.IntegerField()
    coast_low_c = models.IntegerField(null=True, blank=True)

    inland_high_f = models.IntegerField()
    inland_high_c = models.IntegerField(null=True, blank=True)

    inland_low_f = models.IntegerField()
    inland_low_c = models.IntegerField(null=True, blank=True)

    hills_high_f = models.IntegerField()
    hills_high_c = models.IntegerField(null=True, blank=True)

    hills_low_f = models.IntegerField()
    hills_low_c = models.IntegerField(null=True, blank=True)

    publish_to_web = models.BooleanField()

    forecaster_id = models.IntegerField()

    #created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="general_forecasts_created")
    #updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="general_forecasts_updated")

    #created_by = models.CharField(max_length=11)
    #created_time = models.DateTimeField(null=True, blank=True)

    #updated_by = models.CharField(max_length=11)
    #updated_time = models.DateTimeField(null=True, blank=True)

    auto_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "tbl_forecast_general"

    def __str__(self):
        return f"{self.forecast_date} ({self.id})"