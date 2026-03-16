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

        # Simulate processing time
        time.sleep(1.5)

        diseases = [
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
            }
        ]

        # Select a result based on "analysis" (random for demo)
        result = random.choice(diseases)

        return Response(result)
