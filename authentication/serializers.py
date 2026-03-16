from rest_framework import serializers
from .models import Farmer

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = [
            'id', 'name', 'phone', 'email', 'role', 'village', 'district',
            'farm_location', 'farm_size', 
            'crop_type', 'latitude', 'longitude', 'soil_type', 
            'irrigation_type', 'planting_date', 'crop_variety', 'created_at',
            'is_staff', 'is_superuser', 'assigned_district'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Farmer
        fields = [
            'name', 'phone', 'email', 'password', 'role', 'village', 'district',
            'farm_location', 'farm_size', 
            'crop_type', 'latitude', 'longitude', 'soil_type', 
            'irrigation_type', 'planting_date', 'crop_variety', 'assigned_district'
        ]

    def create(self, validated_data):
        user = Farmer.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data['password'],
            name=validated_data['name'],
            phone=validated_data['phone'],
            role=validated_data.get('role', 'farmer'),
            village=validated_data.get('village'),
            district=validated_data.get('district'),
            farm_location=validated_data.get('farm_location'),
            farm_size=validated_data.get('farm_size'),
            crop_type=validated_data.get('crop_type'),
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude'),
            assigned_district=validated_data.get('assigned_district')
        )
        return user
