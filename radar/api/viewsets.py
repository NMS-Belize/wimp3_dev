from rest_framework import viewsets
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..models import RadarImages
from ..api import serializers as sx
from .permissions import ReadOnly
from .serializers import RadarImagesSerializer

### API VIEWSETS
#class RadarImagesViewSet(viewsets.ModelViewSet):
class RadarImagesViewSet(viewsets.ReadOnlyModelViewSet):
   permission_classes = [ReadOnly]
   #authentication_classes = []  # IMPORTANT
   queryset = RadarImages.objects.filter(is_published=True).order_by('id')
   serializer_class = sx.RadarImagesSerializer