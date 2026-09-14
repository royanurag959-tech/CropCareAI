import os
import io
from typing import Dict, Any, Optional
from PIL import Image
from app.ai.base import BaseInferenceEngine
from app.ai.mock_provider import MockInferenceProvider

try:
    import torch
    import torchvision.transforms as transforms
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

class RealModelInferenceProvider(BaseInferenceEngine):
    """
    Production Deep Learning Provider for CropCare AI.
    Loads trained PyTorch / ONNX / TorchScript models (e.g. MobileNetV3 / EfficientNet on PlantVillage).
    If model weights are not configured or torch is not installed in the environment,
    it automatically falls back to MockInferenceProvider with a clear metadata audit trail.
    """

    def __init__(self, model_weights_path: Optional[str] = None):
        self.provider_name = "RealModelInferenceProvider"
        self.model_version = "CropCare-MobileNetV3-PlantVillage-v2.1"
        self.fallback_engine = MockInferenceProvider()
        self.classes = [
            "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
            "Corn___Cercospora_leaf_spot", "Corn___Common_rust", "Corn___Northern_Leaf_Blight", "Corn___healthy",
            "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
            "Rice___Brown_Spot", "Rice___Leaf_Blast", "Rice___Neck_Blast", "Rice___healthy",
            "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
            "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites",
            "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus",
            "Tomato___healthy"
        ]

        self.model = None
        self.device = None
        self.transform = None

        if TORCH_AVAILABLE:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            if model_weights_path and os.path.exists(model_weights_path):
                try:
                    self.model = torch.load(model_weights_path, map_location=self.device)
                    self.model.eval()
                    print(f"Loaded production neural model from {model_weights_path} on {self.device}")
                except Exception as e:
                    print(f"Warning: Failed to load model weights from {model_weights_path}: {e}")
                    self.model = None

            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])

    def validate_image(self, image_bytes: bytes, filename: Optional[str] = None) -> Dict[str, Any]:
        return self.fallback_engine.validate_image(image_bytes, filename)

    def predict(
        self,
        image_bytes: bytes,
        crop_name: str,
        filename: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        val_result = self.validate_image(image_bytes, filename)
        if not val_result["is_valid"]:
            return self.fallback_engine.predict(image_bytes, crop_name, filename, context)

        if self.model and TORCH_AVAILABLE:
            try:
                image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                tensor = self.transform(image).unsqueeze(0).to(self.device)

                with torch.no_grad():
                    logits = self.model(tensor)
                    probs = torch.nn.functional.softmax(logits, dim=1)[0]
                    conf_tensor, pred_idx = torch.max(probs, dim=0)

                conf = float(conf_tensor.item())
                class_name = self.classes[pred_idx.item()]
                predicted_disease = class_name.replace("___", " ").replace("_", " ")

                severity = "High" if ("Blight" in class_name or "Curl" in class_name or "Blast" in class_name) else ("Low" if "healthy" in class_name else "Medium")
                conf_pct = int(round(conf * 100))

                if conf >= 0.90:
                    conf_level = "high"
                    conf_label = "High Confidence"
                    conf_label_hi = "उच्च विश्वास (सटीक)"
                    is_uncertain = False
                    uncertainty_msg = None
                elif conf >= 0.60:
                    conf_level = "medium"
                    conf_label = "Medium Confidence"
                    conf_label_hi = "मध्यम विश्वास"
                    is_uncertain = False
                    uncertainty_msg = None
                else:
                    conf_level = "low"
                    conf_label = "Low Confidence"
                    conf_label_hi = "कम विश्वास (अपुष्ट)"
                    is_uncertain = True
                    uncertainty_msg = "Low confidence prediction. The AI cannot confirm this diagnosis. Please upload a clearer photo or consult an expert."

                return {
                    "crop": crop_name,
                    "crop_hindi": crop_name,
                    "predicted_disease": predicted_disease,
                    "hindi_name": f"{crop_name} रोग",
                    "scientific_name": class_name,
                    "confidence": round(conf, 3),
                    "confidence_percentage": conf_pct,
                    "confidence_level": conf_level,
                    "confidence_level_label": conf_label,
                    "confidence_level_label_hindi": conf_label_hi,
                    "severity": severity,
                    "is_uncertain": is_uncertain,
                    "uncertainty_message": uncertainty_msg,
                    "short_explanation": f"Deep learning pattern match identified {predicted_disease} with {conf_pct}% confidence.",
                    "short_explanation_hindi": f"डीप लर्निंग मॉडल द्वारा {predicted_disease} की पहचान {conf_pct}% विश्वास के साथ की गई।",
                    "model_version": self.model_version,
                    "provider_name": self.provider_name,
                    "raw_scores": {self.classes[i]: float(probs[i].item()) for i in range(len(self.classes))}
                }
            except Exception as e:
                print(f"Error during neural inference: {e}. Falling back to mock provider.")

        # Graceful fallback to mock provider with provider indicator
        result = self.fallback_engine.predict(image_bytes, crop_name, filename, context)
        result["provider_name"] = f"{self.provider_name} (Mock Heuristics Fallback)"
        return result
