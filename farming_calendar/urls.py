from django.urls import path
from .views import FarmingCalendarView

urlpatterns = [
    path('', FarmingCalendarView.as_view(), name='farming-calendar'),
]
