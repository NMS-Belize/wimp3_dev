""" URL configuration for wimp project. """

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.urls import include, path

from rest_framework import routers
from rest_framework.routers import DefaultRouter

#from .router import router
from rest_framework.authtoken import views

from forecasts import views as forecasts_views
from agro import views as agro_views
#from alerts import views as alert_views
from radar import views as radar_views
from users import views as user_views

from radar.api import urls as radar_api_urls
from radar.api.viewsets import RadarImagesViewSet

from . import views

app_name = 'wimp'

router = routers.DefaultRouter()
router.register('users', agro_views.UserViewSet)
router.register('groups', agro_views.GroupViewSet)

### FORECASTS API ROUTES ###
router.register('district-forecast', forecasts_views.DistrictForecastViewSet, basename='district-forecast')
router.register('district-forecasts-all', forecasts_views.DistrictForecastAllViewSet, basename='district-forecasts-all')

### AGRO API ROUTES ###
router.register('sectors',      agro_views.SectorViewSet, basename='sectors')
router.register('zones',        agro_views.ZoneViewSet, basename='zones')
router.register('districts',    agro_views.DistrictViewSet, basename='districts')
router.register('commodity',    agro_views.CommodityTypeViewSet, basename='commodity')
router.register('pest-alert-levels', agro_views.PestAlertLevelViewSet, basename='pestalertlevels')
router.register('drought-alert-levels', agro_views.DroughtAlertLevelViewSet, basename='droughtalertlevels')
router.register('action-items', agro_views.ActionItemsViewSet, basename='actionitems')
router.register('effect-items', agro_views.EffectItemsViewSet, basename='effectitems')
router.register('pest-risk', agro_views.PestRiskMainListingViewSet, basename='pestrisk')

### ALERTS API ROUTES ###
#router.register('cap-alerts', alert_views.CAPAlertsViewSet, basename='capalerts')
#router.register('cap-alert-details', alert_views.CAPAlertDetailsViewSet, basename='capalertdetails')

### RADAR SERVICES API ROUTES ###
router.register('radar-images', RadarImagesViewSet, basename='radarimages')

urlpatterns = [
    
    ### Include ADMIN URL
    path('admin/', admin.site.urls),

    ### Set the root URL (/) to redirect to the login page
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False), name='index'),
    path('dashboard/', views.dashboard, name='site_home'),
    path('accounts/login/', user_views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    ### Include API URLS
    path('api/',            include(router.urls)),
    path('api/',            include(radar_api_urls)),
   
    path('api-auth/',       include('rest_framework.urls', namespace='rest_framework')),

    ### Include URLS for Apps
    path('forecasts/',      include('forecasts.urls')),
    path('observations/',   include('observations.urls')),
    path('agro/',           include('agro.urls')),
    #path('alerts/',         include('alerts.urls')),
    path('radar/',          include('radar.urls')),
    path('users/',          include('users.urls')),
    path('inventory/',      include('inventory.urls')),
   
    #path('test_token/', user_views.test_token, name='test_token')

    ### Include URLS for WIMP App
    #path('dashboard/', views.dashboard, name='dashboard'),

    #path('', views.index, name='index'),
    # Include all default authentication URLs under the /accounts/ path
    #path('', include('django.contrib.auth.urls')),
]