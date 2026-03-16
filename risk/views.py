from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import random

class RiskAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Mock data for Risk Analytics
        risks = [
            {
                "type": "Flood Risk",
                "level": random.choice(["Low", "Medium", "High"]),
                "description": "High probability of intense rainfall in the next 48 hours.",
                "action": "Ensure proper drainage in downstream fields."
            },
            {
                "type": "Drought Risk",
                "level": random.choice(["Low", "Medium"]),
                "description": "Prolonged dry spell predicted for the coming week.",
                "action": "Optimize irrigation schedules."
            },
            {
                "type": "Storm Risk",
                "level": random.choice(["Low", "Medium", "High"]),
                "description": "Strong winds may affect tall crops.",
                "action": "Secure temporary structures and equipment."
            },
            {
                "type": "Fungal Disease Risk",
                "level": random.choice(["Low", "Medium", "High"]),
                "description": "High humidity conditions favor fungal growth.",
                "action": "Monitor crop leaves for signs of infection."
            }
        ]
        
        data = {
            "risks": risks,
            "risk_trend": [
                {"week": "Week 1", "level": random.randint(10, 30)},
                {"week": "Week 2", "level": random.randint(30, 50)},
                {"week": "Week 3", "level": random.randint(20, 40)},
                {"week": "Week 4", "level": random.randint(15, 25)},
            ],
            "weather_impact": [
                {"factor": "Heat", "impact": random.randint(40, 70)},
                {"factor": "Rain", "impact": random.randint(20, 50)},
                {"factor": "Wind", "impact": random.randint(10, 30)},
            ]
        }
        
        return Response(data)
