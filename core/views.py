from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "Agro Backend Running 🚀",
        "message": "Hackathon API is live"
    })