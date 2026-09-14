from typing import Dict, Any, List, Optional

class ExpertEscalationEvaluator:
    """
    Evaluates whether an agricultural case warrants certified agronomist review.
    Automatically triggers escalation recommendations under 5 distinct criteria:
    1. Low AI Confidence (< 60%)
    2. High Disease Severity
    3. High or Critical Crop Risk Score (>= 61)
    4. Worsening Disease Progression Trend ('Increasing' or 'Rapidly Increasing')
    5. Direct Farmer Manual Request
    """

    @classmethod
    def evaluate(
        cls,
        confidence: float,
        severity: str,
        risk_score: int,
        trend: Optional[str] = None,
        manual_request: bool = False
    ) -> Dict[str, Any]:
        reasons_en: List[str] = []
        reasons_hi: List[str] = []

        if confidence < 0.60:
            reasons_en.append("AI confidence is low (<60%) — visual diagnosis is uncertain")
            reasons_hi.append("AI विश्वास कम है (<60%) — फोटो से पक्की पुष्टि नहीं हो सकी")

        if (severity or "").lower() == "high":
            reasons_en.append("Disease severity level is High Alert — rapid foliar collapse risk")
            reasons_hi.append("रोग की गंभीरता उच्च (High Alert) है — फसल को गंभीर नुकसान का खतरा है")

        if risk_score >= 61:
            reasons_en.append(f"Crop Risk Score is elevated ({risk_score}/100) due to compounding conditions")
            reasons_hi.append(f"क्रॉप रिस्क स्कोर अधिक ({risk_score}/100) है — मौसम व खेत की स्थिति रोग के अनुकूल है")

        if trend in ["Increasing", "Rapidly Increasing"]:
            reasons_en.append(f"Disease progression trend is worsening ({trend}) over successive scans")
            reasons_hi.append(f"निगरानी टाइमलाइन में रोग का फैलाव बढ़ रहा है ({trend})")

        if manual_request:
            reasons_en.append("Farmer explicitly requested 1-on-1 agronomy review")
            reasons_hi.append("किसान द्वारा सीधे विशेषज्ञ परामर्श का अनुरोध किया गया")

        suggest_expert = len(reasons_en) > 0

        if suggest_expert:
            primary_en = (
                "⚠️ Certified Agronomist Review Recommended: Based on your crop's current condition "
                f"({', '.join(reasons_en[:2])}), we advise connecting with a state agricultural specialist."
            )
            primary_hi = (
                "⚠️ विशेषज्ञ परामर्श की अनुशंसा: आपकी फसल की मौजूदा स्थिति "
                f"({', '.join(reasons_hi[:2])}) को देखते हुए कृषि विशेषज्ञ से सलाह लेना उचित होगा।"
            )
        else:
            primary_en = "Standard self-management: Follow the step-by-step cultural action plan below."
            primary_hi = "सामान्य देखभाल: नीचे दी गई चरणबद्ध कार्ययोजना का पालन करें।"

        return {
            "suggest_expert": suggest_expert,
            "trigger_count": len(reasons_en),
            "reasons": reasons_en,
            "reasons_hindi": reasons_hi,
            "primary_prompt": primary_en,
            "primary_prompt_hindi": primary_hi
        }

    @classmethod
    def compile_case_dossier(
        cls,
        crop: str,
        predicted_disease: str,
        confidence: float,
        confidence_level: str,
        risk_score: int,
        risk_category: str,
        image_url: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        weather: Optional[Dict[str, Any]] = None,
        farmer_question: Optional[str] = None,
        farmer_name: Optional[str] = None,
        farmer_phone: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Assembles a comprehensive case dossier snapshot for agronomist triage.
        """
        context = context or {}
        weather = weather or {}

        return {
            "crop": crop,
            "predicted_disease": predicted_disease,
            "confidence_percentage": int(round(confidence * 100)),
            "confidence_level": confidence_level,
            "risk_score": risk_score,
            "risk_category": risk_category,
            "image_url": image_url,
            "farmer_info": {
                "name": farmer_name or "Farmer",
                "phone": farmer_phone or "Unspecified"
            },
            "farmer_answers": {
                "growth_stage": context.get("growth_stage", "Vegetative"),
                "crop_age": context.get("crop_age", "Not specified"),
                "symptom_duration": context.get("duration", "3-5 days"),
                "rainfall_reported": context.get("rainfall", "Moderate"),
                "irrigation_frequency": context.get("irrigation", "Every 2-3 days"),
                "soil_drainage": context.get("drainage", "Good"),
                "affected_area": context.get("affected_area", "10-30%"),
                "location": context.get("location", "Pune District")
            },
            "weather_conditions": {
                "temperature_c": weather.get("temperature_c", 26.0),
                "humidity_pct": weather.get("humidity_pct", 80),
                "rainfall_desc": weather.get("rainfall_desc", "Moderate"),
                "condition": weather.get("condition", "Humid Overcast")
            },
            "farmer_question": farmer_question or "What immediate steps should I take to prevent this from spreading across my plot?"
        }
