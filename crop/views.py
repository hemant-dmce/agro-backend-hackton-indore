from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpResponse
import random
import io
from datetime import datetime
from fpdf import FPDF

class CropSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        crop = user.crop_type or "Rice"
        
        # In a real app, we'd fetch these from actual models/APIs
        ndvi = round(random.uniform(0.3, 0.9), 2)
        moisture = random.randint(30, 80)
        temp = random.randint(20, 35)
        rain_prob = random.randint(0, 100)
        
        summary = self._generate_summary(crop, ndvi, moisture, temp, rain_prob)
        
        return Response({
            "crop": crop,
            "summary": summary,
            "metrics": {
                "ndvi": ndvi,
                "soil_moisture": moisture,
                "temperature": temp,
                "rain_probability": rain_prob
            }
        })

    def _generate_summary(self, crop, ndvi, moisture, temp, rain_prob):
        if crop.lower() == "rice":
            base = "Satellite NDVI analysis indicates good vegetation density across the rice field." if ndvi > 0.6 else "NDVI analysis shows moderate growth. Rice fields require consistent monitoring."
            moist_str = "Current moisture levels support optimal rice growth." if moisture > 50 else "Lower moisture detected; consider increasing irrigation for better paddock flooding."
            advice = "Maintain irrigation schedule and monitor for pest activity during the flowering stage."
            return f"{base} {moist_str} {advice}"
        
        elif crop.lower() == "wheat":
            base = "Satellite vegetation analysis shows healthy crop development with moderate soil moisture." if ndvi > 0.5 else "Wheat growth appears steady, though canopy density is slightly below average."
            temp_str = "Current temperature conditions are favorable for wheat growth." if 15 <= temp <= 25 else "Ambient temperature is fluctuating; monitor for heat stress."
            advice = "No immediate irrigation adjustment is required." if rain_prob < 30 else "Light rainfall expected; hold irrigation to save water."
            return f"{base} {temp_str} {advice}"
        
        elif crop.lower() == "cotton":
            return f"Cotton crop health is overall positive with an NDVI of {ndvi}. Soil moisture at {moisture}% is within the target range for vegetative branching. Watch for pest risks due to current temperature trends."
            
        elif crop.lower() == "soybean":
            return f"Soybean fields showing high nitrogen fixation activity based on green-spectrum analysis. Moisture levels ({moisture}%) are adequate for the current pod-filling stage. Temperature is optimal."
            
        elif crop.lower() == "maize":
            return f"Maize health index is rated high. Canopy structure is robust. Rainfall probability of {rain_prob}% might reduce the need for the next irrigation cycle. Overall yield projection remains stable."
            
        else:
            return f"General crop summary for {crop}: Vegetation health ({ndvi}) is stable. Soil moisture is at {moisture}%. Weather conditions are moderate for typical agricultural cycles."

class CropReportDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        crop = user.crop_type or "General"
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 24)
        pdf.set_text_color(31, 175, 92) # Nature-500 color approx
        pdf.cell(190, 20, "AgroCast - Precision Agriculture Report", ln=True, align='C')
        
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(100, 116, 139) # slate color
        pdf.cell(190, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
        pdf.ln(10)
        
        # Farm Details Section
        pdf.set_fill_color(248, 250, 252)
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(190, 12, " Farm Details", ln=True, fill=True)
        pdf.set_font("Arial", '', 12)
        pdf.ln(5)
        pdf.cell(95, 10, f"Farmer Name: {user.name}")
        pdf.cell(95, 10, f"Location: {user.latitude}, {user.longitude}", ln=True)
        pdf.cell(95, 10, f"Selected Crop: {crop}")
        pdf.cell(95, 10, f"Soil Type: {user.soil_type}", ln=True)
        pdf.cell(95, 10, f"Irrigation Type: {user.irrigation_type}")
        pdf.ln(15)
        
        # Health Metrics
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 12, " Crop Health & Environmental Metrics", ln=True, fill=True)
        pdf.set_font("Arial", '', 12)
        pdf.ln(5)
        ndvi = round(random.uniform(0.4, 0.9), 2)
        pdf.cell(95, 10, f"NDVI Vegetation Index: {ndvi}")
        pdf.cell(95, 10, f"Soil Moisture: {random.randint(40, 75)}%", ln=True)
        pdf.cell(95, 10, f"Temperature: {random.randint(22, 34)}C")
        pdf.cell(95, 10, f"Humidity: {random.randint(30, 60)}%", ln=True)
        pdf.ln(10)
        
        # AI Summary
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 12, " AI-Powered Crop Summary", ln=True, fill=True)
        pdf.set_font("Arial", 'I', 11)
        pdf.ln(5)
        summary_text = CropSummaryView()._generate_summary(crop, ndvi, 50, 25, 10)
        pdf.multi_cell(190, 10, summary_text)
        pdf.ln(10)
        
        # Recommendations
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 12, " Strategic Recommendations", ln=True, fill=True)
        pdf.set_font("Arial", '', 11)
        pdf.ln(5)
        pdf.cell(10, 10, "-")
        pdf.cell(180, 10, "Increase sensor sampling frequency during the upcoming weather shifts.", ln=True)
        pdf.cell(10, 10, "-")
        pdf.cell(180, 10, "Apply nitrogen-based fertilizer in the cool evening hours to prevent evaporation.", ln=True)
        pdf.cell(10, 10, "-")
        pdf.cell(180, 10, "Check secondary drainage channels for early monsoon preparation.", ln=True)
        
        # Output PDF
        output = io.BytesIO()
        pdf_content = pdf.output(dest='S')
        output.write(pdf_content.encode('latin-1'))
        output.seek(0)
        
        filename = f"AgroCast_Crop_Report_{crop.replace(' ', '_')}.pdf"
        response = HttpResponse(output, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

class CropAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Mock data for Crop Analytics
        data = {
            "crop_health": random.choice(["Optimal", "Good", "Fair"]),
            "soil_moisture": random.randint(30, 80),
            "growth_stage": random.choice(["Vegetative", "Flowering", "Ripening"]),
            "irrigation_status": random.choice(["Required", "Not Required", "Scheduled"]),
            "growth_trend": [
                {"day": "Mon", "value": random.randint(10, 20)},
                {"day": "Tue", "value": random.randint(20, 30)},
                {"day": "Wed", "value": random.randint(30, 45)},
                {"day": "Thu", "value": random.randint(45, 60)},
                {"day": "Fri", "value": random.randint(60, 80)},
            ],
            "soil_moisture_levels": [
                {"time": "06:00", "moisture": random.randint(40, 50)},
                {"time": "12:00", "moisture": random.randint(30, 40)},
                {"time": "18:00", "moisture": random.randint(50, 60)},
                {"time": "00:00", "moisture": random.randint(55, 65)},
            ]
        }
        
        return Response(data)
