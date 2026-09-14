from typing import Dict, Any, Optional
from app.weather.base import BaseWeatherProvider

class MockWeatherProvider(BaseWeatherProvider):
    """
    Mock/Simulated Weather Provider for hackathon evaluations and offline testing.
    Provides realistic Indian agricultural microclimate models.
    """

    def __init__(self):
        self.provider_name = "MockWeatherProvider (Regional Microclimate)"

    def get_weather(self, location: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        loc_clean = (location or "Pune District").strip().title()

        # Regional agricultural weather presets
        regional_presets = {
            "Pune": {
                "temp": 26.5,
                "humidity": 82,
                "rain_mm": 18.0,
                "rain_desc": "Moderate",
                "condition": "Warm & Humid Overcast",
                "condition_hi": "गर्म व उमस भरा बादल",
                "wind_kmh": 12.0,
                "risk": "High"
            },
            "Karnal": {
                "temp": 24.0,
                "humidity": 78,
                "rain_mm": 12.0,
                "rain_desc": "Light Showers",
                "condition": "Cloudy & Damp",
                "condition_hi": "बादल व ठंडी नमी",
                "wind_kmh": 14.5,
                "risk": "Medium"
            },
            "Varanasi": {
                "temp": 29.0,
                "humidity": 85,
                "rain_mm": 24.0,
                "rain_desc": "Heavy",
                "condition": "Heavy Rain & Humid",
                "condition_hi": "भारी बारिश व अत्यधिक उमस",
                "wind_kmh": 16.0,
                "risk": "High"
            },
            "Mandya": {
                "temp": 27.0,
                "humidity": 74,
                "rain_mm": 6.0,
                "rain_desc": "Light",
                "condition": "Partly Cloudy",
                "condition_hi": "आंशिक बादल",
                "wind_kmh": 10.0,
                "risk": "Medium"
            },
            "Indore": {
                "temp": 28.5,
                "humidity": 68,
                "rain_mm": 0.0,
                "rain_desc": "None",
                "condition": "Sunny & Dry",
                "condition_hi": "धूप व शुष्क",
                "wind_kmh": 9.0,
                "risk": "Low"
            },
            "Shimla": {
                "temp": 18.0,
                "humidity": 88,
                "rain_mm": 15.0,
                "rain_desc": "Moderate",
                "condition": "Cool Mist & Rain",
                "condition_hi": "ठंडा कोहरा व फुहारें",
                "wind_kmh": 18.0,
                "risk": "High"
            }
        }

        # Find matching preset by partial match
        matched_preset = None
        for k, v in regional_presets.items():
            if k.lower() in loc_clean.lower():
                matched_preset = v
                break

        if not matched_preset:
            matched_preset = {
                "temp": 26.0,
                "humidity": 80,
                "rain_mm": 14.0,
                "rain_desc": "Moderate",
                "condition": "Humid & Overcast",
                "condition_hi": "उमस भरा व बादल",
                "wind_kmh": 12.0,
                "risk": "Medium"
            }

        # Override or refine with farmer-provided rainfall if specified in context
        farmer_rain = context.get("rainfall")
        if farmer_rain:
            if farmer_rain in ["Heavy", "Continuous"]:
                matched_preset["rain_desc"] = "Heavy / Continuous"
                matched_preset["rain_mm"] = max(matched_preset["rain_mm"], 35.0)
                matched_preset["humidity"] = max(matched_preset["humidity"], 88)
                matched_preset["risk"] = "High"
            elif farmer_rain in ["None", "Dry"]:
                matched_preset["rain_desc"] = "None / Dry"
                matched_preset["rain_mm"] = 0.0
                matched_preset["humidity"] = min(matched_preset["humidity"], 55)
            elif farmer_rain in ["Light"]:
                matched_preset["rain_desc"] = "Light Showers"
                matched_preset["rain_mm"] = 5.0

        return {
            "location": loc_clean,
            "temperature_c": matched_preset["temp"],
            "humidity_pct": matched_preset["humidity"],
            "rainfall_mm": matched_preset["rain_mm"],
            "rainfall_desc": matched_preset["rain_desc"],
            "condition": matched_preset["condition"],
            "condition_hindi": matched_preset["condition_hi"],
            "wind_kmh": matched_preset["wind_kmh"],
            "microclimate_risk": matched_preset["risk"],
            "provider_name": self.provider_name
        }
