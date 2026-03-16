from django.urls import path
from .views import FarmWeatherForecastView, VillageWeatherView, DisasterAlertView

urlpatterns = [
    path('farm-forecast/', FarmWeatherForecastView.as_view(), name='farm-forecast'),
    path('village-weather/', VillageWeatherView.as_view(), name='village-weather'),
    path('disaster-alerts/', DisasterAlertView.as_view(), name='disaster-alerts'),
]
