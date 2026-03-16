from django.urls import path
from .views import (
    LaborRegisterView, LaborProfileView, LaborAvailabilityView,
    ApprovedLaborListView, LaborDetailView, AdminLaborListView, AdminLaborActionView
)

urlpatterns = [
    path('register', LaborRegisterView.as_view(), name='labor_register'),
    path('profile', LaborProfileView.as_view(), name='labor_profile'),
    path('availability', LaborAvailabilityView.as_view(), name='labor_availability'),
    path('list', ApprovedLaborListView.as_view(), name='labor_list'),
    path('detail/<int:pk>', LaborDetailView.as_view(), name='labor_detail'),
    path('admin/all', AdminLaborListView.as_view(), name='admin_labor_list'),
    path('admin/action/<int:pk>', AdminLaborActionView.as_view(), name='admin_labor_action'),
]
