from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.urls import include, path
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from agro import views as agro_views
from forecasts import views as forecasts_views
from alerts import views as alert_views
from radar import views as radar_views
from system_core import views as system_core_views
from users import views as user_views

from . import views

app_name = 'wimp'

router = routers.DefaultRouter()
router.register('users',    agro_views.UserViewSet)
router.register('groups',   agro_views.GroupViewSet)

### FORECASTS API ROUTES ###
router.register('district-forecast',            forecasts_views.DistrictForecastViewSet,        basename='district-forecast')
router.register('district-forecasts-all',       forecasts_views.DistrictForecastAllViewSet,     basename='district-forecasts-all')
router.register('general-weather-forecast',     forecasts_views.GeneralForecastViewSet,         basename='general-weather-forecast')
router.register('general-weather-forecast-all', forecasts_views.GeneralForecastAllViewSet,      basename='general-weather-forecast-all')

### AGRO API ROUTES ###
router.register('sectors',      agro_views.SectorViewSet, basename='sectors')
router.register('zones',        agro_views.ZoneViewSet, basename='zones')
router.register('districts',    agro_views.DistrictViewSet, basename='districts')
router.register('commodity',    agro_views.CommodityTypeViewSet, basename='commodity')
router.register('drought-alert-levels', agro_views.DroughtAlertLevelViewSet, basename='droughtalertlevels')
router.register('action-items', agro_views.ActionItemsViewSet, basename='actionitems')
router.register('effect-items', agro_views.EffectItemsViewSet, basename='effectitems')
router.register('pest-risk',    agro_views.PestRiskViewSet, basename='pestrisk')

#router.register('alert-levels', agro_views.AlertLevelViewSet, basename='pestalertlevels')

### ALERTS API ROUTES ###
router.register('cap', alert_views.CAPAlertsViewSet, basename='cap')
router.register('cap-all', alert_views.CAPAlertsAllViewSet, basename='cap-all')
#router.register('cap-alert-details', alert_views.CAPAlertDetailsViewSet, basename='capalertdetails')

### RADAR SERVICES API ROUTES ###
router.register('radar-images', radar_views.RadarImagesViewSet, basename='radarimages')

urlpatterns = [
    
    ### Include ADMIN URL
    path('admin/', admin.site.urls),

    ### Set the root URL (/) to redirect to the login page
    path('',            RedirectView.as_view(url='/accounts/login/', permanent=False), name='index'),
    path('dashboard/',  views.dashboard, name='site_home'),
    path('accounts/login/', user_views.login, name='login'),
    path('logout/',     auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    ### Include API URLS
    path('api/',            include(router.urls)),
    path('api/forecast-files/', forecasts_views.WIMP2FilesAPIView.as_view(), name='forecast-files'),
    path('api-auth/',       include('rest_framework.urls', namespace='rest_framework')),

    ### Include URLS for Apps
    path('forecasts/',      include('forecasts.urls')),
    path('observations/',   include('observations.urls')),
    path('agro/',           include('agro.urls')),
    path('alerts/',         include('alerts.urls')),
    path('radar/',          include('radar.urls')),
    path('users/',          include('users.urls')),
    path('inventory/',      include('inventory.urls')),
    path('system/',         include('system_core.urls')),
    path("select2/",        include("django_select2.urls")),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)