"""
CropCare AI - Production ML Inference Model Loader
--------------------------------------------------
Demonstrates how production neural networks (PyTorch / TensorFlow / ONNX / TFLite)
integrate directly into the BaseInferenceEngine interface without altering the API or Frontend.
"""

import os
import io
from typing import Dict, Any, Optional
from PIL import Image

try:
    import torch
    import torchvision.transforms as transforms
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from app.ai.base import BaseInferenceEngine

class ProductionVisionEngine(BaseInferenceEngine):
    """
    Production PyTorch / MobileNetV3 classifier trained on PlantVillage
    (38 classes across 14 crop species).
    """

    def __init__(self, model_weights_path: Optional[str] = None):
        self.model_version = "CropCare-MobileNetV3-PlantVillage-v2.1"
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

        if TORCH_AVAILABLE and model_weights_path and os.path.exists(model_weights_path):
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = torch.load(model_weights_path, map_location=self.device)
            self.model.eval()
            print(f"Loaded production model from {model_weights_path} onto {self.device}")
        else:
            self.model = None

        if TORCH_AVAILABLE:
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])

    def predict(
        self,
        image_bytes: bytes,
        crop_name: str,
        filename: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Runs real PyTorch inference if weights are loaded, otherwise
        falls back gracefully to deterministic demo heuristics.
        """
        if self.model and TORCH_AVAILABLE:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            tensor = self.transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                logits = self.model(tensor)
                probs = torch.nn.functional.softmax(logits, dim=1)[0]
                conf, pred_idx = torch.max(probs, dim=0)

            class_name = self.classes[pred_idx.item()]
            predicted_disease = class_name.replace("___", " ").replace("_", " ")

            confidence = float(conf.item())
            severity = "High" if "Blight" in class_name or "Curl" in class_name else ("Low" if "healthy" in class_name else "Medium")
            is_uncertain = confidence < 0.70

            return {
                "crop": crop_name,
                "predicted_disease": predicted_disease,
                "confidence": round(confidence, 3),
                "severity": severity,
                "is_uncertain": is_uncertain,
                "model_version": self.model_version,
                "raw_scores": {self.classes[i]: float(probs[i].item()) for i in range(len(self.classes))}
            }
        else:
            from app.ai.demo_engine import DemoInferenceEngine
            fallback = DemoInferenceEngine()
            return fallback.predict(image_bytes, crop_name, filename, context)
