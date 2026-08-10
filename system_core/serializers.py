from rest_framework import serializers
from system_core.models import District, AlertLevel, Months, Zone

class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Months
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'

class AlertLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertLevel
        fields = '__all__'