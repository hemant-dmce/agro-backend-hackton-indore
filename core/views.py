from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "Backend running successfully 🚀",
        "project": "Agro Hackathon API",
        "available_endpoints": [
            "/api/register",
            "/api/login",
            "/api/weather/",
            "/api/crop/analytics",
            "/api/risk/analysis"
        ]
    })