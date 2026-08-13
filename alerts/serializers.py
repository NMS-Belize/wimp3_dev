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
    class Meta:
        model   = TropicalWeatherAlerts
        fields  = '__all__'

class TropicalAlertsCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model   = TropicalWeatherAlertsCategory
        fields  = '__all__'