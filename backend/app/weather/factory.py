from typing import Dict, Type, Optional
from app.weather.base import BaseWeatherProvider
from app.weather.mock_provider import MockWeatherProvider
from app.weather.real_provider import RealWeatherProvider
from app.core.config import settings

_WEATHER_PROVIDERS: Dict[str, Type[BaseWeatherProvider]] = {
    "mock": MockWeatherProvider,
    "demo": MockWeatherProvider,
    "real": RealWeatherProvider,
    "production": RealWeatherProvider
}

_SINGLETONS: Dict[str, BaseWeatherProvider] = {}

def get_weather_provider(provider_name: Optional[str] = None) -> BaseWeatherProvider:
    """
    Factory function returning the configured Weather Provider.
    Driven by settings.WEATHER_PROVIDER or explicit parameter.
    """
    key = (provider_name or getattr(settings, "WEATHER_PROVIDER", "mock")).lower().strip()
    if key not in _WEATHER_PROVIDERS:
        key = "mock"

    if key not in _SINGLETONS:
        _SINGLETONS[key] = _WEATHER_PROVIDERS[key]()

    return _SINGLETONS[key]
