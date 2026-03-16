from rest_framework import serializers
from .models import Labor

class LaborSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labor
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at']

class LaborPublicSerializer(serializers.ModelSerializer):
    """Serializer for farmers to view labor profiles"""
    class Meta:
        model = Labor
        fields = ['id', 'name', 'phone', 'village', 'district', 'state', 'experience', 'availability']
