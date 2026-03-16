from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import random

class IrrigationRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        crop_type = request.GET.get('crop_type') or user.crop_type or "General"
        
        # For Demo: If soil_moisture isn't a real field, we mock it or use a default
        # In a real system, this would come from IoT sensors stored in DB
        soil_moisture_levels = ["Low", "Medium", "High"]
        soil_moisture = random.choice(soil_moisture_levels)
        
        # Mock weather data for recommendation logic
        # Ideally, this would call our own weather API view or reuse its logic
        rain_probability = random.randint(0, 100)
        
        recommendation = ""
        duration = 0

        # Simple crop logic simulation to make it look dynamic based on crop
        base_durations = {
            'sugarcane': 45,
            'rice': 60,
            'wheat': 30,
            'cotton': 40,
            'soybean': 25,
            'maize': 35,
            'general': 20
        }
        
        crop_key = crop_type.lower()
        base_duration = base_durations.get(crop_key, base_durations['general'])

        # Rule-based logic from prompt
        if soil_moisture == "Low":
            if rain_probability < 30:
                recommendation = "आज सिंचन करा" if request.GET.get('lang') == 'mr' else "Irrigation Recommended"
                duration = base_duration
            else:
                recommendation = "पावसाची शक्यता आहे, सिंचन थांबवा" if request.GET.get('lang') == 'mr' else "Wait – Rain Expected"
                duration = 0
        elif soil_moisture == "Medium":
            if rain_probability > 40:
                recommendation = "पावसाची शक्यता आहे, सिंचन थांबवा" if request.GET.get('lang') == 'mr' else "Wait – Rain Expected"
                duration = 0
            else:
                recommendation = "आज हलके सिंचन करा" if request.GET.get('lang') == 'mr' else "Light Irrigation Recommended"
                duration = int(base_duration * 0.5)
        elif soil_moisture == "High":
            recommendation = "आज सिंचनाची गरज नाही" if request.GET.get('lang') == 'mr' else "No Irrigation Needed Today"
            duration = 0
        
        # Overriding for high rain probability regardless of soil
        if rain_probability > 60 and "गरज नाही" not in recommendation and "Needed" not in recommendation:
            recommendation = "पावसाची शक्यता आहे, सिंचन थांबवा" if request.GET.get('lang') == 'mr' else "Wait – Rain Expected"
            duration = 0

        data = {
            "recommendation": recommendation,
            "soil_moisture": soil_moisture,
            "rain_probability": rain_probability,
            "crop_type": crop_type,
            "recommended_duration": duration,
            "status": "Success"
        }
        
        return Response(data)
