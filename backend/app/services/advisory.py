import json
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app.database.models import Disease, Crop

class AdvisoryService:
    """
    Constructs evidence-based agricultural recommendations and time-phased farm treatment plans.
    Strictly enforces chemical safety guardrails, avoiding universal uncalibrated doses and promoting
    label adherence and certified extension compliance.
    """

    @staticmethod
    def get_advisory_for_disease(
        db: Session,
        crop_name: str,
        predicted_disease: str
    ) -> Dict[str, Any]:
        disease = db.query(Disease).join(Crop).filter(
            Crop.name.ilike(f"%{crop_name}%"),
            Disease.name.ilike(f"%{predicted_disease}%")
        ).first()

        if not disease:
            disease = db.query(Disease).filter(
                Disease.name.ilike(f"%{predicted_disease}%")
            ).first()

        if disease:
            return {
                "hindi_name": disease.hindi_name,
                "scientific_name": disease.scientific_name,
                "description": disease.description,
                "symptoms": json.loads(disease.symptoms),
                "possible_causes": json.loads(disease.possible_causes),
                "favorable_conditions": json.loads(disease.favorable_conditions),
                "immediate_actions": json.loads(disease.immediate_actions),
                "general_management": json.loads(disease.general_management),
                "prevention": json.loads(disease.prevention),
                "when_to_contact_expert": disease.when_to_contact_expert,
                "disclaimer": (
                    "Important Agricultural Advisory Notice: These recommendations are protective cultural guidelines. "
                    "Always read and strictly follow the chemical/biological product label registered in your region, "
                    "wear personal protective gear, and consult your local Krishi Vigyan Kendra (KVK)."
                )
            }

        # Fallback
        return {
            "hindi_name": f"{crop_name} रोग",
            "scientific_name": "Unspecified foliar pathogen",
            "description": f"Potential foliar disorder detected on {crop_name}.",
            "symptoms": [
                "Discoloration or spotted lesions on leaf blades",
                "Reduced photosynthetic area",
                "Marginal curling or wilting"
            ],
            "possible_causes": [
                "Excess surface moisture or prolonged humidity",
                "Microclimate imbalance or poor aeration",
                "Substrate or nutritional stress"
            ],
            "favorable_conditions": [
                "Warm humid environments with stagnant air"
            ],
            "immediate_actions": [
                "Isolate or prune visibly affected leaves",
                "Avoid late afternoon overhead watering",
                "Improve canopy aeration and weed spacing"
            ],
            "general_management": [
                "Rotate with non-susceptible crop families",
                "Ensure balanced NPK fertilization"
            ],
            "prevention": [
                "Plant certified disease-tolerant varieties",
                "Sterilize tools between pruning passes"
            ],
            "when_to_contact_expert": "If symptoms exceed 20% foliar coverage or new growth shows dieback.",
            "disclaimer": "Agricultural Advisory Notice: Follow state agricultural university package of practices."
        }

    @staticmethod
    def get_time_phased_action_plan(
        disease_name: str,
        crop_name: str,
        severity: str,
        risk_category: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generates practical time-phased action plan:
        1. What to do today (urgent cultural steps)
        2. What to do in next 3 days (short-term intervention)
        3. What to monitor during next 7 days (weather, re-scan reminder)
        """
        crop_clean = (crop_name or "Crop").title()

        today_en = [
            f"Inspect nearby {crop_clean.lower()} rows to verify if spotting is localized or spreading.",
            "Carefully pluck severely blighted lower leaves and dispose away from field (do not compost).",
            "Halt evening overhead watering immediately to avoid prolonged overnight leaf wetness.",
            "Inspect field drainage furrows to ensure no irrigation water is stagnating around root zones."
        ]

        today_hi = [
            f"आस-पास के {crop_clean} पौधों की तुरंत जांच करें कि लक्षण एक जगह हैं या फैल रहे हैं।",
            "अधिक प्रभावित निचली पत्तियों को सावधानीपूर्वक तोड़कर खेत से दूर नष्ट करें (इन्हें खाद के गड्ढे में न डालें)।",
            "शाम के समय ऊपर से फव्वारा पानी देना तुरंत बंद करें ताकि रातभर पत्तियां गीली न रहें।",
            "खेत की जल निकासी नालियों की जांच करें और जड़ों के पास जमा पानी तुरंत निकालें।"
        ]

        next_3_days_en = [
            "Improve row aeration by clearing weeds and gently thinning excessive suckers or crowded foliage.",
            "Verify soil moisture 2 inches deep before adding water; switch to base furrow or drip irrigation.",
            "If fungal spotting continues, apply an approved bio-control formulation (e.g. Trichoderma or registered bio-fungicide) strictly following container label directions."
        ]

        next_3_days_hi = [
            "पंक्तियों के बीच खरपतवार निकालें ताकि पौधों के बीच हवा और धूप का संचार बेहतर हो सके।",
            "सिंचाई से पहले 2 इंच मिट्टी खोदकर नमी जांचें; केवल जरूरत होने पर ही थाला या टपक विधि से पानी दें।",
            "यदि फफूंद के धब्बे बढ़ते हैं, तो स्थानीय कृषि विभाग द्वारा अनुशंसित जैविक फफूंदनाशी (जैसे ट्राइकोडर्मा) का उत्पाद लेबल के अनुसार ही छिड़काव करें।"
        ]

        next_7_days_en = [
            "Monitor local weather forecast daily for high humidity alerts, cloud cover, or rainfall spikes.",
            "Inspect newly emerged top leaves to ensure new vegetative growth remains healthy and green.",
            "Re-scan your crop in 5–7 days on CropCare AI to evaluate recovery and track disease progression.",
            "If symptoms persist or worsen, schedule a 1-on-1 Agronomist consultation through CropCare AI."
        ]

        next_7_days_hi = [
            "आगामी 7 दिनों के मौसम पूर्वानुमान पर नजर रखें (अधिक उमस या बारिश से रोग बढ़ सकता है)।",
            "पौधों की नई निकलने वाली ऊपरी कोपलों और पत्तियों की जांच करें कि वे हरी और स्वस्थ हैं या नहीं।",
            "5 से 7 दिनों बाद क्रॉपकेयर AI पर दोबारा फोटो खींचकर जांचें ताकि सुधार की प्रगति दर्ज हो सके।",
            "यदि लक्षण ठीक नहीं होते हैं, तो ऐप के माध्यम से तुरंत कृषि विशेषज्ञ से परामर्श बुक करें।"
        ]

        safety_notice_en = (
            "Agricultural Chemical Safety Compliance: Never apply uncalibrated chemical mixtures or universal doses. "
            "Always read and strictly follow the container product label, adhere to Pre-Harvest Intervals (PHI), "
            "wear protective gear, and consult your local Krishi Vigyan Kendra (KVK) specialist."
        )

        safety_notice_hi = (
            "कृषि रसायन सुरक्षा चेतावनी: किसी भी दवा का अंधाधुंध या बिना माप-तौल के छिड़काव न करें। "
            "हमेशा उत्पाद के डिब्बे पर दिए गए निर्देशों और प्रतीक्षा अवधि (PHI) का कड़ाई से पालन करें, "
            "सुरक्षात्मक दस्ताने-मास्क पहनें और नजदीकी कृषि विज्ञान केंद्र से सलाह लें।"
        )

        return {
            "today": today_en,
            "today_hindi": today_hi,
            "next_3_days": next_3_days_en,
            "next_3_days_hindi": next_3_days_hi,
            "next_7_days": next_7_days_en,
            "next_7_days_hindi": next_7_days_hi,
            "rescan_recommended_days": 5,
            "chemical_safety_notice": safety_notice_en,
            "chemical_safety_notice_hindi": safety_notice_hi
        }
