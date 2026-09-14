from typing import Dict, Type, Optional
from app.ai.base import BaseInferenceEngine
from app.ai.mock_provider import MockInferenceProvider
from app.ai.real_provider import RealModelInferenceProvider
from app.core.config import settings

_PROVIDERS: Dict[str, Type[BaseInferenceEngine]] = {
    "mock": MockInferenceProvider,
    "demo": MockInferenceProvider,
    "real": RealModelInferenceProvider,
    "production": RealModelInferenceProvider,
}

_SINGLETONS: Dict[str, BaseInferenceEngine] = {}

def register_provider(name: str, provider_cls: Type[BaseInferenceEngine]) -> None:
    """
    Allows registering custom AI vision providers at runtime (e.g., ONNX, TFLite, Cloud Vision).
    """
    _PROVIDERS[name.lower()] = provider_cls

def get_inference_engine(provider_name: Optional[str] = None) -> BaseInferenceEngine:
    """
    Factory function returning the configured AI vision inference engine.
    Driven by settings.AI_PROVIDER ('mock' or 'real') or explicit override.
    """
    key = (provider_name or getattr(settings, "AI_PROVIDER", "mock")).lower().strip()

    if key not in _PROVIDERS:
        key = "mock"

    if key not in _SINGLETONS:
        provider_cls = _PROVIDERS[key]
        if key in ["real", "production"]:
            weights_path = getattr(settings, "MODEL_WEIGHTS_PATH", None)
            _SINGLETONS[key] = provider_cls(model_weights_path=weights_path)
        else:
            _SINGLETONS[key] = provider_cls()

    return _SINGLETONS[key]
