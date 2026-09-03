from rest_framework import serializers
#from system_core.serializers import DistrictSerializer, AlertLevelSerializer

from forecasts.models import DistrictForecast, DistrictForecastDetails, ForecastGeneral

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
    risk_temp_min = serializers.SerializerMethodField()
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
        model = DistrictForecastDetails
        fields = ['id', 'district',
                  'temp_min', 'prob_temp_min', 'sev_temp_min', 'risk_temp_min', 'ins_temp_min',
                  'temp_max', 'prob_temp_max', 'sev_temp_max', 'risk_temp_max', 'ins_temp_max',
                  'precip_max', 'prob_precip_max', 'sev_precip_max', 'risk_precip_max', 'ins_precip_max',
                  'winds_min', 'winds_max', 'prob_winds', 'sev_winds', 'risk_winds', 'ins_winds',
                  'weather_conditions', 'prob_weather_conditions', 'sev_weather_conditions', 'risk_weather_conditions', 'ins_weather_conditions'
                  ]
    
    def get_district(self, obj): return obj.district.district_name if obj.district_id else ""
    
    # Precipitation Max
    def get_precip_max(self, obj): return f"{obj.precip_max:.1f} in" if obj.precip_max is not None else ""

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
    def get_temp_min(self, obj): return f"{obj.temp_min:.0f} °F" if obj.temp_min is not None else ""

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
    def get_temp_max(self, obj): return f"{obj.temp_max:.0f} °F" if obj.temp_max is not None else ""

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

    class Meta:
        model   = DistrictForecast
        fields  = ['id', 'forecast_date', 'created_by', 'created_datetime', 'updated_by', 'updated_datetime', 'district']

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

    created_by  = serializers.SerializerMethodField()
    updated_by  = serializers.SerializerMethodField()
    forecast_category = serializers.StringRelatedField()

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