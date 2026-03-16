from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from authentication.models import Farmer
from .models import Labor
from .serializers import LaborSerializer, LaborPublicSerializer
from authentication.serializers import RegisterSerializer

class LaborRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_data = request.data.copy()
        user_data['role'] = 'labor'
        
        # We need a unique email, if not provided we'll generate one from phone
        if 'email' not in user_data or not user_data['email']:
            user_data['email'] = f"{user_data['phone']}@agrocast-labor.com"
            
        user_serializer = RegisterSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            
            labor_data = {
                'name': user_data.get('name'),
                'phone': user_data.get('phone'),
                'village': user_data.get('village'),
                'district': user_data.get('district'),
                'state': user_data.get('state'),
                'experience': user_data.get('experience'),
            }
            
            labor = Labor.objects.create(user=user, **labor_data)
            return Response(LaborSerializer(labor).data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LaborProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LaborSerializer

    def get_object(self):
        return get_object_or_404(Labor, user=self.request.user)

class LaborAvailabilityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        labor = get_object_or_404(Labor, user=request.user)
        availability = request.data.get('availability')
        if availability in ['available', 'busy']:
            labor.availability = availability
            labor.save()
            return Response({"status": "success", "availability": labor.availability})
        return Response({"error": "Invalid availability status"}, status=status.HTTP_400_BAD_REQUEST)

class ApprovedLaborListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LaborPublicSerializer

    def get_queryset(self):
        return Labor.objects.filter(status='approved')

class LaborDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LaborPublicSerializer
    queryset = Labor.objects.all()

class AdminLaborListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser] # Or check role='admin'
    serializer_class = LaborSerializer
    queryset = Labor.objects.all()

class AdminLaborActionView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        labor = get_object_or_404(Labor, pk=pk)
        action = request.data.get('action') # approve / reject
        if action == 'approve':
            labor.status = 'approved'
        elif action == 'reject':
            labor.status = 'rejected'
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        labor.save()
        return Response({"status": "success", "new_status": labor.status})
