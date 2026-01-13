"""
URL configuration for wimp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from rest_framework import routers
from agro import views as agro_views
from radar import views as radar_views

from . import views

router = routers.DefaultRouter()
router.register('users', agro_views.UserViewSet)
router.register('groups', agro_views.GroupViewSet)

### AGRO-CLIMAT SERVICES API ROUTES ###
router.register('districts', agro_views.DistrictViewSet)
router.register('commodity-types', agro_views.CommodityTypeViewSet)
router.register('commodity-categories', agro_views.CommodityCategoryViewSet)
router.register('pest-alert-levels', agro_views.PestAlertLevelViewSet)
router.register('drought-alert-levels', agro_views.DroughtAlertLevelViewSet)
router.register('action-items', agro_views.ActionItemsViewSet)
router.register('effect-items', agro_views.EffectItemsViewSet)
router.register('pest-risk', agro_views.PestRiskMainListingViewSet)

### RADAR SERVICES API ROUTES ###
router.register('radar-images', radar_views.RadarImagesViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("agro-climat-services/", include("agro.urls")),
    path("radar/", include("radar.urls")),
]