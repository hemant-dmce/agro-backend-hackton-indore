from django.urls import path
from .views import IrrigationRecommendationView

urlpatterns = [
    path('recommendation', IrrigationRecommendationView.as_view(), name='irrigation_recommendation'),
]
