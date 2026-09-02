from time import timezone

from django.db import models
from django.conf import settings

from system_core.models import District, AlertLevel, RiskLevel
from alerts.models import CAPAlertDetails, TropicalWeatherAlerts

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

    class Meta:
            verbose_name = "District Level Forecast Instructions Category"
            verbose_name_plural = "District Level Forecast Instructions Categories"

    def __str__(self):
        return str(self.category_name)
        
class DistrictForecastInstructions(models.Model):
    description = models.CharField(max_length=200)
    category = models.ForeignKey(DistrictForecastInstructionsCategory,on_delete=models.CASCADE,related_name="instructions_category")

    class Meta:
        verbose_name = "District Level Forecast Instruction"
        verbose_name_plural = "District Level Forecast Instructions"

    def __str__(self):
        return str(self.description)

class DistrictForecast(models.Model):
    forecast_date       = models.DateField(unique=True)
    is_published        = models.BooleanField(default=False)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="district_forecasts_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="district_forecasts_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "District Level Forecast"
        verbose_name_plural = "District Level Forecasts"

    def __str__(self):
        return f"{self.forecast_date}"
    
class DistrictForecastDetails(models.Model):
    forecast        = models.ForeignKey(DistrictForecast,on_delete=models.CASCADE,related_name="district_forecast_details")
    district        = models.ForeignKey(District,on_delete=models.CASCADE,related_name="forecast_details")

    temp_min        = models.IntegerField(default=0)
    prob_temp_max   = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="probability_temp_max")
    sev_temp_max    = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="severity_temp_max")
    risk_temp_max   = models.ForeignKey(RiskLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="risk_temp_max")
    #ins_temp_max    = models.ForeignKey(DistrictForecastInstructions,on_delete=models.SET_NULL,null=True,blank=True,)
    ins_temp_max    = models.ManyToManyField(DistrictForecastInstructions, blank=True, related_name="instructions_temp_max")

    temp_max        = models.IntegerField(default=0)
    prob_temp_min   = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="probability_temp_min")
    sev_temp_min    = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="severity_temp_min")
    risk_temp_min   = models.ForeignKey(RiskLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="risk_temp_min")
    #ins_temp_min    = models.ForeignKey(DistrictForecastInstructions,on_delete=models.SET_NULL,null=True,blank=True,)
    ins_temp_min    = models.ManyToManyField(DistrictForecastInstructions, blank=True, related_name="instructions_temp_min")

    winds_min       = models.IntegerField(default=0)
    winds_max       = models.IntegerField(default=0)
    prob_winds      = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="probability_winds")
    sev_winds       = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="severity_winds")
    risk_winds      = models.ForeignKey(RiskLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="risk_winds")
    #ins_winds       = models.ForeignKey(DistrictForecastInstructions,on_delete=models.SET_NULL,null=True,blank=True,)
    ins_winds       = models.ManyToManyField(DistrictForecastInstructions, blank=True, related_name="instructions_winds")

    precip_max      = models.DecimalField(default=0.00,max_digits=5,decimal_places=2)
    prob_precip_max = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="probability_precip_max")
    sev_precip_max  = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="severity_precip_max")
    risk_precip_max = models.ForeignKey(RiskLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="risk_precip_max")
    #ins_precip_max  = models.ForeignKey(DistrictForecastInstructions,on_delete=models.SET_NULL,null=True,blank=True,)
    ins_precip_max  = models.ManyToManyField(DistrictForecastInstructions, blank=True, related_name="instructions_precip_max")

    weather_conditions         = models.TextField(blank=True, null=True)
    prob_weather_conditions    = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="probability_weather_conditions")
    sev_weather_conditions     = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="severity_weather_conditions")
    risk_weather_conditions    = models.ForeignKey(RiskLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="risk_weather_conditions")
    #ins_weather_conditions     = models.ForeignKey(DistrictForecastInstructions,on_delete=models.SET_NULL,null=True,blank=True,)
    ins_weather_conditions  = models.ManyToManyField(DistrictForecastInstructions, blank=True, related_name="instructions_weather_conditions")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["forecast", "district"],
                name="unique_district_per_forecast"
            )
        ]

        verbose_name = "District Level Forecast Details"
        verbose_name_plural = "District Level Forecast Details"

    def __str__(self):
        return f"{self.district} - {self.forecast.forecast_date}"

class SeaState(models.Model):
    description         = models.CharField(max_length=20)
    
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="sea_state_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="sea_state_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return self.description
    
class WindDirection(models.Model):
    description         = models.CharField(max_length=20)
    long_description    = models.CharField(max_length=100)
    value               = models.DecimalField(default=0.00,max_digits=5,decimal_places=1)

    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="wind_direction_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="wind_direction_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return self.description

class WindCondition(models.Model):
    description         = models.CharField(max_length=20)

    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="wind_condition_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="wind_condition_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return self.description

class ForescastGeneralCategory(models.Model):
    description = models.CharField(max_length=200)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="general_forecasts_category_created")
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="general_forecasts_category_updated")
    created_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "General Weather Forecast Category"
        verbose_name_plural = "General Weather Forecast Categories"

    def __str__(self):
        return str(self.description)

class ForecastGeneral(models.Model):

    legacy_id = models.PositiveBigIntegerField(null=True,blank=True,unique=True,db_index=True,)

    forecast_date       = models.DateField()
    forecast_time       = models.TimeField(null=True, blank=True)
    forecast_category   = models.ForeignKey(ForescastGeneralCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="forecast_general_category")

    audio_file = models.FileField(upload_to="general_forecast/{self.forecast_date}/", null=True, blank=True)

    general_situation = models.CharField(max_length=255,null=True, blank=True)
    twenty_four_hour_forecast = models.CharField(max_length=1000,null=True, blank=True)

    light_variable = models.IntegerField(null=True, blank=True)

    wind_speed = models.CharField(max_length=10,null=True, blank=True)

    wind_direction      = models.CharField(max_length=50, null=True, blank=True)
    wind_direction_m2m  = models.ManyToManyField(WindDirection, blank=True,related_name="general_forecasts_wind_direction")

    wind_condition      = models.CharField(max_length=50, null=True, blank=True)
    wind_condition_m2m  = models.ManyToManyField(WindCondition, blank=True,related_name="general_forecasts_wind_condition")

    wind_shift_speed    = models.CharField(max_length=10, null=True, blank=True)

    wind_shift_direction        = models.CharField(max_length=50, null=True, blank=True)
    wind_shift_direction_m2m    = models.ManyToManyField(WindDirection, blank=True,related_name="general_forecasts_wind_direction_shift")
    
    wind_shift_condition        = models.CharField(max_length=50, null=True, blank=True)
    wind_shift_condition_m2m    = models.ManyToManyField(WindCondition, blank=True,related_name="general_forecasts_wind_condition_shift")

    sea_state       = models.CharField(max_length=255,null=True, blank=True)
    sea_state_m2m   = models.ManyToManyField(SeaState, blank=True,related_name="general_forecasts")

    sea_state_shift     = models.CharField(max_length=255, null=True, blank=True)
    sea_state_shift_m2m = models.ManyToManyField(SeaState, blank=True,related_name="general_forecasts_shift")

    wave            = models.CharField(max_length=10, null=True, blank=True)
    wave_shift      = models.CharField(max_length=10, null=True, blank=True)

    advisory        = models.CharField(max_length=1000,null=True, blank=True)
    outlook         = models.CharField(max_length=1000,null=True, blank=True)
    cap_alerts      = models.ManyToManyField("alerts.CAPAlertDetails", blank=True,related_name="general_forecasts_cap")
    tropical_alerts = models.ManyToManyField("alerts.TropicalWeatherAlerts", blank=True,related_name="general_forecasts_cap")

    coast_high_f    = models.IntegerField(null=True, blank=True)
    coast_high_c    = models.IntegerField(null=True, blank=True)

    coast_low_f     = models.IntegerField(null=True, blank=True)
    coast_low_c     = models.IntegerField(null=True, blank=True)

    inland_high_f = models.IntegerField(null=True, blank=True)
    inland_high_c = models.IntegerField(null=True, blank=True)

    inland_low_f = models.IntegerField(null=True, blank=True)
    inland_low_c = models.IntegerField(null=True, blank=True)

    hills_high_f = models.IntegerField(null=True, blank=True)
    hills_high_c = models.IntegerField(null=True, blank=True)

    hills_low_f = models.IntegerField(null=True, blank=True)
    hills_low_c = models.IntegerField(null=True, blank=True)

    is_published = models.BooleanField(default=False)

    forecaster_id = models.IntegerField(null=True, blank=True)

    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="general_forecasts_created")
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="general_forecasts_updated")

    #created_by = models.CharField(max_length=11,null=True, blank=True)
    created_datetime = models.DateTimeField(null=True, blank=True)

    #updated_by = models.CharField(max_length=11,null=True, blank=True)
    updated_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "General Weather Forecast"
        verbose_name_plural = "General Weather Forecasts"

    def __str__(self):
        return f"{self.forecast_date} ({self.id})"

class ForescastMarineCategory(models.Model):
    description         = models.CharField(max_length=200)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_forecasts_category_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_forecasts_category_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "Marine Forecast Category"
        verbose_name_plural = "Marine Forecast Categories"

    def __str__(self):
        return str(self.description)


class ForescastMarineDetailsCategory(models.Model):
    description         = models.CharField(max_length=200)
    display_order     = models.IntegerField(null=True, blank=True)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_forecasts_details_category_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_forecasts_details_category_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "Marine Forecast Category"
        verbose_name_plural = "Marine Forecast Categories"

    def __str__(self):
        return str(self.description)

class ForecastMarine(models.Model):

    legacy_id = models.PositiveBigIntegerField(null=True,blank=True,unique=True,db_index=True,)

    forecast_date       = models.DateField()
    forecast_time       = models.TimeField(null=True, blank=True)
    forecast_category   = models.ForeignKey(ForescastMarineCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="forecast_marine_category")

    synopsis            = models.CharField(max_length=255,null=True, blank=True)

    sea_surface_temperature    = models.IntegerField(null=True, blank=True)
    max_temperature    = models.IntegerField(null=True, blank=True)
    min_temperature    = models.IntegerField(null=True, blank=True)

    advisory        = models.CharField(max_length=1000,null=True, blank=True)
    cap_alerts      = models.ManyToManyField("alerts.CAPAlertDetails", blank=True,related_name="marine_forecasts_cap")
    tropical_alerts = models.ManyToManyField("alerts.TropicalWeatherAlerts", blank=True,related_name="marine_forecasts_cap")

    '''light_variable = models.IntegerField(null=True, blank=True)

    wind_speed = models.CharField(max_length=10,null=True, blank=True)

    wind_direction      = models.CharField(max_length=50, null=True, blank=True)
    wind_direction_m2m  = models.ManyToManyField(WindDirection, blank=True,related_name="general_forecasts_wind_direction")

    wind_condition      = models.CharField(max_length=50, null=True, blank=True)
    wind_condition_m2m  = models.ManyToManyField(WindCondition, blank=True,related_name="general_forecasts_wind_condition")

    wind_shift_speed    = models.CharField(max_length=10, null=True, blank=True)

    wind_shift_direction        = models.CharField(max_length=50, null=True, blank=True)
    wind_shift_direction_m2m    = models.ManyToManyField(WindDirection, blank=True,related_name="general_forecasts_wind_direction_shift")
    
    wind_shift_condition        = models.CharField(max_length=50, null=True, blank=True)
    wind_shift_condition_m2m    = models.ManyToManyField(WindCondition, blank=True,related_name="general_forecasts_wind_condition_shift")

    sea_state       = models.CharField(max_length=255,null=True, blank=True)
    sea_state_m2m   = models.ManyToManyField(SeaState, blank=True,related_name="general_forecasts")

    sea_state_shift     = models.CharField(max_length=255, null=True, blank=True)
    sea_state_shift_m2m = models.ManyToManyField(SeaState, blank=True,related_name="general_forecasts_shift")

    wave            = models.CharField(max_length=10, null=True, blank=True)
    wave_shift      = models.CharField(max_length=10, null=True, blank=True)

    advisory        = models.CharField(max_length=1000,null=True, blank=True)
    outlook         = models.CharField(max_length=1000,null=True, blank=True)
    cap_alerts      = models.ManyToManyField("alerts.CAPAlertDetails", blank=True,related_name="general_forecasts_cap")
    tropical_alerts  = models.ManyToManyField("alerts.TropicalWeatherAlerts", blank=True,related_name="general_forecasts_cap")

    
    coast_high_c    = models.IntegerField(null=True, blank=True)

    coast_low_f     = models.IntegerField(null=True, blank=True)
    coast_low_c     = models.IntegerField(null=True, blank=True)

    inland_high_f = models.IntegerField(null=True, blank=True)
    inland_high_c = models.IntegerField(null=True, blank=True)

    inland_low_f = models.IntegerField(null=True, blank=True)
    inland_low_c = models.IntegerField(null=True, blank=True)

    hills_high_f = models.IntegerField(null=True, blank=True)
    hills_high_c = models.IntegerField(null=True, blank=True)

    hills_low_f = models.IntegerField(null=True, blank=True)
    hills_low_c = models.IntegerField(null=True, blank=True)'''

    is_published    = models.BooleanField(default=False)
    forecaster_id   = models.IntegerField(null=True, blank=True)

    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_forecasts_created")
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_forecasts_updated")

    #created_by = models.CharField(max_length=11,null=True, blank=True)
    created_datetime = models.DateTimeField(null=True, blank=True)

    #updated_by = models.CharField(max_length=11,null=True, blank=True)
    updated_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Marine Forecast"
        verbose_name_plural = "Marine Forecasts"

    def __str__(self):
        return f"{self.forecast_date} ({self.id})"

'''class ForecastMarineDetails(models.Model):

    #marine_type         = models.ForeignKey(ForescastMarineDetailsCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="forecast_marine_category") 
    #marine_date_type varchar(20) 
    marine_date         = models.DateField() 
    forecast_id         = models.IntegerField(null=True, blank=True)
    wind_speed          = models.CharField(max_length=10,null=True, blank=True)
    #wind_direction varchar(255) 
    #wind_condition varchar(255) 
    #sea_state varchar(255) 
    #waves varchar(255) 
    #info varchar(255

    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_forecasts_details_created")
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_forecasts_details_updated")

    #created_by = models.CharField(max_length=11,null=True, blank=True)
    created_datetime = models.DateTimeField(null=True, blank=True)

    #updated_by = models.CharField(max_length=11,null=True, blank=True)
    updated_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
            verbose_name = "Marine Forecast Details"
            verbose_name_plural = "Marine Forecast Details"
    
    def __str__(self):
        return f"{self.marine_date} ({self.id})"'''