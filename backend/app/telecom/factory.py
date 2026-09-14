from typing import Dict, Type, Optional
from app.telecom.base import BaseTelecomProvider
from app.telecom.mock_provider import MockTelecomProvider
from app.telecom.real_provider import RealTelecomProvider
from app.core.config import settings

_TELECOM_PROVIDERS: Dict[str, Type[BaseTelecomProvider]] = {
    "mock": MockTelecomProvider,
    "demo": MockTelecomProvider,
    "real": RealTelecomProvider,
    "production": RealTelecomProvider
}

_SINGLETONS: Dict[str, BaseTelecomProvider] = {}

def get_telecom_provider(provider_name: Optional[str] = None) -> BaseTelecomProvider:
    """
    Factory returning configured Telecom Provider.
    Driven by settings.TELECOM_PROVIDER or explicit parameter.
    """
    key = (provider_name or getattr(settings, "TELECOM_PROVIDER", "mock")).lower().strip()
    if key not in _TELECOM_PROVIDERS:
        key = "mock"

    if key not in _SINGLETONS:
        _SINGLETONS[key] = _TELECOM_PROVIDERS[key]()

    return _SINGLETONS[key]
