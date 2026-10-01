import os
from rest_framework import serializers
from django.conf import settings

from forecasts.models import DistrictForecast, DistrictForecastDetails, ForecastGeneral, ForecastMarine, ForecastMarineDetails, SunRiseSet, MoonRiseSet, Tides

class DistrictForecastDetailsSerializer(serializers.ModelSerializer):
    
    district = serializers.SerializerMethodField()
    
    precip_min = serializers.SerializerMethodField()
    precip_max = serializers.SerializerMethodField()
    prob_precip_max = serializers.SerializerMethodField()
    sev_precip_max = serializers.SerializerMethodField()
    risk_precip_max = serializers.SerializerMethodField()
    ins_precip_max = serializers.SerializerMethodField()
    
    temp_min_low = serializers.SerializerMethodField()
    temp_min_high = serializers.SerializerMethodField()
    prob_temp_min = serializers.SerializerMethodField()
    sev_temp_min = serializers.SerializerMethodField()
    risk_temp_min = serializers.SerializerMethodField()
    ins_temp_min = serializers.SerializerMethodField()
    
    temp_max_low = serializers.SerializerMethodField()
    temp_max_high = serializers.SerializerMethodField()
    prob_temp_max = serializers.SerializerMethodField()
    sev_temp_max = serializers.SerializerMethodField()
    risk_temp_max = serializers.SerializerMethodField()
    ins_temp_max = serializers.SerializerMethodField()

    winds_min = serializers.SerializerMethodField()
    winds_max = serializers.SerializerMethodField()
    prob_winds = serializers.SerializerMethodField()
    sev_winds = serializers.SerializerMethodField()
    risk_winds = serializers.SerializerMethodField()
    ins_winds = serializers.SerializerMethodField()
    
    weather_conditions = serializers.SerializerMethodField()
    prob_weather_conditions = serializers.SerializerMethodField()
    sev_weather_conditions = serializers.SerializerMethodField()
    risk_weather_conditions = serializers.SerializerMethodField()
    ins_weather_conditions = serializers.SerializerMethodField()

    class Meta:
        model = DistrictForecastDetails
        fields = ['id', 'district',
                  'temp_min_low', 'temp_min_high', 'prob_temp_min', 'sev_temp_min', 'risk_temp_min', 'ins_temp_min',
                  'temp_max_low', 'temp_max_high', 'prob_temp_max', 'sev_temp_max', 'risk_temp_max', 'ins_temp_max',
                  'precip_min','precip_max', 'prob_precip_max', 'sev_precip_max', 'risk_precip_max', 'ins_precip_max',
                  'winds_min', 'winds_max', 'prob_winds', 'sev_winds', 'risk_winds', 'ins_winds',
                  'weather_conditions', 'prob_weather_conditions', 'sev_weather_conditions', 'risk_weather_conditions', 'ins_weather_conditions'
                  ]
    
    def get_district(self, obj): return obj.district.district_name if obj.district_id else ""
    
    # Precipitation MIn
    def get_precip_min(self, obj): return f"{obj.precip_min:.2f} in" if obj.precip_min is not None else ""

    # Precipitation Max
    def get_precip_max(self, obj): return f"{obj.precip_max:.2f} in" if obj.precip_max is not None else ""

    def get_prob_precip_max(self, obj):
        prob = obj.prob_precip_max
        if prob:
            return { "value": prob.description, "color": prob.color if prob.color else "" }
        return { "value": "", "color": "" }
    
    def get_sev_precip_max(self, obj):
        sev = obj.sev_precip_max
        if sev:
            return { "value": sev.description, "color": sev.color if sev.color else "" }
        return { "value": "", "color": "" }
    
    def get_risk_precip_max(self, obj):
        risk = obj.risk_precip_max
        if risk:
            return { "value": risk.description, "color": risk.color if risk.color else "" }
        return { "value": "", "color": "" }
    
    def get_ins_precip_max(self, obj): 
        return [item.description for item in obj.ins_precip_max.all()]

    # Temperature Min
    def get_temp_min_low(self, obj): return f"{obj.temp_min_low:.0f} °F" if obj.temp_min_low is not None else ""
    def get_temp_min_high(self, obj): return f"{obj.temp_min_high:.0f} °F" if obj.temp_min_high is not None else ""

    def get_prob_temp_min(self, obj):
            prob = obj.prob_temp_min
            if prob:
                return { "value": prob.description, "color": prob.color if prob.color else "" }
            return { "value": "", "color": "" }

    def get_sev_temp_min(self, obj):
        sev = obj.sev_temp_min
        if sev:
            return { "value": sev.description, "color": sev.color if sev.color else "" }
        return { "value": "", "color": "" }

    def get_risk_temp_min(self, obj):
        risk = obj.risk_temp_min
        if risk:
            return { "value": risk.description, "color": risk.color if risk.color else "" }
        return { "value": "", "color": "" }
    
    def get_ins_temp_min(self, obj): 
        return [item.description for item in obj.ins_temp_min.all()]

    # Temperature Max 
    def get_temp_max_low(self, obj): return f"{obj.temp_max_low:.0f} °F" if obj.temp_max_low is not None else ""
    def get_temp_max_high(self, obj): return f"{obj.temp_max_high:.0f} °F" if obj.temp_max_high is not None else ""

    def get_prob_temp_max(self, obj):
            prob = obj.prob_temp_max
            if prob:
                return { "value": prob.description, "color": prob.color if prob.color else "" }
            return { "value": "", "color": "" }

    def get_sev_temp_max(self, obj):
        sev = obj.sev_temp_max
        if sev:
            return { "value": sev.description, "color": sev.color if sev.color else "" }
        return { "value": "", "color": "" }
    
    def get_risk_temp_max(self, obj):
        risk = obj.risk_temp_max
        if risk:
            return { "value": risk.description, "color": risk.color if risk.color else "" }
        return { "value": "", "color": "" }
    
    def get_ins_temp_max(self, obj): 
        return [item.description for item in obj.ins_temp_max.all()]

    # Winds
    def get_winds_min(self, obj): return f"{obj.winds_min}" if obj.winds_min is not None else ""
    def get_winds_max(self, obj): return f"{obj.winds_max}" if obj.winds_max is not None else ""

    def get_prob_winds(self, obj):
            prob = obj.prob_winds
            if prob:
                return { "value": prob.description, "color": prob.color if prob.color else "" }
            return { "value": "", "color": "" }

    def get_sev_winds(self, obj):
        sev = obj.sev_winds
        if sev:
            return { "value": sev.description, "color": sev.color if sev.color else "" }
        return { "value": "", "color": "" }
    
    def get_risk_winds(self, obj):
        risk = obj.risk_winds
        if risk:
            return { "value": risk.description, "color": risk.color if risk.color else "" }
        return { "value": "", "color": "" }

    def get_ins_winds(self, obj): 
        return [item.description for item in obj.ins_winds.all()]

    # Weather Conditions
    def get_weather_conditions(self, obj): return obj.weather_conditions if obj.weather_conditions else ""
    def get_prob_weather_conditions(self, obj):
        prob = obj.prob_weather_conditions
        if prob:
            return { "value": prob.description, "color": prob.color if prob.color else "" }
        return { "value": "", "color": "" }
    
    def get_sev_weather_conditions(self, obj):
        sev = obj.sev_weather_conditions
        if sev:
            return { "value": sev.description, "color": sev.color if sev.color else "" }
        return { "value": "", "color": "" }

    def get_risk_weather_conditions(self, obj):
        risk = obj.risk_weather_conditions
        if risk:
            return { "value": risk.description, "color": risk.color if risk.color else "" }
        return { "value": "", "color": "" }
    def get_ins_weather_conditions(self, obj): 
        return [item.description for item in obj.ins_weather_conditions.all()]
   
class DistrictForecastSerializer(serializers.ModelSerializer):

    district    = serializers.SerializerMethodField()
    created_by  = serializers.SerializerMethodField()
    updated_by  = serializers.SerializerMethodField()

    latest_updated_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model   = DistrictForecast
        fields  = ['id', 'forecast_date', 'created_by', 'created_datetime', 'latest_updated_datetime', 'updated_by', 'updated_datetime', 'district']

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return ""

    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.username
        return ""

    def get_district(self, obj):

        results = []

        for detail in obj.district_forecast_details.all():

            if detail.district:

                results.append({
                    "id": detail.district.id,
                    "district_name": detail.district.district_name,
                    "details": DistrictForecastDetailsSerializer(detail).data
                })

        return results

    #risk_level  = AlertLevelSerializer(many=True,read_only=True,source='district_alerts')
    #details     = DistrictForecastDetailsSerializer(many=True,read_only=True,source='district_forecast_details')

    #district    = DistrictSerializer(read_only=True,)

class GeneralForecastSerializer(serializers.ModelSerializer):

    wind_direction_m2m = serializers.StringRelatedField(many=True)
    wind_condition_m2m = serializers.StringRelatedField(many=True)
    wind_shift_direction_m2m = serializers.StringRelatedField(many=True)
    wind_shift_condition_m2m = serializers.StringRelatedField(many=True)

    sea_state_m2m = serializers.StringRelatedField(many=True)
    sea_state_shift_m2m = serializers.StringRelatedField(many=True)

    created_by  = serializers.SerializerMethodField()
    updated_by  = serializers.SerializerMethodField()
    forecast_category = serializers.StringRelatedField()
    pdf_file  = serializers.SerializerMethodField()
    audio_file  = serializers.SerializerMethodField()

    class Meta:
        model   = ForecastGeneral
        fields = '__all__'

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return ""

    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.username
        return ""

    def get_audio_file(self, obj):
            
        forecast_time   = obj.forecast_time.strftime("%I%M_%p")
        audio_filename        = (f"{obj.forecast_date}_{forecast_time}_NMS_BZ.mp3")

        # Actual filesystem path
        audio_path = os.path.join(settings.MEDIA_ROOT,"forecast","general","audio",audio_filename)

        if os.path.exists(audio_path):
            return f"{settings.MEDIA_URL}forecast/general/audio/{audio_filename}"
        else:
            return ""

    def get_pdf_file(self, obj):
        
        forecast_time   = obj.forecast_time.strftime("%I%M_%p")
        filename        = (f"General_Forecast_{obj.forecast_date}_{forecast_time}_NMS_BZ.pdf")

        # Actual filesystem path
        pdf_path = os.path.join(settings.MEDIA_ROOT,"forecast","general","doc",filename)

        if os.path.exists(pdf_path):
            return f"{settings.MEDIA_URL}forecast/general/doc/{filename}"
        else:
            return ""

class MarineForecastDetailsSerializer(serializers.ModelSerializer):
    
    wind_direction_m2m = serializers.SlugRelatedField(many=True, read_only=True, slug_field="description")
    wind_condition_m2m = serializers.SlugRelatedField(many=True, read_only=True, slug_field="description")
    sea_state_m2m = serializers.SlugRelatedField(many=True, read_only=True, slug_field="description")

    class Meta:
        model = ForecastMarineDetails
        fields = "__all__"

class TideSerializer(serializers.ModelSerializer):

    tide_level_category = serializers.SlugRelatedField(read_only=True, slug_field="description")
    tide_day_category = serializers.SlugRelatedField(read_only=True, slug_field="description")
    tide_time = serializers.TimeField(format="%I:%M %p")

    class Meta:
        model = Tides
        fields = ["id","tide_level_category","tide_day_category","tide_date","tide_time"]


class SunSerializer(serializers.ModelSerializer):

    sun_move_category = serializers.SlugRelatedField(read_only=True, slug_field="description")
    sun_day_category = serializers.SlugRelatedField(read_only=True, slug_field="description")
    sun_time = serializers.TimeField(format="%I:%M %p")

    class Meta:
        model = SunRiseSet
        fields = ["id","sun_move_category","sun_day_category","sun_date","sun_time"]

class MoonSerializer(serializers.ModelSerializer):

    moon_move_category = serializers.SlugRelatedField(read_only=True, slug_field="description")
    moon_day_category = serializers.SlugRelatedField(read_only=True, slug_field="description")
    moon_time = serializers.TimeField(format="%I:%M %p")

    class Meta:
        model = MoonRiseSet
        fields = ["id","moon_move_category","moon_day_category","moon_date","moon_time"]

class MarineForecastSerializer(serializers.ModelSerializer):

    created_by  = serializers.SerializerMethodField()
    updated_by  = serializers.SerializerMethodField()
    forecast_category = serializers.StringRelatedField()
    #pdf_file  = serializers.SerializerMethodField()

    forecast_category = serializers.StringRelatedField()

    marine_details = MarineForecastDetailsSerializer(many=True, read_only=True, source="forecast_marine_details")
    tides   = TideSerializer(many=True, read_only=True, source="marine_tides")
    sun     = SunSerializer(many=True, read_only=True, source="sunrise_set")
    moon    = MoonSerializer(many=True, read_only=True, source="moonrise_set")

    class Meta:
        model   = ForecastMarine
        fields = ["id","legacy_id","forecast_date","forecast_time","forecast_category","synopsis","sea_surface_temperature","max_temperature", "min_temperature","advisory","cap_alerts","tropical_alerts","marine_details","tides","sun","moon","forecaster_id","created_by","created_datetime","updated_by","updated_datetime"]
        #fields = "__all__"

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return ""

    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.username
        return ""

    def get_pdf_file(self, obj):
        
        forecast_time   = obj.forecast_time.strftime("%I%M_%p")
        filename        = (f"Marine_Forecast_{obj.forecast_date}_{forecast_time}_NMS_BZ.pdf")

        # Actual filesystem path
        pdf_path = os.path.join(settings.MEDIA_ROOT,"forecast","marine","doc",filename)

        if os.path.exists(pdf_path):
            return f"{settings.MEDIA_URL}forecast/marine/doc/{filename}"
        else:
            return ""
