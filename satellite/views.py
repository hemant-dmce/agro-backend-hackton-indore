import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class SatelliteCropHealthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Simulated NDVI data based on requested ranges:
        # 0.7 – 1.0 → Healthy vegetation
        # 0.4 – 0.6 → Moderate vegetation
        # 0.2 – 0.3 → Crop stress
        # 0.0 – 0.2 → Severe vegetation loss
        
        user = request.user
        lat = user.latitude
        lon = user.longitude

        if not lat or not lon:
            return Response({
                "error": "Location not set",
                "latitude": None,
                "longitude": None
            })

        ndvi = round(random.uniform(0.15, 0.95), 2)
        
        if ndvi >= 0.7:
            health = "Healthy"
            status = "Excellent vegetation cover"
            risk = "Low"
        elif ndvi >= 0.4:
            health = "Moderate"
            status = "Good vegetation cover"
            risk = "Low"
        elif ndvi >= 0.2:
            health = "Stressed"
            status = "Crop stress detected"
            risk = "Medium"
        else:
            health = "Severe"
            status = "Severe vegetation loss"
            risk = "High"
            
        # Simulate a grid of NDVI values around the center
        # We'll create a 5x5 grid
        grid_data = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                # Offset by approx 0.002 degrees (approx 200m)
                grid_lat = lat + (i * 0.002)
                grid_lon = lon + (j * 0.002)
                # Randomize NDVI slightly around the main value
                grid_ndvi = max(0, min(1.0, round(ndvi + random.uniform(-0.15, 0.15), 2)))
                grid_data.append({
                    "lat": grid_lat,
                    "lon": grid_lon,
                    "ndvi": grid_ndvi
                })

        return Response({
            "ndvi": ndvi,
            "crop_health": health,
            "drought_risk": risk,
            "vegetation_status": status,
            "latitude": lat,
            "longitude": lon,
            "grid_data": grid_data
        })
