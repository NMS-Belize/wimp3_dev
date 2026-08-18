import os
from rest_framework import serializers
from radar.models import RadarImages

from urllib.parse import urljoin
from django.conf import settings


class RadarImagesSerializer(serializers.ModelSerializer):

    image_url_full = serializers.SerializerMethodField()
    local_image_url = serializers.SerializerMethodField()

    class Meta:
        model = RadarImages
        fields = ['image_url','web_directory','image_title','image_url_full','local_image_url']

    def get_image_url_full(self, obj):
    
            if obj.image_url:
                filename = os.path.basename(obj.image_url)
    
                # Ensure web_directory ends with a slash
                web_dir = obj.web_directory
                if not web_dir.endswith('/'):
                    web_dir += '/'
                    
                # Combine with fixed base URL
                full_url = urljoin('https://nms.gov.bz/', f"{web_dir}{filename}")
                return full_url
            return None
    

    def get_local_image_url(self, obj):
        if not obj.image_url:
            return None

        request = self.context.get("request")

        # Get just the filename
        filename = os.path.basename(obj.image_url)

        # /media/radar/filename.png
        media_url = f"{settings.MEDIA_URL.rstrip('/')}/radar/{filename}"

        # https://wimp3.nms.gov.bz/media/radar/filename.png
        if request:
            return request.build_absolute_uri(media_url)

        return media_url