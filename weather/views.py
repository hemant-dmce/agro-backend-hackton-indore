import requests
import random
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Maharashtra villages with approximate coordinates (district-wise)
MAHARASHTRA_VILLAGES = {
    'Thane': [
        {'name': 'Thane City', 'lat': 19.1860, 'lon': 72.9752},
        {'name': 'Kalyan', 'lat': 19.2437, 'lon': 73.1350},
        {'name': 'Ulhasnagar', 'lat': 19.2000, 'lon': 73.1667},
        {'name': 'Ambernath', 'lat': 19.2014, 'lon': 73.1865},
        {'name': 'Bhiwandi', 'lat': 19.3000, 'lon': 73.0667},
        {'name': 'Vasai', 'lat': 19.3833, 'lon': 72.8333},
        {'name': 'Virar', 'lat': 19.4567, 'lon': 72.8111},
        {'name': 'Navi Mumbai', 'lat': 19.0330, 'lon': 73.0299},
        {'name': 'Panvel', 'lat': 18.9944, 'lon': 73.1116},
        {'name': 'Kasarwadi', 'lat': 19.1833, 'lon': 72.9500},
    ],
    'Pune': [
        {'name': 'Shirdi', 'lat': 19.7978, 'lon': 74.4785},
        {'name': 'Shrigonda', 'lat': 18.6186, 'lon': 74.3167},
        {'name': 'Rahata', 'lat': 19.8533, 'lon': 74.4750},
        {'name': 'Parner', 'lat': 18.9333, 'lon': 74.6000},
        {'name': 'Karjat', 'lat': 18.9167, 'lon': 74.9833},
    ],
    'Pune': [
        {'name': 'Haveli', 'lat': 18.5933, 'lon': 73.9328},
        {'name': 'Mulshi', 'lat': 18.4500, 'lon': 73.6500},
        {'name': 'Maval', 'lat': 18.6500, 'lon': 73.5500},
        {'name': 'Velhe', 'lat': 18.2833, 'lon': 73.7500},
        {'name': 'Bhor', 'lat': 18.1500, 'lon': 73.8000},
    ],
    'Nagpur': [
        {'name': 'Nagpur Rural', 'lat': 21.1497, 'lon': 79.0823},
        {'name': 'Ramtek', 'lat': 21.3833, 'lon': 79.3333},
        {'name': 'Kamptee', 'lat': 21.2500, 'lon': 79.4833},
        {'name': 'Katol', 'lat': 21.2667, 'lon': 78.9333},
        {'name': 'Narkhed', 'lat': 21.4667, 'lon': 78.8333},
    ],
    'Nashik': [
        {'name': 'Nashik Rural', 'lat': 20.0112, 'lon': 73.7903},
        {'name': 'Igatpuri', 'lat': 19.7000, 'lon': 73.5667},
        {'name': 'Dindori', 'lat': 20.1167, 'lon': 73.8833},
        {'name': 'Sinnar', 'lat': 20.8833, 'lon': 74.0500},
        {'name': 'Yeola', 'lat': 20.9333, 'lon': 74.5000},
    ],
    'Mumbai Suburban': [
        {'name': 'Andheri', 'lat': 19.1197, 'lon': 72.8468},
        {'name': 'Borivali', 'lat': 19.2287, 'lon': 72.8562},
        {'name': 'Kurla', 'lat': 19.0667, 'lon': 72.8833},
        {'name': 'Mulund', 'lat': 19.1725, 'lon': 72.9571},
        {'name': 'Thane', 'lat': 19.1860, 'lon': 72.9752},
    ],
    'Thane': [
        {'name': 'Thane Rural', 'lat': 19.3000, 'lon': 73.0667},
        {'name': 'Kalyan', 'lat': 19.2437, 'lon': 73.1350},
        {'name': 'Ulhasnagar', 'lat': 19.2000, 'lon': 73.1667},
        {'name': 'Ambernath', 'lat': 19.2014, 'lon': 73.1865},
        {'name': 'Bhiwandi', 'lat': 19.3000, 'lon': 73.0667},
    ],
    'Solapur': [
        {'name': 'Solapur Rural', 'lat': 17.6800, 'lon': 75.9200},
        {'name': 'Malshiras', 'lat': 17.9833, 'lon': 74.9500},
        {'name': 'Pandharpur', 'lat': 17.6833, 'lon': 75.3167},
        {'name': 'Sangola', 'lat': 17.4333, 'lon': 75.0667},
        {'name': 'Akalkot', 'lat': 17.7333, 'lon': 76.2000},
    ],
    'Aurangabad': [
        {'name': 'Aurangabad Rural', 'lat': 19.8762, 'lon': 75.3433},
        {'name': 'Paithan', 'lat': 19.4833, 'lon': 75.3833},
        {'name': 'Gangapur', 'lat': 19.8333, 'lon': 75.1667},
        {'name': 'Vaijapur', 'lat': 19.9333, 'lon': 74.7333},
        {'name': 'Sillod', 'lat': 20.3167, 'lon': 75.0167},
    ],
    'Kolhapur': [
        {'name': 'Kolhapur Rural', 'lat': 16.7050, 'lon': 74.2433},
        {'name': 'Karveer', 'lat': 16.8500, 'lon': 74.2333},
        {'name': 'Panhala', 'lat': 16.8000, 'lon': 74.1000},
        {'name': 'Shirol', 'lat': 16.9500, 'lon': 74.0500},
        {'name': 'Gadhinglaj', 'lat': 16.2333, 'lon': 74.3500},
    ],
    'Navi Mumbai': [
        {'name': 'Vashi', 'lat': 19.0667, 'lon': 73.0333},
        {'name': 'Nerul', 'lat': 19.0333, 'lon': 73.0167},
        {'name': 'Belapur', 'lat': 19.0175, 'lon': 73.0388},
        {'name': 'Panvel', 'lat': 18.9833, 'lon': 73.1167},
        {'name': 'Kharghar', 'lat': 19.0500, 'lon': 73.0667},
    ],
}

# Add more districts with villages
for district in ['Satara', 'Ratnagiri', 'Sindhudurg', 'Palghar', 'Dhule', 'Jalgaon', 'Amravati', 'Wardha', 'Bhandara', 'Gadchiroli', 'Chandrapur', 'Gondia', 'Washim', 'Hingoli', 'Parbhani', 'Latur', 'Osmanabad', 'Beed', 'Jalna', 'Nanded', 'Akola', 'Buldhana']:
    if district not in MAHARASHTRA_VILLAGES:
        # Add generic villages for each district (center point)
        base_coords = {
            'Satara': (17.6833, 74.0000), 'Ratnagiri': (16.8333, 73.3000), 'Sindhudurg': (16.5667, 73.5333),
            'Palghar': (19.7000, 72.7500), 'Dhule': (20.9000, 74.7833), 'Jalgaon': (21.0000, 75.5667),
            'Amravati': (20.9333, 77.7500), 'Wardha': (20.7500, 78.6000), 'Bhandara': (21.1667, 79.6500),
            'Gadchiroli': (19.8000, 80.3000), 'Chandrapur': (19.9667, 79.3000), 'Gondia': (21.4667, 80.2000),
            'Washim': (20.1167, 77.1500), 'Hingoli': (19.7333, 77.1000), 'Parbhani': (19.2667, 76.7833),
            'Latur': (18.4000, 80.9500), 'Osmanabad': (18.1833, 76.0333), 'Beed': (18.9833, 75.7500),
            'Jalna': (19.8333, 75.8833), 'Nanded': (19.1500, 77.3333), 'Akola': (20.7000, 77.0167),
            'Buldhana': (20.5333, 75.5667)
        }
        lat, lon = base_coords.get(district, (20.0, 75.0))
        MAHARASHTRA_VILLAGES[district] = [
            {'name': f'{district} HQ', 'lat': lat, 'lon': lon},
            {'name': f'Village 1', 'lat': lat + 0.05, 'lon': lon + 0.05},
            {'name': 'Village 2', 'lat': lat - 0.05, 'lon': lon + 0.03},
            {'name': 'Village 3', 'lat': lat + 0.03, 'lon': lon - 0.04},
            {'name': 'Village 4', 'lat': lat - 0.02, 'lon': lon - 0.02},
        ]


class VillageWeatherView(APIView):
    """Get weather for all villages in a coordinator's district"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Check if user is a coordinator
        if user.role != 'coordinator':
            return Response(
                {"error": "Only coordinators can access village weather data"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # If no district assigned, use a default district for demo
        district_input = user.assigned_district if user.assigned_district else "Thane"
        # Capitalize the first letter to match our dictionary keys
        district = district_input.capitalize() if district_input else "Thane"
        
        # Also try lowercase version
        villages = MAHARASHTRA_VILLAGES.get(district, MAHARASHTRA_VILLAGES.get(district_input, []))
        
        if not villages:
            # Try to find any matching district
            for key in MAHARASHTRA_VILLAGES.keys():
                if key.lower() == district_input.lower():
                    villages = MAHARASHTRA_VILLAGES[key]
                    district = key
                    break
        
        # If still no villages, generate sample villages
        if not villages:
            # Generate sample villages based on any available district
            sample_lat, sample_lon = 19.0760, 72.8777  # Mumbai as default
            villages = [
                {'name': 'Sample Village 1', 'lat': sample_lat, 'lon': sample_lon},
                {'name': 'Sample Village 2', 'lat': sample_lat + 0.05, 'lon': sample_lon + 0.05},
                {'name': 'Sample Village 3', 'lat': sample_lat - 0.03, 'lon': sample_lon + 0.02},
                {'name': 'Sample Village 4', 'lat': sample_lat + 0.02, 'lon': sample_lon - 0.03},
                {'name': 'Sample Village 5', 'lat': sample_lat - 0.04, 'lon': sample_lon - 0.02},
            ]
        
        now = datetime.now()
        month = now.month
        
        # Determine season
        if month in [11, 12, 1, 2]:
            base_temp = 20.0
            max_rain = 15
            desc = "Clear"
        elif month in [3, 4, 5, 6]:
            base_temp = 36.0
            max_rain = 25
            desc = "Hot"
        elif month in [7, 8, 9]:
            base_temp = 28.0
            max_rain = 95
            desc = "Rainy"
        else:
            base_temp = 26.0
            max_rain = 40
            desc = "Cloudy"
        
        village_weather = []
        for village in villages:
            # Generate slight variations per village
            temp_variation = random.uniform(-2, 2)
            rain_variation = random.randint(-10, 10)
            
            village_weather.append({
                'village_name': village['name'],
                'district': district,
                'coordinates': {
                    'lat': village['lat'],
                    'lon': village['lon']
                },
                'current': {
                    'temperature': round(base_temp + temp_variation, 1),
                    'humidity': random.randint(40, 80),
                    'wind_speed': round(random.uniform(5, 20), 1),
                    'rain_chance': min(100, max(0, max_rain + rain_variation)),
                    'condition': desc,
                },
                'forecast': [
                    {
                        'day': (now + timedelta(days=i)).strftime('%A'),
                        'temp': round(base_temp + temp_variation + random.uniform(-3, 3), 1),
                        'rain_prob': min(100, max(0, max_rain + rain_variation + random.randint(-20, 20)))
                    }
                    for i in range(5)
                ],
                'advisory': self._generate_advisory(base_temp + temp_variation, max_rain + rain_variation, month)
            })
        
        return Response({
            'district': district,
            'total_villages': len(village_weather),
            'villages': village_weather
        }, status=status.HTTP_200_OK)
    
    def _generate_advisory(self, temp, rain_chance, month):
        """Generate agricultural advisory based on weather"""
        advisories = []
        
        if temp > 35:
            advisories.append("High temperature - advise farmers to irrigate early morning or late evening")
        elif temp < 15:
            advisories.append("Cool temperature - delay sowing of summer crops")
        
        if rain_chance > 70:
            advisories.append("High rain expected - postpone pesticide/fertilizer application")
        elif rain_chance < 20 and month in [7, 8, 9]:
            advisories.append("Low rain - advise farmers to start supplementary irrigation")
        
        if month in [7, 8, 9]:
            advisories.append("Monsoon season - watch for fungal diseases in crops")
        elif month in [3, 4, 5]:
            advisories.append("Summer season - ensure adequate water supply for standing crops")
        
        if not advisories:
            advisories.append("Weather conditions are favorable for agricultural activities")
        
        return advisories

class FarmWeatherForecastView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Check if coordinates exist
        if user.latitude is None or user.longitude is None:
            return Response(
                {"error": "Please select your farm location to view weather forecasts."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        lat = user.latitude
        lon = user.longitude
        api_key = "dummy_key_for_hackathon" # In a real scenario, use settings.OPENWEATHER_API_KEY
        
        # In a real app we would call:
        # url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        # response = requests.get(url, timeout=5)
        # if response.status_code == 200:
        #     return Response(response.json(), status=status.HTTP_200_OK)
        
        # For the hackathon demo, we generate high-quality hyper-local mock data based on the farm coordinates
        # SEASONAL LOGIC: Adjust weather based on month
        now = datetime.now()
        month = now.month
        
        # Determine season and base values
        # Northern Hemisphere approximate (India context)
        # Nov-Feb: Winter, Mar-Jun: Summer/Pre-monsoon, Jul-Sep: Monsoon, Oct: Post-monsoon
        
        if month in [11, 12, 1, 2]: # Winter
            base_temp = random.uniform(10.0, 25.0)
            max_rain_prob = 15 # Very low rain in winter
            description = "Clear Skies"
            icon = "sunny"
        elif month in [3, 4, 5, 6]: # Summer / Pre-monsoon
            base_temp = random.uniform(30.0, 42.0)
            max_rain_prob = 25 # Rare pre-monsoon showers
            description = "Hot & Sunny"
            icon = "sunny"
        elif month in [7, 8, 9]: # Monsoon
            base_temp = random.uniform(25.0, 32.0)
            max_rain_prob = 95 # High rain probability
            description = "Heavy Rain"
            icon = "rain"
        else: # Post-monsoon (October)
            base_temp = random.uniform(22.0, 30.0)
            max_rain_prob = 40
            description = "Partly Cloudy"
            icon = "cloudy"

        current_temp = round(base_temp, 1)
        humidity = random.randint(30, 90) if month in [7, 8, 9] else random.randint(20, 60)
        wind_speed = round(random.uniform(5.0, 25.0), 1)
        
        # If it's monsoon, current rain chance is high
        rain_chance = random.randint(60, 100) if month in [7, 8, 9] else random.randint(0, max_rain_prob)
        
        # Generate 5-Day Forecast
        daily_forecast = []
        
        for i in range(5):
            date = now + timedelta(days=i)
            
            # Determine condition based on max_rain_prob
            daily_rain_prob = random.randint(0, 100)
            if daily_rain_prob < max_rain_prob:
                condition = random.choice(['Rain', 'Drizzle', 'Thunderstorm'])
                icon_name = 'rain' if condition != 'Thunderstorm' else 'storm'
            else:
                condition = 'Clear' if daily_rain_prob > 80 else 'Clouds'
                icon_name = 'sunny' if condition == 'Clear' else 'cloudy'
                daily_rain_prob = random.randint(0, 20) # Low prob if clear/clouds
            
            daily_forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "day_name": date.strftime("%A") if i > 0 else "Today",
                "temp": round(current_temp + random.uniform(-4.0, 4.0), 1),
                "condition": condition,
                "icon": icon_name,
                "rain_prob": daily_rain_prob
            })
        
        # Generate hourly trend data for charts (Temperature and Rainfall probability)
        hourly_trend = []
        temp = current_temp
        for i in range(8):
            time = now + timedelta(hours=i*3)
            # Simple diurnal cycle simulation: warmer mid-day
            hour = time.hour
            temp_offset = 0
            if 10 <= hour <= 16: temp_offset = 5
            elif 0 <= hour <= 5: temp_offset = -5
            
            current_hourly_temp = temp + temp_offset + random.uniform(-1, 1)
            
            hourly_trend.append({
                "time": time.strftime("%H:00"),
                "temp": round(current_hourly_temp, 1),
                "rain_prob": random.randint(0, max_rain_prob),
                "wind_speed": round(random.uniform(5.0, 20.0), 1)
            })

        # Advanced Agronomic Metrics
        # Soil temp is usually ± a few degrees from ambient
        soil_temp = round(current_temp + random.uniform(-2, 2), 1)
        # Dew point is always <= ambient temp
        dew_point = round(current_temp - (random.uniform(2, 10)), 1)
        # UV Index depends on month/description (very simplistic)
        uv_index = random.randint(1, 11) if month in [3, 4, 5, 6] else random.randint(1, 6)
        # ET (Evapotranspiration) in mm
        et = round(random.uniform(2.0, 7.0), 2)
        pressure = random.randint(1005, 1015)
        visibility = random.randint(5, 10)

        data = {
            "location": {"lat": lat, "lon": lon},
            "current": {
                "temperature": current_temp,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "rain_chance": rain_chance,
                "description": description,
                "icon": icon,
                "soil_temperature": soil_temp,
                "dew_point": dew_point,
                "uv_index": uv_index,
                "evapotranspiration": et,
                "pressure": pressure,
                "visibility": visibility
            },
            "daily_forecast": daily_forecast,
            "hourly_trend": hourly_trend
        }
        
        return Response(data, status=status.HTTP_200_OK)

class DisasterAlertView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        if user.latitude is None or user.longitude is None:
            return Response([], status=status.HTTP_200_OK)
            
        # Get weather data to base alerts on
        # In a real app, we'd fetch actual API data here
        now = datetime.now()
        month = now.month
        
        # We reuse some logic from FarmWeatherForecastView to stay consistent
        if month in [3, 4, 5, 6]: # Summer
            base_temp = random.uniform(35.0, 45.0)
            rain_chance = random.randint(0, 20)
        elif month in [7, 8, 9]: # Monsoon
            base_temp = random.uniform(25.0, 32.0)
            rain_chance = random.randint(50, 100)
        else:
            base_temp = random.uniform(15.0, 30.0)
            rain_chance = random.randint(0, 40)
            
        alerts = []
        
        # Heavy Rainfall Alert
        if rain_chance > 80:
            alerts.append({
                "type": "Heavy Rainfall",
                "severity": "red" if rain_chance > 90 else "yellow",
                "icon": "cloud-rain",
                "message": "heavy_rain_warning",
                "action": "protect_crops_drainage"
            })
            
        # Flood Risk (in Monsoon with very high rain chance)
        if rain_chance > 92 and month in [7, 8, 9]:
            alerts.append({
                "type": "Flood Risk",
                "severity": "red",
                "icon": "droplets",
                "message": "flood_warning",
                "action": "move_livestock_drainage"
            })
            
        # Heatwave Alert
        if base_temp > 40:
            alerts.append({
                "type": "Heatwave",
                "severity": "red" if base_temp > 43 else "yellow",
                "icon": "sun",
                "message": "heatwave_warning",
                "action": "increase_irrigation_shade"
            })
            
        # Drought Risk (Low rain for a long time)
        # For demo, if it's summer and rain chance is very low
        if rain_chance < 5 and month in [3, 4, 5]:
            alerts.append({
                "type": "Drought Risk",
                "severity": "yellow",
                "icon": "thermometer-sun",
                "message": "drought_warning",
                "action": "conserve_water_mulching"
            })

        # If no disasters, maybe one low-level info alert or empty list
        if not alerts:
            # Random chance to show a green "Safe" alert for demo
            if random.random() > 0.5:
                alerts.append({
                    "type": "Optimal Conditions",
                    "severity": "green",
                    "icon": "check-circle",
                    "message": "optimal_weather",
                    "action": "proceed_with_activities"
                })

        return Response(alerts, status=status.HTTP_200_OK)
