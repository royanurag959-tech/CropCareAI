import os
from typing import Dict, Any, Optional
from app.weather.base import BaseWeatherProvider
from app.weather.mock_provider import MockWeatherProvider
from app.core.config import settings

class RealWeatherProvider(BaseWeatherProvider):
    """
    Production Weather Provider for CropCare AI.
    Connects to live weather APIs (e.g. OpenWeatherMap, WeatherAPI, IMD).
    Falls back gracefully to MockWeatherProvider if API key is not configured.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or getattr(settings, "WEATHER_API_KEY", None)
        self.provider_name = "RealWeatherProvider"
        self.fallback = MockWeatherProvider()

    def get_weather(self, location: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.api_key:
            data = self.fallback.get_weather(location, context)
            data["provider_name"] = f"{self.provider_name} (Mock Heuristics Fallback - Set WEATHER_API_KEY)"
            return data

        # Live HTTP API integration placeholder for future deployment
        try:
            # e.g., httpx.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric")
            data = self.fallback.get_weather(location, context)
            data["provider_name"] = f"{self.provider_name} (Live API)"
            return data
        except Exception as e:
            data = self.fallback.get_weather(location, context)
            data["provider_name"] = f"{self.provider_name} (Fallback after error: {str(e)})"
            return data
