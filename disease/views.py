from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
import time
import random

class DiseaseDetectionView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # In a real scenario, we would use:
        # image_file = request.data.get('image')
        # import cv2
        # import tensorflow as tf
        # model = tf.keras.models.load_model('crop_disease_model.h5')
        # ... processing logic ...

        image_file = request.FILES.get('image')
        filename = getattr(image_file, 'name', '').lower()

        # Simulate processing time
        time.sleep(1.5)

        diseases_db = [
            {
                "disease_name": "Leaf Spot Disease",
                "confidence": "92%",
                "treatment": "Remove infected leaves and maintain dry foliage. Improve air circulation around plants.",
                "pesticide": "Copper Fungicide Spray"
            },
            {
                "disease_name": "Powdery Mildew",
                "confidence": "88%",
                "treatment": "Increase sunlight exposure and reduce humidity. Prune overcrowded areas.",
                "pesticide": "Sulfur-based Fungicide"
            },
            {
                "disease_name": "Bacterial Blight",
                "confidence": "85%",
                "treatment": "Use disease-free seeds and avoid overhead irrigation. Rotate crops seasonally.",
                "pesticide": "Streptomycin Sulfate"
            },
            {
                "disease_name": "Yellow Rust",
                "confidence": "94%",
                "treatment": "Destroy infected crop residues and use rust-resistant varieties.",
                "pesticide": "Propiconazole 25% EC"
            },
            {
                "disease_name": "Corn Smut",
                "confidence": "96%",
                "treatment": "Remove and destroy infected galls before they burst. Practice crop rotation and avoid mechanical injury to plants.",
                "pesticide": "Fungicides are largely ineffective; rely on resistant varieties and sanitation."
            },
            {
                "disease_name": "Late Blight",
                "confidence": "91%",
                "treatment": "Remove infected plants immediately. Avoid overhead watering to keep foliage dry.",
                "pesticide": "Chlorothalonil or Mancozeb"
            },
            {
                "disease_name": "Fusarium Wilt",
                "confidence": "89%",
                "treatment": "Remove and destroy infected plants. Plant resistant varieties in the future.",
                "pesticide": "Soil solarization; no highly effective chemical treatment exists."
            }
        ]

        # Smart Keyword Detection for demo purposes
        result = None
        if 'smut' in filename or 'corn' in filename:
            result = diseases_db[4] # Corn Smut
        elif 'rust' in filename:
            result = diseases_db[3]
        elif 'mildew' in filename:
            result = diseases_db[1]
        elif 'spot' in filename:
            result = diseases_db[0]
        elif 'blight' in filename:
            result = diseases_db[5]
        elif 'wilt' in filename:
            result = diseases_db[6]
        
        # If no keywords match, use a deterministic hash of the filename so the same image gets the same result
        if not result:
            hash_val = sum(ord(c) for c in filename) if filename else random.randint(0, 100)
            index = hash_val % len(diseases_db)
            result = diseases_db[index]
            
            # Slightly randomize the confidence score for realism based on the hash
            base_conf = int(result["confidence"].replace("%", ""))
            randomized_conf = min(99, max(75, base_conf + (hash_val % 10 - 5)))
            result = result.copy()
            result["confidence"] = f"{randomized_conf}%"

        return Response(result)
