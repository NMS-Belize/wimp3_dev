from rest_framework import serializers
from .models import WeatherCodes

class WeatherCodeSerializer(serializers.ModelSerializer):

    icon_day = serializers.SerializerMethodField()
    icon_night = serializers.SerializerMethodField()

    class Meta:
        model = WeatherCodes
        fields = ['code','description','icon_day','icon_night']

    def get_icon_day(self, obj):
        if obj.icon_day and obj.icon_day.icon:
            return self.get_icon_url(obj.icon_day.icon)
        return None

    def get_icon_night(self, obj):
        if obj.icon_night and obj.icon_night.icon:
            return self.get_icon_url(obj.icon_night.icon)
        return None

    def get_icon_url(self, icon):
        request = self.context.get('request')

        url = icon.url

        if request:
            return request.build_absolute_uri(url)

        return url