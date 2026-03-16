from django.contrib import admin
from django.urls import path, include
from .views import home

from authentication.views import (
    RegisterView, ProfileView, CustomTokenObtainPairView,
    SaveFarmLocationView, CoordinatorListView, CoordinatorCreateView,
    FarmerListAdminView, CoordinatorFarmersView, CoordinatorSendAlertView
)

from crop.views import CropAnalyticsView, CropSummaryView, CropReportDownloadView
from risk.views import RiskAnalysisView
from rest_framework_simplejwt.views import TokenRefreshView
from satellite.views import SatelliteCropHealthView


urlpatterns = [
    # Root health check
    path('', home),

    path('admin/', admin.site.urls),

    # Authentication APIs
    path('api/register', RegisterView.as_view(), name='register'),
    path('api/login', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/profile', ProfileView.as_view(), name='profile'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/save-farm-location/', SaveFarmLocationView.as_view(), name='save_farm_location'),

    # Weather
    path('api/weather/', include('weather.urls')),

    # Crop
    path('api/crop/analytics', CropAnalyticsView.as_view(), name='crop_analytics'),
    path('api/crop/summary', CropSummaryView.as_view(), name='crop_summary'),
    path('api/crop-report', CropReportDownloadView.as_view(), name='crop_report_download'),

    # Risk
    path('api/risk/analysis', RiskAnalysisView.as_view(), name='risk_analysis'),

    # Other modules
    path('api/irrigation/', include('irrigation.urls')),
    path('api/disease/', include('disease.urls')),
    path('api/labor/', include('labor.urls')),
    path('api/alerts-manager/', include('alerts_manager.urls')),

    # Coordinator APIs
    path('api/authentication/coordinators/', CoordinatorListView.as_view(), name='coordinator_list'),
    path('api/authentication/coordinators/create', CoordinatorCreateView.as_view(), name='coordinator_create'),
    path('api/authentication/admin/farmers', FarmerListAdminView.as_view(), name='farmer_list_admin'),
    path('api/authentication/coordinators/farmers', CoordinatorFarmersView.as_view(), name='coordinator_farmers'),
    path('api/authentication/coordinators/send-alert', CoordinatorSendAlertView.as_view(), name='coordinator_send_alert'),

    # Satellite
    path('api/satellite/crop-health', SatelliteCropHealthView.as_view(), name='satellite_crop_health'),

    # Farming calendar
    path('api/farming-calendar', include('farming_calendar.urls')),
]