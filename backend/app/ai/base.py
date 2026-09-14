from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseInferenceEngine(ABC):
    """
    Abstract interface for CropCare AI vision inference.
    Production implementations (e.g. PyTorch, TensorFlow Lite, ONNX, or Cloud Vision)
    must implement this interface to remain drop-in compatible.
    """

    @abstractmethod
    def validate_image(self, image_bytes: bytes, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate image data before running inference.
        Returns dict with:
            - is_valid: bool
            - error_message: Optional[str]
            - width: Optional[int]
            - height: Optional[int]
            - format: Optional[str]
        """
        pass

    @abstractmethod
    def predict(
        self,
        image_bytes: bytes,
        crop_name: str,
        filename: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute disease classification inference.

        Returns dict with:
            - crop: str
            - crop_hindi: str
            - predicted_disease: str
            - hindi_name: str
            - scientific_name: Optional[str]
            - confidence: float (0.0 to 1.0)
            - confidence_percentage: int (0 to 100)
            - confidence_level: str ('high', 'medium', 'low')
            - confidence_level_label: str
            - confidence_level_label_hindi: str
            - severity: str ('Low', 'Medium', 'High')
            - is_uncertain: bool
            - uncertainty_message: Optional[str]
            - short_explanation: str
            - short_explanation_hindi: str
            - model_version: str
            - provider_name: str
            - raw_scores: Dict[str, float]
        """
        pass
