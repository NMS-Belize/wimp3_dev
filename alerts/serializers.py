from rest_framework import serializers
from .models import CAPAlerts, CAPAlertDetails, TropicalWeatherAlertsCategory, TropicalWeatherAlerts

class CAPAlertsAllSerializer(serializers.ModelSerializer):
    class Meta:
        model   = CAPAlerts
        fields  = '__all__'

    def validate_description(self, value):
        print("Incoming length:", len(value))
        return value

class CAPAlertDetailsSerializer(serializers.ModelSerializer):

    url = serializers.URLField(source="identifier.link",read_only=True)

    class Meta:
        model = CAPAlertDetails
        fields = '__all__'

class CAPAlertsSerializer(serializers.ModelSerializer):

    details = CAPAlertDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = CAPAlerts
        fields = '__all__'

    def validate_description(self, value):
        print("Incoming length:", len(value))
        return value

class TropicalAlertsSerializer(serializers.ModelSerializer):

    storm_category = serializers.StringRelatedField()
    created_by  = serializers.SerializerMethodField()
    updated_by  = serializers.SerializerMethodField()
    
    class Meta:
        model   = TropicalWeatherAlerts
        fields  = '__all__'

    def get_created_by(self, obj):
            if obj.created_by:
                return obj.created_by.get_full_name() or obj.created_by.username
            return ""
    
    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.username
        return ""

class TropicalAlertsCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model   = TropicalWeatherAlertsCategory
        fields  = '__all__'