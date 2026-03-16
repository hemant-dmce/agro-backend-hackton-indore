from django.urls import path
from .views import FarmerNotificationListView, AdminSendNotificationView, AdminStatsView

urlpatterns = [
    path('my-notifications', FarmerNotificationListView.as_view(), name='farmer_notifications'),
    path('admin/send', AdminSendNotificationView.as_view(), name='admin_send_notification'),
    path('admin/stats', AdminStatsView.as_view(), name='admin_stats'),
]
