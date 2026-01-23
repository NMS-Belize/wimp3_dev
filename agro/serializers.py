from rest_framework import serializers
from . import models as mx

class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.Months
        fields = '__all__'

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.CommodityCategory
        fields = '__all__'

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.Zone
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.District
        fields = '__all__'

class CommodityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.CommodityType
        fields = '__all__'
    
class PestAlertLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.PestAlertLevel
        fields = '__all__'

class DroughtAlertLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.DroughtAlertLevel
        fields = '__all__'

class ActionItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.PestRiskAction
        fields = '__all__'

class EffectItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.PestRiskEffect
        fields = '__all__'

class PestRiskEntryDetailsSerializer(serializers.ModelSerializer):
    #pest_risk_listing_id = PestRiskEntryMainListingSerializer(read_only=True)
    zone = serializers.SerializerMethodField()
    pest_alert = serializers.SerializerMethodField()
    drought_alert = serializers.SerializerMethodField()
    temp_min = serializers.SerializerMethodField()
    temp_max = serializers.SerializerMethodField()
    precip_min = serializers.SerializerMethodField()
    precip_max = serializers.SerializerMethodField()
    effect = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()

    class Meta:
        model = mx.PestRiskEntryDetails
        fields = ['pest_risk_listing_id', 'zone', 'pest_alert', 'drought_alert', 'temp_min','temp_max','precip_min','precip_max','effect','info','actions']
    
    def get_zone(self, obj): 
        return f"{obj.district_id.district_area}" if obj.district_id is not None else "N/A"
    
    def get_pest_alert(self, obj): 
        return f"{obj.pest_alert_lvl_id.description}" if obj.pest_alert_lvl_id is not None else "N/A"
    
    def get_drought_alert(self, obj): 
        return f"{obj.drought_alert_lvl_id.description}" if obj.drought_alert_lvl_id is not None else "N/A"
    
    def get_temp_min(self, obj): 
        return f"{obj.temp_min:.1f} °F" if obj.temp_min is not None else "N/A"
    
    def get_temp_max(self, obj): 
        return f"{obj.temp_min:.1f} °F" if obj.temp_min is not None else "N/A"
    
    def get_precip_min(self, obj): 
        return f"{obj.precip_min:.1f} mm" if obj.precip_min is not None else "N/A"
    
    def get_precip_max(self, obj): 
        return f"{obj.precip_max:.1f} mm" if obj.precip_max is not None else "N/A"
    
    def get_effect(self, obj): 
        return f"{obj.effect.effect_description}" if obj.effect is not None else "N/A"
    
    def get_actions(self, obj): 
        return f"{obj.actions.action_description}" if obj.actions is not None else "N/A"
    
class PestRiskEntryMainListingSerializer(serializers.ModelSerializer):
    commodity = serializers.SerializerMethodField()
    months = serializers.SerializerMethodField()

    pest_risk_details = PestRiskEntryDetailsSerializer(
        many=True,
        read_only=True,
        source='pest_risk_entries'
    )

    class Meta:
        model = mx.PestRiskEntryMainListing
        fields = ['id', 'months', 'year', 'commodity', 'pest_risk_details']

    def get_commodity(self, obj): 
        return f"{obj.commodity.description}" if obj.commodity is not None else "N/A"
    
    def get_months(self, obj):
        month_map = {
            "1": "JAN", "2": "FEB", "3": "MAR", "4": "APR",
            "5": "MAY", "6": "JUN", "7": "JUL", "8": "AUG",
            "9": "SEP", "10": "OCT", "11": "NOV", "12": "DEC"
        }
        if obj.months:
            return ", ".join([month_map.get(str(m), f"Unknown({m})") for m in obj.months])
        return "N/A"
    
   