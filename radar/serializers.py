from rest_framework import serializers
from . import models as mx
import os
from urllib.parse import urljoin

class RadarImagesSerializer(serializers.ModelSerializer):

    # Custom field
    image_url_full = serializers.SerializerMethodField()

    class Meta:
        model = mx.RadarImages
        #fields = '__all__'
        fields = ['image_url_full']

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