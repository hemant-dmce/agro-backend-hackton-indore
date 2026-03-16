import random
from datetime import datetime, date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class FarmingCalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        crop_type = getattr(user, 'crop_type', None)
        sowing_date_val = getattr(user, 'planting_date', None)
        
        print(f"DEBUG: FarmingCalendarView - crop_type: {crop_type}, sowing_date: {sowing_date_val}")

        # Check if crop details are set
        if not crop_type or not sowing_date_val:
            return Response({
                "crop": crop_type,
                "sowing_date": str(sowing_date_val) if sowing_date_val else None,
                "is_setup_complete": False,
                "message": "Please set crop type and sowing date in your profile to generate your farming calendar.",
                "tasks": []
            }, status=status.HTTP_200_OK)

        try:
            if isinstance(sowing_date_val, str):
                sowing_date = datetime.strptime(sowing_date_val, '%Y-%m-%d').date()
            elif isinstance(sowing_date_val, datetime):
                sowing_date = sowing_date_val.date()
            elif isinstance(sowing_date_val, date):
                sowing_date = sowing_date_val
            else:
                # Fallback to current date if type is unknown but not None
                print(f"DEBUG: Unknown date type: {type(sowing_date_val)}")
                sowing_date = date.today()
        except Exception as e:
            print(f"DEBUG: Date processing error: {e}")
            sowing_date = date.today()

        # Define crop cycles (Day offsets from sowing)
        CROP_CYCLES = {
            "Soybean": [
                {"day": 1, "task": "Sowing", "icon": "🌱", "desc": "Sow seeds at 2-3cm depth"},
                {"day": 10, "task": "First Irrigation", "icon": "💧", "desc": "Provide light watering for germination"},
                {"day": 20, "task": "Fertilizer Application", "icon": "🧪", "desc": "Apply NPK (20:20:20) mix"},
                {"day": 30, "task": "Weed Control", "icon": "🌿", "desc": "Manual weeding or selective herbicide"},
                {"day": 45, "task": "Pest Monitoring", "icon": "🐛", "desc": "Check for Aphids and Stem Fly"},
                {"day": 60, "task": "Second Fertilizer Application", "icon": "🧪", "desc": "Top dressing for pod development"},
                {"day": 90, "task": "Harvest Preparation", "icon": "🌾", "desc": "Monitor moisture content for harvest"}
            ],
            "Wheat": [
                {"day": 1, "task": "Sowing", "icon": "🌱", "desc": "Drill sowing with fertilizer"},
                {"day": 21, "task": "Crown Root Initiation", "icon": "💧", "desc": "Critical first irrigation"},
                {"day": 45, "task": "Tillering Stage", "icon": "🧪", "desc": "Top dressing with Urea"},
                {"day": 65, "task": "Jointing Stage", "icon": "💧", "desc": "Second irrigation and weed check"},
                {"day": 85, "task": "Flowering/Heading", "icon": "🐛", "desc": "Check for Rust and Aphids"},
                {"day": 105, "task": "Milking Stage", "icon": "💧", "desc": "Final irrigation"},
                {"day": 125, "task": "Dough Stage", "icon": "🌾", "desc": "Stop irrigation, allow drying"},
                {"day": 140, "task": "Harvesting", "icon": "🚜", "desc": "Harvest when grains are hard"}
            ],
            "Cotton": [
                {"day": 1, "task": "Sowing", "icon": "🌱", "desc": "Sowing at recommended spacing"},
                {"day": 30, "task": "Thinning & Weeding", "icon": "🌿", "desc": "Maintain optimum plant population"},
                {"day": 50, "task": "Flower Bud Initiation", "icon": "🧪", "desc": "Apply growth regulators and nutrients"},
                {"day": 75, "task": "Peak Flowering", "icon": "🐛", "desc": "Monitor for Bollworms"},
                {"day": 100, "task": "Boll Development", "icon": "💧", "desc": "Critical moisture requirement"},
                {"day": 130, "task": "First Picking", "icon": "🚜", "desc": "Pick when bolls are fully opened"},
                {"day": 160, "task": "Final Picking", "icon": "🚜", "desc": "Complete harvest and clear residues"}
            ]
        }

        # Normalize crop type for matching
        normalized_crop = (crop_type or "").strip().capitalize()
        if normalized_crop.endswith('s'): # Handle "Soybeans" -> "Soybean"
            normalized_crop = normalized_crop[:-1]

        # Select cycle or default to Soybean
        base_tasks = CROP_CYCLES.get(normalized_crop, CROP_CYCLES["Soybean"])
        
        # Mock weather data for adjustment
        # In real scenario, fetch from weather service
        rain_prob = random.randint(0, 100)
        temp = random.randint(20, 42)
        
        tasks_with_dates = []
        today = datetime.now().date()
        
        for base in base_tasks:
            task_date = sowing_date + timedelta(days=base["day"] - 1)
            task_status = "Completed" if task_date < today else "Upcoming"
            
            # AI Adjustments
            current_action = base["desc"]
            adjustment = None
            
            if "irrigation" in base["task"].lower():
                if rain_prob > 60:
                    adjustment = "High rain probability detected (>60%). Delaying scheduled irrigation."
                elif temp > 38:
                    adjustment = "Very high temperature detected. Recommend additional irrigation."
            
            if "Fertilizer" in base["task"] and rain_prob > 70:
                adjustment = "Heavy rain expected. Postpone fertilizer application to avoid runoff."

            tasks_with_dates.append({
                "day": base["day"],
                "date": task_date.strftime('%Y-%m-%d'),
                "task": base["task"],
                "icon": base["icon"],
                "action": current_action,
                "ai_adjustment": adjustment,
                "status": task_status,
                "is_critical": base["day"] in [1, 21, 90, 100]
            })

        try:
            current_day = (date.today() - sowing_date).days + 1
        except Exception as e:
            print(f"DEBUG: current_day calculation error: {e}")
            current_day = 1

        return Response({
            "crop": crop_type,
            "sowing_date": sowing_date.strftime('%Y-%m-%d') if sowing_date else None,
            "is_setup_complete": True,
            "current_day": current_day,
            "weather_context": {
                "rain_prob": rain_prob,
                "temp": temp
            },
            "tasks": tasks_with_dates
        }, status=status.HTTP_200_OK)


