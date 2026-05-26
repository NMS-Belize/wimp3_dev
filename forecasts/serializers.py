from rest_framework import serializers
from . import models as mx

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.District
        fields = '__all__'

class AlertLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.AlertLevel
        fields = '__all__'

class DistrictForecastDetailsSerializer(serializers.ModelSerializer):
    
    district = serializers.SerializerMethodField()
    
    precip_max = serializers.SerializerMethodField()
    prob_precip_max = serializers.SerializerMethodField()
    sev_precip_max = serializers.SerializerMethodField()
    risk_precip_max = serializers.SerializerMethodField()
    ins_precip_max = serializers.SerializerMethodField()
    
    temp_min = serializers.SerializerMethodField()
    prob_temp_min = serializers.SerializerMethodField()
    sev_temp_min = serializers.SerializerMethodField()
    risk_temp_max = serializers.SerializerMethodField()
    ins_temp_min = serializers.SerializerMethodField()
    
    temp_max = serializers.SerializerMethodField()
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
        model = mx.DistrictForecastDetails
        fields = ['id', 'district', 
                  'temp_min', 'prob_temp_min', 'sev_temp_min', 'risk_temp_min', 'ins_temp_min',
                  'temp_max', 'prob_temp_max', 'sev_temp_max', 'risk_temp_max', 'ins_temp_max',
                  'precip_max', 'prob_precip_max', 'sev_precip_max', 'risk_precip_max', 'ins_precip_max',
                  'winds_min', 'winds_max', 'prob_winds', 'sev_winds', 'risk_winds', 'ins_winds',
                  'weather_conditions', 'prob_weather_conditions', 'sev_weather_conditions', 'risk_weather_conditions', 'ins_weather_conditions'
                  ]
    
    def get_district(self, obj): return obj.district.district_name if obj.district_id else ""
    
    def get_precip_max(self, obj): return f"{obj.precip_max:.1f} in" if obj.precip_max is not None else ""
    def get_prob_precip_max(self, obj): return obj.prob_precip_max.description if obj.prob_precip_max else ""
    def get_sev_precip_max(self, obj): return obj.sev_precip_max.description if obj.sev_precip_max else ""
    def get_risk_precip_max(self, obj): return obj.risk_precip_max.description if obj.risk_precip_max else ""
    def get_ins_precip_max(self, obj): return obj.ins_precip_max.description if obj.ins_precip_max else ""

    def get_temp_min(self, obj): return f"{obj.temp_min:.1f} °F" if obj.temp_min is not None else ""
    def get_prob_temp_min(self, obj): return obj.prob_temp_min.description if obj.prob_temp_min else ""
    def get_sev_temp_min(self, obj): return obj.sev_temp_min.description if obj.sev_temp_min else ""
    def get_risk_temp_min(self, obj): return obj.risk_temp_min.description if obj.risk_temp_min else ""
    def get_ins_temp_min(self, obj): return obj.ins_temp_min.description if obj.ins_temp_min else ""

    def get_temp_max(self, obj): return f"{obj.temp_max:.1f} °F" if obj.temp_max is not None else ""
    def get_prob_temp_max(self, obj): return obj.prob_temp_max.description if obj.prob_temp_max else ""
    def get_sev_temp_max(self, obj): return obj.sev_temp_max.description if obj.sev_temp_max else ""
    def get_risk_temp_max(self, obj): return obj.risk_temp_max.description if obj.risk_temp_max else ""
    def get_ins_temp_max(self, obj): return obj.ins_temp_max.description if obj.ins_temp_max else ""

    def get_winds_min(self, obj): return f"{obj.winds_min}" if obj.winds_min is not None else ""
    def get_winds_max(self, obj): return f"{obj.winds_max}" if obj.winds_max is not None else ""
    def get_prob_winds(self, obj): return obj.prob_winds.description if obj.prob_winds else ""
    def get_sev_winds(self, obj): return obj.sev_winds.description if obj.sev_winds else ""
    def get_risk_winds(self, obj): return obj.risk_winds.description if obj.risk_winds else ""
    def get_ins_winds(self, obj): return obj.ins_winds.description if obj.ins_winds else ""

    def get_weather_conditions(self, obj): return obj.weather_conditions if obj.weather_conditions else ""
    def get_prob_weather_conditions(self, obj): return obj.prob_weather_conditions.description if obj.prob_weather_conditions else ""
    def get_sev_weather_conditions(self, obj): return obj.sev_weather_conditions.description if obj.sev_weather_conditions else ""
    def get_risk_weather_conditions(self, obj): return obj.risk_weather_conditions.description if obj.risk_weather_conditions else ""
    def get_ins_weather_conditions(self, obj): return obj.ins_weather_conditions.description if obj.ins_weather_conditions else ""

class DistrictForecastSerializer(serializers.ModelSerializer):

    class Meta:
        model = mx.DistrictForecast
        fields = ['id', 'forecast_date', 'is_published', 'created_datetime', 'updated_datetime', 'df_details']

    df_details = DistrictForecastDetailsSerializer(
        many=True,
        read_only=True,
        source='district_forecast_details'
    )