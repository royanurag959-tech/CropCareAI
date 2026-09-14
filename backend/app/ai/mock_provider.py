import io
from typing import Dict, Any, Optional
from PIL import Image
from app.ai.base import BaseInferenceEngine

class MockInferenceProvider(BaseInferenceEngine):
    """
    Modular Mock AI Vision Inference Provider for CropCare AI.
    Provides realistic, biologically grounded disease diagnostics across 7 major crops,
    supporting offline simulation, edge-case testing, and rapid hackathon evaluation.
    """

    def __init__(self):
        self.provider_name = "MockInferenceProvider"
        self.model_version = "CropCare-Vision-MockEngine-v2.0"

    def validate_image(self, image_bytes: bytes, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Validates uploaded image bytes, header, and dimensions before inference.
        """
        if not image_bytes or len(image_bytes) == 0:
            return {
                "is_valid": False,
                "error_message": "Uploaded image file is empty (0 bytes).",
                "width": 0,
                "height": 0,
                "format": None
            }

        if len(image_bytes) > 10 * 1024 * 1024:
            return {
                "is_valid": False,
                "error_message": "Image exceeds maximum allowed size of 10MB.",
                "width": 0,
                "height": 0,
                "format": None
            }

        try:
            image = Image.open(io.BytesIO(image_bytes))
            width, height = image.size
            img_format = image.format or "UNKNOWN"

            if width < 50 or height < 50:
                return {
                    "is_valid": False,
                    "error_message": f"Image dimensions too small ({width}x{height}px). Minimum 50x50px required for foliar diagnostic feature extraction.",
                    "width": width,
                    "height": height,
                    "format": img_format
                }

            return {
                "is_valid": True,
                "error_message": None,
                "width": width,
                "height": height,
                "format": img_format
            }
        except Exception as e:
            return {
                "is_valid": False,
                "error_message": f"Corrupted or unsupported image file format: {str(e)}",
                "width": 0,
                "height": 0,
                "format": None
            }

    def predict(
        self,
        image_bytes: bytes,
        crop_name: str,
        filename: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        filename_lower = (filename or "").lower()
        crop_clean = crop_name.strip().title()

        crop_hindi_map = {
            "Tomato": "टमाटर",
            "Potato": "आलू",
            "Rice": "धान",
            "Apple": "सेब",
            "Corn": "मक्का",
            "Wheat": "गेहूं",
            "Cotton": "कपास"
        }
        crop_hindi = crop_hindi_map.get(crop_clean, f"{crop_clean}")

        # 1. Pre-validation
        val_result = self.validate_image(image_bytes, filename)
        if not val_result["is_valid"]:
            return {
                "crop": crop_clean,
                "crop_hindi": crop_hindi,
                "predicted_disease": "Unprocessable / Invalid Image",
                "hindi_name": "अमान्य या अस्पष्ट फोटो",
                "scientific_name": None,
                "confidence": 0.20,
                "confidence_percentage": 20,
                "confidence_level": "low",
                "confidence_level_label": "Low Confidence",
                "confidence_level_label_hindi": "कम विश्वास (अपुष्ट)",
                "severity": "Low",
                "is_uncertain": True,
                "uncertainty_message": f"Image validation failed: {val_result['error_message']}. Please upload a clear leaf photo.",
                "short_explanation": "We could not process this file. Please take a clear, well-lit photo focusing directly on the infected crop leaf.",
                "short_explanation_hindi": "फोटो प्रोसेस नहीं हो सकी। कृपया संक्रमित पत्ती पर केंद्रित साफ और धूप में ली गई फोटो अपलोड करें।",
                "model_version": self.model_version,
                "provider_name": self.provider_name,
                "raw_scores": {"invalid_image": 1.0}
            }

        # 2. Trigger low confidence flow for blurry or unclear test vectors
        if "unclear" in filename_lower or "blur" in filename_lower:
            conf = 0.45
            return {
                "crop": crop_clean,
                "crop_hindi": crop_hindi,
                "predicted_disease": f"Inconclusive {crop_clean} Condition",
                "hindi_name": f"{crop_hindi} की अनिश्चित स्थिति",
                "scientific_name": "Inconclusive foliar symptoms",
                "confidence": conf,
                "confidence_percentage": int(conf * 100),
                "confidence_level": "low",
                "confidence_level_label": "Low Confidence",
                "confidence_level_label_hindi": "कम विश्वास (अपुष्ट)",
                "severity": "Medium",
                "is_uncertain": True,
                "uncertainty_message": "We could not confidently identify the disease due to image clarity or lighting. Please upload a clearer photo or consult an agricultural expert.",
                "short_explanation": "The image appears blurry or low contrast. The AI cannot confirm the diagnosis with certainty. A clearer, closer picture will provide an accurate result.",
                "short_explanation_hindi": "फोटो स्पष्ट न होने या प्रकाश की कमी के कारण रोग की पक्की पुष्टि नहीं की जा सकती। कृपया धूप में साफ व नजदीक से फोटो लें या विशेषज्ञ से परामर्श लें।",
                "model_version": self.model_version,
                "provider_name": self.provider_name,
                "raw_scores": {"inconclusive": 0.55, "other": 0.45}
            }

        # 3. Check for healthy leaf test cases
        if "healthy" in filename_lower:
            conf = 0.96
            return {
                "crop": crop_clean,
                "crop_hindi": crop_hindi,
                "predicted_disease": f"Healthy {crop_clean}",
                "hindi_name": f"स्वस्थ {crop_hindi}",
                "scientific_name": "No pathogen detected",
                "confidence": conf,
                "confidence_percentage": int(conf * 100),
                "confidence_level": "high",
                "confidence_level_label": "High Confidence",
                "confidence_level_label_hindi": "उच्च विश्वास (सटीक)",
                "severity": "Low",
                "is_uncertain": False,
                "uncertainty_message": None,
                "short_explanation": f"Your {crop_clean.lower()} leaf shows no visible signs of fungal or viral infection. Maintain current irrigation and monitoring.",
                "short_explanation_hindi": f"आपकी {crop_hindi} की पत्ती पूरी तरह स्वस्थ दिख रही है। फफूंद या कीट के कोई लक्षण नहीं हैं। नियमित देखभाल जारी रखें।",
                "model_version": self.model_version,
                "provider_name": self.provider_name,
                "raw_scores": {f"Healthy {crop_clean}": 0.96, "Other": 0.04}
            }

        # 4. Standard Crop Disease Library
        catalog = {
            "Tomato": {
                "disease": "Tomato Leaf Blight",
                "hindi_name": "टमाटर पत्ता झुलसा (अर्ली ब्लाइट)",
                "scientific_name": "Alternaria solani",
                "confidence": 0.94,
                "severity": "Medium",
                "short_en": "Fungal infection triggered by prolonged leaf wetness and high humidity. Spreads upwards from lower canopy leaves.",
                "short_hi": "पत्तियों पर लगातार नमी और उमस के कारण फफूंद का संक्रमण। यह निचली पत्तियों से शुरू होकर ऊपर की ओर फैलता है।",
                "scores": {"Tomato Leaf Blight": 0.94, "Tomato Leaf Curl": 0.04, "Healthy": 0.02}
            },
            "Potato": {
                "disease": "Potato Early Blight",
                "hindi_name": "आलू अगेती झुलसा",
                "scientific_name": "Alternaria solani",
                "confidence": 0.88,
                "severity": "Medium",
                "short_en": "Target-board circular brown lesions on older leaves, often exacerbated by fluctuating wet and dry soil conditions.",
                "short_hi": "पुरानी पत्तियों पर छल्लेदार भूरे धब्बे बनते हैं। मिट्टी में नमी के बार-बार उतार-चढ़ाव से रोग बढ़ता है।",
                "scores": {"Potato Early Blight": 0.88, "Potato Late Blight": 0.09, "Healthy": 0.03}
            },
            "Rice": {
                "disease": "Rice Blast",
                "hindi_name": "धान झोंका रोग (ब्लास्ट)",
                "scientific_name": "Magnaporthe oryzae",
                "confidence": 0.91,
                "severity": "High",
                "short_en": "Spindle-shaped necrotic lesions with grey centers. Thrives in cloudy, humid weather with heavy nitrogen fertilizer use.",
                "short_hi": "पत्तियों पर नाव या आंख के आकार के धब्बे बनते हैं। अधिक यूरिया के प्रयोग और लगातार बादलों वाले मौसम से यह तेजी से फैलता है।",
                "scores": {"Rice Blast": 0.91, "Rice Brown Spot": 0.07, "Healthy": 0.02}
            },
            "Apple": {
                "disease": "Apple Scab",
                "hindi_name": "सेब का स्कैब रोग",
                "scientific_name": "Venturia inaequalis",
                "confidence": 0.89,
                "severity": "Medium",
                "short_en": "Olive-green velvety fungal spots on leaf surfaces resulting from prolonged leaf wetness during temperate spring rains.",
                "short_hi": "लगातार बारिश और पत्तों पर पानी ठहरने से जैतूनी-हरे रंग के मखमली धब्बे बनते हैं जो पत्तियों को कमजोर करते हैं।",
                "scores": {"Apple Scab": 0.89, "Apple Rust": 0.08, "Healthy": 0.03}
            },
            "Corn": {
                "disease": "Corn Leaf Spot (Northern Corn Leaf Blight)",
                "hindi_name": "मक्का पत्ता धब्बा (उत्तरी लीफ ब्लाइट)",
                "scientific_name": "Exserohilum turcicum",
                "confidence": 0.87,
                "severity": "Medium",
                "short_en": "Elongated grayish-green elliptical lesions that turn tan. Favored by warm, damp microclimates and heavy morning dews.",
                "short_hi": "पत्तियों पर लंबे भूरे-धूसर रंग के धब्बे बनते हैं। सुबह की ओस और गर्म-नम मौसम में इसका प्रकोप अधिक होता है।",
                "scores": {"Corn Leaf Spot": 0.87, "Common Rust": 0.09, "Healthy": 0.04}
            },
            "Wheat": {
                "disease": "Wheat Stripe Rust (Yellow Rust)",
                "hindi_name": "गेहूं का पीला रतुआ (स्ट्राइप रस्ट)",
                "scientific_name": "Puccinia striiformis",
                "confidence": 0.92,
                "severity": "High",
                "short_en": "Linear stripes of yellow-orange powdery pustules along leaf veins, carried by cool damp winds in northern plains.",
                "short_hi": "पत्तियों की नसों के समानांतर पीले रंग की धारियों में चूर्ण जैसे दाने बनते हैं, जो ठंडी हवा और नमी से फैलते हैं।",
                "scores": {"Wheat Stripe Rust": 0.92, "Spot Blotch": 0.06, "Healthy": 0.02}
            },
            "Cotton": {
                "disease": "Cotton Leaf Curl Virus (CLCuV)",
                "hindi_name": "कपास का पर्ण कुंचन विषाणु (लीफ कर्ल)",
                "scientific_name": "Begomovirus / CLCuV",
                "confidence": 0.93,
                "severity": "High",
                "short_en": "Viral upward leaf curling and vein thickening transmitted rapidly by phloem-feeding whitefly swarms in warm dry periods.",
                "short_hi": "सफेद मक्खी द्वारा फैलाया जाने वाला वायरस, जिससे पत्तियां ऊपर की ओर मुड़ जाती हैं और पौधे की बढ़वार रुक जाती है।",
                "scores": {"Cotton Leaf Curl": 0.93, "Bacterial Blight": 0.05, "Healthy": 0.02}
            }
        }

        entry = catalog.get(crop_clean, {
            "disease": f"{crop_clean} Foliar Blight",
            "hindi_name": f"{crop_hindi} पत्ता झुलसा",
            "scientific_name": "Phytopathogenic complex",
            "confidence": 0.85,
            "severity": "Medium",
            "short_en": f"Foliar necrotic spotting detected on {crop_clean}. Frequently related to leaf wetness and microclimate humidity.",
            "short_hi": f"{crop_hindi} की पत्तियों पर धब्बे दिखे हैं, जो अधिक नमी और खराब वायु संचार के कारण हो सकते हैं।",
            "scores": {f"{crop_clean} Foliar Blight": 0.85, "Other": 0.15}
        })

        conf = entry["confidence"]
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
            "crop": crop_clean,
            "crop_hindi": crop_hindi,
            "predicted_disease": entry["disease"],
            "hindi_name": entry["hindi_name"],
            "scientific_name": entry["scientific_name"],
            "confidence": conf,
            "confidence_percentage": conf_pct,
            "confidence_level": conf_level,
            "confidence_level_label": conf_label,
            "confidence_level_label_hindi": conf_label_hi,
            "severity": entry["severity"],
            "is_uncertain": is_uncertain,
            "uncertainty_message": uncertainty_msg,
            "short_explanation": entry["short_en"],
            "short_explanation_hindi": entry["short_hi"],
            "model_version": self.model_version,
            "provider_name": self.provider_name,
            "raw_scores": entry["scores"]
        }
