from django.urls import path
from .views import DiseaseDetectionView

urlpatterns = [
    path('detect', DiseaseDetectionView.as_view(), name='disease_detect'),
]
