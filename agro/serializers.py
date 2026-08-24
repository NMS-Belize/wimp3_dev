from rest_framework import serializers
from agro.models import Sector, Commodity, PestRiskAction, PestRiskEffect, PestRiskEntryDetails, PestRisk
from system_core.models import AlertLevel

from system_core.serializers import DistrictSerializer, AlertLevelSerializer, ZoneSerializer

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'

class CommodityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'

class DroughtAlertLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertLevel
        fields = '__all__'

class ActionItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PestRiskAction
        fields = '__all__'

class EffectItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PestRiskEffect
        fields = '__all__'

class PestRiskEntryDetailsSerializer(serializers.ModelSerializer):
    #pest_risk_listing_id = PestRiskEntryMainListingSerializer(read_only=True)
    #commodity = serializers.SerializerMethodField()
    zone = serializers.SerializerMethodField()
    pest_alert = serializers.SerializerMethodField()
    pest_alert_color_hex = serializers.SerializerMethodField()
    drought_alert = serializers.SerializerMethodField()
    drought_alert_color_hex = serializers.SerializerMethodField()
    temp_min = serializers.SerializerMethodField()
    temp_max = serializers.SerializerMethodField()
    precip_min = serializers.SerializerMethodField()
    precip_max = serializers.SerializerMethodField()
    effect = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    is_published = serializers.SerializerMethodField()

    class Meta:
        model = PestRiskEntryDetails
        fields = ['zone', 'pest_alert','pest_alert_color_hex', 'drought_alert', 'drought_alert_color_hex', 'temp_min','temp_max','precip_min','precip_max','effect','info','actions', 'is_published']

    '''def get_commodity(self, obj): 
            return f"{obj.commodity_id.description}" if obj.commodity_id is not None else "N/A"'''
    
    def get_zone(self, obj): 
        return f"{obj.district_id.district_name}" if obj.district_id is not None else "N/A"
    
    def get_pest_alert(self, obj): 
        return f"{obj.pest_alert_lvl_id.description}" if obj.pest_alert_lvl_id is not None else "N/A"
    
    def get_pest_alert_color_hex(self, obj): 
        return f"{obj.pest_alert_lvl_id.color}" if obj.pest_alert_lvl_id is not None else "N/A"
    
    def get_drought_alert(self, obj): 
        return f"{obj.drought_alert_lvl_id.description}" if obj.drought_alert_lvl_id is not None else "N/A"
    
    def get_drought_alert_color_hex(self, obj): 
        return f"{obj.drought_alert_lvl_id.color_hex}" if obj.drought_alert_lvl_id is not None else "N/A"
    
    def get_temp_min(self, obj): 
        return f"{obj.temp_min:.1f} °F" if obj.temp_min is not None else "N/A"
    
    def get_temp_max(self, obj): 
        return f"{obj.temp_min:.1f} °F" if obj.temp_min is not None else "N/A"
    
    def get_precip_min(self, obj): 
        return f"{obj.precip_min:.1f} mm" if obj.precip_min is not None else "N/A"
    
    def get_precip_max(self, obj): 
        return f"{obj.precip_max:.1f} mm" if obj.precip_max is not None else "N/A"
    
    def get_effect(self, obj): 
        effects = obj.effect.all()
        if not effects:
            return []

        return [
            effect.effect_description
            for effect in effects
        ]

    def get_actions(self, obj):
        actions = obj.actions.all()

        if not actions:
            return []

        return [
            action.action_description
            for action in actions
        ]

    def get_info(self, obj):
        info_items = obj.info.all()

        if not info_items:
            return []

        return [
            item.info_description
            for item in info_items
        ]

    def get_is_published(self, obj): 
            return f"{obj.is_published}" if obj.is_published is not None else "N/A"
    
class PestRiskSerializer(serializers.ModelSerializer):

    months = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()
    '''pest_risk_details = PestRiskEntryDetailsSerializer(
        many=True,
        read_only=True,
        source='pest_risk_entries'
    )'''

    class Meta:
        model = PestRisk
        fields = ['id', 'months', 'year', 'sector' ]

    #def get_commodity(self, obj): 
    #    return f"{obj.commodity.description}" if obj.commodity is not None else "N/A"
    
    def get_months(self, obj):
        month_map = {
            "1": "JAN", "2": "FEB", "3": "MAR", "4": "APR",
            "5": "MAY", "6": "JUN", "7": "JUL", "8": "AUG",
            "9": "SEP", "10": "OCT", "11": "NOV", "12": "DEC"
        }
        if obj.months:
            return ", ".join([month_map.get(str(m), f"Unknown({m})") for m in obj.months])
        return ""

    def get_sector(self, obj):

        grouped = {}

        entries = obj.pest_risk_entries.all()

        for entry in entries:

            if not entry.commodity_id:
                continue

            commodity = entry.commodity_id
            sector = commodity.sector

            sector_name = sector.description
            commodity_name = commodity.description

            # Create sector
            if sector_name not in grouped:
                grouped[sector_name] = {}

            # Create commodity inside sector
            if commodity_name not in grouped[sector_name]:
                grouped[sector_name][commodity_name] = []

            # Add pest risk entry
            grouped[sector_name][commodity_name].append(entry)

        # Convert dictionary to API structure
        result = []

        for sector_name, commodities in grouped.items():

            commodity_list = []

            for commodity_name, entries in commodities.items():

                commodity_list.append({
                    'commodity_name': commodity_name,
                    'details':
                        PestRiskEntryDetailsSerializer(
                            entries,
                            many=True,
                            context=self.context
                        ).data
                })

            result.append({
                'sector_name': sector_name,
                'commodities': commodity_list
            })

        return result