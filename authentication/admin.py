from django.contrib import admin
from .models import Farmer

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'farm_location', 'crop_type', 'created_at')
    search_fields = ('name', 'email', 'phone', 'farm_location')
    list_filter = ('crop_type', 'created_at')
