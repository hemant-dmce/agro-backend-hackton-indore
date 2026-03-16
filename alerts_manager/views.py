from django.db import models
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer
from authentication.models import Farmer

class FarmerNotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Return notifications for this farmer or general ones
        return Notification.objects.filter(
            models.Q(recipient=self.request.user) | models.Q(recipient=None)
        ).order_by('-created_at')

class AdminSendNotificationView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        title = request.data.get('title')
        message = request.data.get('message')
        type = request.data.get('type', 'general')
        recipient_id = request.data.get('recipient_id') # Optional: if null, send to all
        
        recipient = None
        if recipient_id:
            recipient = Farmer.objects.get(id=recipient_id)
            
        notification = Notification.objects.create(
            title=title,
            message=message,
            type=type,
            recipient=recipient
        )
        return Response(NotificationSerializer(notification).data, status=status.HTTP_201_CREATED)

class AdminStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from labor.models import Labor
        total_farmers = Farmer.objects.filter(role='farmer').count()
        total_labor = Labor.objects.count()
        active_labor = Labor.objects.filter(status='approved', availability='available').count()
        
        return Response({
            "total_farmers": total_farmers,
            "total_labor": total_labor,
            "active_labor": active_labor
        })
