from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import FarmerSerializer, RegisterSerializer
from .models import Farmer
from django.db.models import Q
from rest_framework.views import APIView

class RegisterView(generics.CreateAPIView):
    queryset = Farmer.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FarmerSerializer

    def get_object(self):
        return self.request.user

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Support both email and phone as identifier
        identifier = request.data.get('email') # Front-end might still use 'email' key
        if identifier and '@' not in identifier:
            # Try to find user by phone if it doesn't look like an email
            try:
                user = Farmer.objects.get(phone=identifier)
                request.data['email'] = user.email
            except Farmer.DoesNotExist:
                pass
                
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = Farmer.objects.get(email=request.data['email'])
            response.data['user'] = FarmerSerializer(user).data
        return response

from rest_framework.views import APIView

class SaveFarmLocationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        
        if latitude is None or longitude is None:
            return Response({"error": "Latitude and longitude are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        user.latitude = latitude
        user.longitude = longitude
        user.save()
        
        return Response({"message": "Farm location saved successfully.", "latitude": user.latitude, "longitude": user.longitude}, status=status.HTTP_200_OK)

# Coordinator views
class CoordinatorListView(generics.ListAPIView):
    serializer_class = FarmerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Farmer.objects.filter(role='coordinator')

class CoordinatorCreateView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return Response({"error": "Only admins can create coordinators."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set role to coordinator
        coordinator = Farmer.objects.create_user(
            email=serializer.validated_data.get('email'),
            password=serializer.validated_data['password'],
            name=serializer.validated_data['name'],
            phone=serializer.validated_data['phone'],
            role='coordinator',
            assigned_district=serializer.validated_data.get('assigned_district', '')
        )
        
        return Response(FarmerSerializer(coordinator).data, status=status.HTTP_201_CREATED)

class FarmerListAdminView(generics.ListAPIView):
    serializer_class = FarmerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Farmer.objects.filter(role='farmer')

# Coordinator-specific views - filter by district
class CoordinatorFarmersView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Check if user is coordinator or admin
        if user.role != 'coordinator' and not user.is_staff and not user.is_superuser:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        district = request.query_params.get('district')
        
        # For coordinator, filter by their assigned district
        if user.role == 'coordinator' and user.assigned_district:
            # Use case-insensitive match for district
            farmers = Farmer.objects.filter(
                role='farmer',
                district__icontains=user.assigned_district
            )
        elif district:
            farmers = Farmer.objects.filter(role='farmer', district__icontains=district)
        else:
            farmers = Farmer.objects.filter(role='farmer')
            
        serializer = FarmerSerializer(farmers, many=True)
        return Response(serializer.data)

class CoordinatorLaborView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Check if user is coordinator or admin
        if user.role != 'coordinator' and not user.is_staff and not user.is_superuser:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        # For now, return empty list - will use labor API
        from labor.models import Labor
        
        if user.role == 'coordinator' and user.assigned_district:
            labor_list = Labor.objects.filter(district=user.assigned_district)
        else:
            labor_list = Labor.objects.all()
            
        serializer = Labor.objects.none()
        return Response([])

class CoordinatorSendAlertView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        # Only coordinators and admins can send alerts
        if user.role != 'coordinator' and not user.is_staff and not user.is_superuser:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        title = request.data.get('title')
        message = request.data.get('message')
        alert_type = request.data.get('type', 'general')
        
        if not title or not message:
            return Response({"error": "Title and message are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get farmers in coordinator's district
        if user.role == 'coordinator' and user.assigned_district:
            farmers = Farmer.objects.filter(
                role='farmer',
                district__icontains=user.assigned_district
            )
        else:
            farmers = Farmer.objects.filter(role='farmer')
        
        # Create notifications for all farmers in the district
        from alerts_manager.models import Notification
        from django.core.mail import send_mail
        notifications_created = 0
        
        for farmer in farmers:
            Notification.objects.create(
                recipient=farmer,
                title=title,
                message=message,
                type=alert_type,
                is_read=False
            )
            notifications_created += 1
            
            # SMS placeholder - log to console
            print(f"[SMS] Would send to {farmer.phone}: {title} - {message}")
            
            # Send email to each farmer if they have an email address
            if farmer.email:
                try:
                    email_subject = f"[AgroCast Alert] {title}"
                    email_message = f"""
Dear {farmer.get_full_name() or farmer.username},

You have received a new alert from AgroCast:

Title: {title}
Type: {alert_type}
Message: {message}

This alert was sent to farmers in your district.

Thank you,
AgroCast Team
"""
                    send_mail(
                        email_subject,
                        email_message,
                        'AgroCast <noreply@agrocast.com>',
                        [farmer.email],
                        fail_silently=False,
                    )
                    print(f"[EMAIL] Sent alert email to {farmer.email}")
                except Exception as e:
                    print(f"[EMAIL ERROR] Failed to send email to {farmer.email}: {e}")
        
        # Also send a copy to the coordinator's designated email
        try:
            coordinator_email = 'adwaitmhaske05@gmail.com'
            email_subject = f"[AgroCast Alert] {title}"
            email_message = f"""
Dear Coordinator,

You have sent an alert to farmers:

Title: {title}
Type: {alert_type}
Message: {message}

This alert was sent to {notifications_created} farmer(s) in your district.

Thank you,
AgroCast Team
"""
            send_mail(
                email_subject,
                email_message,
                'AgroCast <noreply@agrocast.com>',
                [coordinator_email],
                fail_silently=False,
            )
            print(f"[EMAIL] Sent confirmation email to coordinator at {coordinator_email}")
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send coordinator email: {e}")
        
        return Response({
            "message": f"Alert sent to {notifications_created} farmers in your district. Notification emails sent.",
            "count": notifications_created
        }, status=status.HTTP_201_CREATED)
