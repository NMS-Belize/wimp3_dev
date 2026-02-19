from rest_framework import routers
from .viewsets import RadarImagesViewSet

router = routers.DefaultRouter()
router.register(r'radar-images', RadarImagesViewSet, basename='radarimages')

urlpatterns = router.urls
