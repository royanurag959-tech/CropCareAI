from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseWeatherProvider(ABC):
    """
    Abstract base class for Weather Providers in CropCare AI.
    Integrates environmental conditions (temperature, humidity, rainfall, wind)
    into disease risk assessments.
    """

    @abstractmethod
    def get_weather(self, location: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieves weather parameters for a given location / district.
        Returns dict with:
            - location: str
            - temperature_c: float
            - humidity_pct: int
            - rainfall_mm: float
            - rainfall_desc: str ('None', 'Light', 'Moderate', 'Heavy')
            - condition: str ('Sunny', 'Cloudy', 'Humid & Overcast', 'Rainy', 'Foggy')
            - condition_hindi: str
            - wind_kmh: float
            - microclimate_risk: str ('High', 'Medium', 'Low')
            - provider_name: str
        """
        pass
