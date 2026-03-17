import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return JsonResponse({
        "status": "Backend running successfully 🚀",
        "project": "Agro Hackathon API",
        "available_endpoints": [
            "/api/register",
            "/api/login",
            "/api/weather/",
            "/api/crop/analytics",
            "/api/risk/analysis",
            "/api/chatbot"
        ]
    })

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get("message", "").lower()
            
            # Simple Python-based Agricultural Domain Restriction
            agri_keywords = ['farm', 'crop', 'soil', 'weather', 'rain', 'temperature', 'harvest', 'irrigation', 'pest', 'disease', 'seed', 'fertilizer', 'yield', 'wheat', 'rice', 'cotton', 'soybean', 'water', 'sun', 'tractor', 'market', 'price', 'scheme', 'agri', 'plant', 'sow', 'plough', 'monsoon']
            
            # Check if general greeting
            greetings = ['hi', 'hello', 'hey']
            if any(message.strip() == g for g in greetings) or message.strip() == "":
                return JsonResponse({"response": "Hello! I am your KrushiSarthi Agricultural Assistant. How can I help you with your farm, crops, or weather today?"})

            is_agri_related = any(kw in message for kw in agri_keywords)
            
            if not is_agri_related:
                return JsonResponse({"response": "I am a strict Agricultural AI Assistant. I can only answer questions related to farming, weather, crops, and agriculture. Please ask an agriculture-related question."})
            
            # Python Rule-based Responses
            if 'weather' in message or 'rain' in message or 'temperature' in message or 'monsoon' in message:
                reply = "Weather patterns strongly dictate crop health. Ensure adequate drainage if heavy rain is expected, and maintain soil moisture above 40% during dry or hot spells. Check the dashboard for real-time risk alerts."
            elif 'pest' in message or 'disease' in message:
                reply = "For pest and disease management, regularly inspect the underside of leaves. Use appropriate fungicides or biocontrol agents at the specific early signs of infestation. You can view our Do's and Don'ts section for specific fungal diseases."
            elif 'soil' in message or 'fertilizer' in message:
                reply = "A soil health test is recommended before applying fertilizers. Maintain a balanced NPK ratio suited specifically for your crop's current growth stage."
            elif 'irrigation' in message or 'water' in message:
                reply = "Use automated smart irrigation or drip irrigation to conserve water. Set your dashboard parameters to alert you when soil moisture drops below critical levels."
            elif 'scheme' in message or 'government' in message:
                reply = "Government schemes like PM-KISAN provide financial support. Ensure your Aadhaar, land records, and bank passbooks are updated to be eligible."
            elif 'price' in message or 'market' in message:
                reply = "Market prices fluctuate based on demand. You can use the AI Price Predictor on the dashboard to get real-time price trend estimates for your specific crops."
            else:
                reply = "I am ready to help optimize your farming operations. Could you provide more specific details about your crop type, soil conditions, or weather concerns?"
                
            return JsonResponse({"response": reply})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST allowed"}, status=405)