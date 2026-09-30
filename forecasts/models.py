from time import timezone

from datetime import time
from django.db import models
from django.conf import settings
from django.db.models import Max

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

    @property
    def latest_updated_datetime(self):
        latest_detail = self.district_forecast_details.aggregate(
            latest=Max("updated_datetime")
        )["latest"]

        dates = [
            dt for dt in (
                self.updated_datetime,
                latest_detail,
            )
            if dt is not None
        ]

        return max(dates) if dates else None

    class Meta:
        verbose_name = "District Level Forecast"
        verbose_name_plural = "District Level Forecasts"

    def __str__(self):
        return f"{self.forecast_date}"
    
class DistrictForecastDetails(models.Model):
    forecast        = models.ForeignKey(DistrictForecast,on_delete=models.CASCADE,related_name="district_forecast_details")
    district        = models.ForeignKey(District,on_delete=models.CASCADE,related_name="forecast_details")

    temp_min_low    = models.IntegerField(default=0)
    temp_min_high   = models.IntegerField(default=0)
    prob_temp_max   = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="probability_temp_max")
    sev_temp_max    = models.ForeignKey(AlertLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="severity_temp_max")
    risk_temp_max   = models.ForeignKey(RiskLevel,on_delete=models.SET_NULL,null=True,blank=True,related_name="risk_temp_max")
    #ins_temp_max    = models.ForeignKey(DistrictForecastInstructions,on_delete=models.SET_NULL,null=True,blank=True,)
    ins_temp_max    = models.ManyToManyField(DistrictForecastInstructions, blank=True, related_name="instructions_temp_max")

    temp_max_low   = models.IntegerField(default=0)
    temp_max_high   = models.IntegerField(default=0)
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

    precip_min      = models.DecimalField(default=0.00,max_digits=5,decimal_places=2)
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

    created_by              = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="district_forecast_details_created")
    updated_by              = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="district_forecast_details_updated")
    created_datetime        = models.DateTimeField(auto_now_add=True,null=True)
    updated_datetime        = models.DateTimeField(auto_now=True,null=True)

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

def general_forecast_audio_path(instance, filename):
    forecast_time = instance.forecast_time.strftime("%I%M_%p")

    new_filename = (
        f"{instance.forecast_date}_"
        f"{forecast_time}_NMS_BZ.mp3"
    )

    return f"forecast/general/audio/{new_filename}"

class ForecastGeneral(models.Model):

    legacy_id = models.PositiveBigIntegerField(null=True,blank=True,unique=True,db_index=True,)

    forecast_date       = models.DateField(null=False,blank=False)
    forecast_time       = models.TimeField(null=False, blank=False, default=time(0, 0))
    forecast_category   = models.ForeignKey(ForescastGeneralCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="forecast_general_category")

    audio_file = models.FileField(upload_to=general_forecast_audio_path,null=True,blank=True)

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

    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "General Weather Forecast"
        verbose_name_plural = "General Weather Forecasts"

    def __str__(self):
        return f"{self.forecast_date} ({self.id})"

class ForecastDiscussion(models.Model):
    forecast_date = models.DateField(null=True,blank=True)

    forecast_time = models.TimeField(null=True,blank=True,default=time(0, 0))

    forecast_category   = models.ForeignKey(ForescastGeneralCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="forecast_discussion_category")
    forecast_discussion = models.TextField(null=True,blank=True)
    forecast_text = models.CharField(max_length=255,null=True,blank=True)
    general_forecast = models.ForeignKey(ForecastGeneral,on_delete=models.SET_NULL,null=True,blank=True,related_name="forecast_discussions")
    outlook = models.CharField(max_length=1000,null=True,blank=True)
    advisory = models.CharField(max_length=1000,null=True,blank=True)
    wind_speed = models.CharField(max_length=255,null=True,blank=True)
    wind_direction = models.CharField(max_length=255,null=True,blank=True)
    wind_condition = models.CharField(max_length=255,null=True,blank=True)
    sea_state = models.CharField(max_length=255,null=True,blank=True)
    marine_wave = models.CharField(max_length=255,null=True,blank=True)
    wave = models.CharField(max_length=11,null=True,blank=True)
    forecaster_id = models.IntegerField(null=True,blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="forecast_discussions_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="forecast_discussions_updated")

    created_datetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_datetime = models.DateTimeField(auto_now=True,null=True,blank=True)
    #created_datetime = models.DateTimeField(null=True,blank=True)
    #updated_datetime = models.DateTimeField(null=True,blank=True)

    auto_update = models.DateTimeField(null=True,blank=True)

    legacy_id = models.PositiveBigIntegerField(null=True,blank=True,unique=True,db_index=True)

    class Meta:
        verbose_name = "Forecast Discussion"
        verbose_name_plural = "Forecast Discussions"
        ordering = ["-forecast_date", "-forecast_time"]

    def __str__(self):
        return f"{self.forecast_date} {self.forecast_time} ({self.id})"
    
class ForecastMarineCategory(models.Model):
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

class ForecastMarineDetailsCategory(models.Model):
    description         = models.CharField(max_length=200)
    display_order       = models.IntegerField(null=True, blank=True)
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
    forecast_time       = models.TimeField(null=False, blank=False, default=time(0, 0))
    forecast_category   = models.ForeignKey(ForecastMarineCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="forecast_marine_category")

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

    created_datetime = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_datetime = models.DateTimeField(auto_now=True,null=True, blank=True)

    class Meta:
        verbose_name = "Marine Forecast"
        verbose_name_plural = "Marine Forecasts"

    def __str__(self):
        return f"{self.forecast_date} ({self.id})"

class ForecastMarineDetails(models.Model):

    legacy_id           = models.PositiveBigIntegerField(null=True,blank=True,unique=True,db_index=True)

    marine_forecast   = models.ForeignKey(ForecastMarine,on_delete=models.SET_NULL,null=True,blank=True,related_name="forecast_marine_details")
    marine_category   = models.ForeignKey(ForecastMarineDetailsCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="forecast_marine_details")
    wind_speed          = models.CharField(max_length=10,null=True, blank=True)

    wind_direction      = models.CharField(max_length=50, null=True, blank=True)
    wind_direction_m2m  = models.ManyToManyField(WindDirection, blank=True,related_name="marine_forecast_details_forecasts_wind_direction")

    wind_condition        = models.CharField(max_length=50, null=True, blank=True)

    sea_state       = models.CharField(max_length=255,null=True, blank=True)
    sea_state_m2m   = models.ManyToManyField(SeaState, blank=True,related_name="marine_forecast_details_sea_state")

    additional_info = models.TextField(null=True,blank=True)
    
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_forecasts_details_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_forecasts_details_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "Marine Forecast Details"
        verbose_name_plural = "Marine Forecast Details"

    def __str__(self):
        return str(self.marine_category)

class TideLevelCategory(models.Model):
    description         = models.CharField(max_length=200)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="tide_level_category_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="tide_level_category_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "Tide Level Category"
        verbose_name_plural = "Tide Level Categories"

    def __str__(self):
        return str(self.description)
    
class TideDayCategory(models.Model):
    description         = models.CharField(max_length=200)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="tide_day_category_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="tide_day_category_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "Tides Day Category"
        verbose_name_plural = "Tides Day Categories"

    def __str__(self):
        return str(self.description)
    
class Tides(models.Model):

    #tide_type = models.CharField(max_length=20,choices=TIDE_TYPE_CHOICES)
    tide_level_category = models.ForeignKey(TideLevelCategory,on_delete=models.CASCADE,related_name="marine_tides_level",null=True,blank=True)

    #tide_date_type      = models.CharField(max_length=20,choices=TIDE_DATE_TYPE_CHOICES)
    tide_day_category   = models.ForeignKey(TideDayCategory,on_delete=models.CASCADE,related_name="marine_tides_day_category",null=True,blank=True)

    tide_date           = models.DateField(null=True,blank=True)
    tide_time           = models.TimeField(null=True,blank=True)

    marine_forecast     = models.ForeignKey(ForecastMarine,on_delete=models.CASCADE,related_name="marine_tides",null=True,blank=True)

    #general_forecast   = models.ForeignKey("ForecastGeneral",on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_tides",db_column="general_forecast_id")
    general_forecast    = models.CharField(max_length=20,null=True,blank=True)

    #created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_forecasts_tides_created")
    #updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="marine_forecasts_tides_updated")

    created_by          = models.CharField(max_length=255,null=True,blank=True)
    created_datetime    = models.DateTimeField(auto_now_add=True)
    updated_by          = models.CharField(max_length=255,null=True,blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["tide_date", "tide_time"]

    def __str__(self):
        return f"{self.tide_type} - {self.tide_date} {self.tide_time}"

class SunMovementCategory(models.Model):
    description         = models.CharField(max_length=200)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="sun_type_category_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="sun_type_category_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True)
    updated_datetime    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sun Movement Category"
        verbose_name_plural = "Sun Movement Categories"

    def __str__(self):
        return str(self.description)
    
class SunDayCategory(models.Model):
    description         = models.CharField(max_length=200)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="sun_day_category_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="sun_day_category_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "Sun - Day Category"
        verbose_name_plural = "Sun - Day Categories"

    def __str__(self):
        return str(self.description)

class SunRiseSet(models.Model):

    sun_move_category   = models.ForeignKey(SunMovementCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="sunrise_set_category")
    sun_day_category    = models.ForeignKey(SunDayCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="sunrise_set_day_category")
    sun_date            = models.DateField(null=True,blank=True)
    sun_time            = models.TimeField(null=True, blank=True)

    marine_forecast = models.ForeignKey(ForecastMarine,on_delete=models.CASCADE,null=True,blank=True,related_name="sunrise_set")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="sunrise_set_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="sunrise_set_updated")

    created_datetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_datetime = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "Sunrise / Sunset"
        verbose_name_plural = "Sunrise / Sunset"

    def __str__(self):
        return f"{self.sun_date} - {self.sun_type} - {self.sun_time}"
    
class MoonMovementCategory(models.Model):
    description         = models.CharField(max_length=200)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="moon_type_category_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="moon_type_category_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True)
    updated_datetime    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Moon Movement Category"
        verbose_name_plural = "Moon Movement Categories"

    def __str__(self):
        return str(self.description)
    
class MoonDayCategory(models.Model):
    description         = models.CharField(max_length=200)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="moon_day_category_created")
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="moon_day_category_updated")
    created_datetime    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_datetime    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "Moon - Day Category"
        verbose_name_plural = "Moon - Day Categories"

    def __str__(self):
        return str(self.description)

class MoonRiseSet(models.Model):

    moon_move_category = models.ForeignKey(MoonMovementCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="moonrise_set_category")
    moon_day_category  = models.ForeignKey(MoonDayCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="moonrise_set_day_category")
    moon_date       = models.DateField(null=True,blank=True)
    moon_time       = models.TimeField(null=True,blank=True)

    marine_forecast = models.ForeignKey(ForecastMarine,on_delete=models.CASCADE,null=True,blank=True,related_name="moonrise_set")

    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="moonrise_set_created")
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="moonrise_set_updated")

    created_datetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_datetime = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = "Moonrise / Moonset"
        verbose_name_plural = "Moonrise / Moonset"

    def __str__(self):
        return f"{self.moon_date} - {self.moon_type} - {self.moon_time}"