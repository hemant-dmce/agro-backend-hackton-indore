from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import random

class IrrigationRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        crop_type = user.crop_type or "General"
        
        # For Demo: If soil_moisture isn't a real field, we mock it or use a default
        # In a real system, this would come from IoT sensors stored in DB
        soil_moisture_levels = ["Low", "Medium", "High"]
        soil_moisture = random.choice(soil_moisture_levels)
        
        # Mock weather data for recommendation logic
        # Ideally, this would call our own weather API view or reuse its logic
        rain_probability = random.randint(0, 100)
        
        recommendation = ""
        duration = 0

        # Rule-based logic from prompt
        if soil_moisture == "Low":
            if rain_probability < 30:
                recommendation = "आज २० मिनिटे ड्रिप सिंचन करा"
                duration = 20
            else:
                recommendation = "पावसाची शक्यता आहे, सिंचन थांबवा"
                duration = 0
        elif soil_moisture == "Medium":
            if rain_probability > 40:
                recommendation = "पावसाची शक्यता आहे, सिंचन थांबवा"
                duration = 0
            else:
                recommendation = "आज १० मिनिटे हलके सिंचन करा"
                duration = 10
        elif soil_moisture == "High":
            recommendation = "आज सिंचनाची गरज नाही"
            duration = 0
        
        # Overriding for high rain probability regardless of soil
        if rain_probability > 60 and recommendation != "आज सिंचनाची गरज नाही":
            recommendation = "पावसाची शक्यता आहे, सिंचन थांबवा"
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
