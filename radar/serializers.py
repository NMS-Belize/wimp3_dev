from rest_framework import serializers
from . import models as mx

class RadarImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = mx.RadarImages
        fields = '__all__'