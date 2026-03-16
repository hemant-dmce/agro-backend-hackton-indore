from django.urls import path
from .views import RegisterView, ProfileView, CustomTokenObtainPairView, SaveFarmLocationView, CoordinatorListView, CoordinatorCreateView, FarmerListAdminView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('save-farm-location/', SaveFarmLocationView.as_view(), name='save_farm_location'),
    path('coordinators/', CoordinatorListView.as_view(), name='coordinator_list'),
    path('coordinators/create', CoordinatorCreateView.as_view(), name='coordinator_create'),
    path('admin/farmers', FarmerListAdminView.as_view(), name='farmer_list_admin'),
]
