from rest_framework import serializers
from . import models as mx

class CAPAlertsSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.CAPAlerts
        fields = '__all__'

    def validate_description(self, value):
        print("Incoming length:", len(value))
        return value


class CAPAlertDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.CAPAlertDetails
        fields = '__all__'