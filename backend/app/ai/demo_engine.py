from app.ai.base import BaseInferenceEngine
from app.ai.mock_provider import MockInferenceProvider
from app.ai.factory import get_inference_engine

# Backward compatibility alias
DemoInferenceEngine = MockInferenceProvider

# Global inference engine instance driven by factory
inference_engine: BaseInferenceEngine = get_inference_engine()
