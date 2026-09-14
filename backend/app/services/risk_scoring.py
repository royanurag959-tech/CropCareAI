from typing import Dict, Any, Optional

class CropRiskScoringEngine:
    """
    Configurable Crop Risk Score Engine for CropCare AI.
    Generates an automated composite risk score from 0 to 100 based on:
    - AI disease confidence
    - Disease severity
    - Weather conditions (rainfall, temperature, humidity)
    - Irrigation frequency & soil drainage
    - Crop growth stage vulnerability
    - Symptom duration & affected crop area
    - Disease progression speed
    """

    # Configurable weights (sum = 1.0)
    DEFAULT_WEIGHTS = {
        "severity": 0.30,
        "confidence": 0.15,
        "weather_moisture": 0.20,
        "irrigation_drainage": 0.15,
        "crop_vulnerability": 0.10,
        "spread_area": 0.10
    }

    # Configurable risk category thresholds
    THRESHOLDS = {
        "low": (0, 30),
        "moderate": (31, 60),
        "high": (61, 80),
        "critical": (81, 100)
    }

    @classmethod
    def calculate_risk_score(
        cls,
        severity: str,
        confidence: float,
        weather: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        w = weights or cls.DEFAULT_WEIGHTS
        context = context or {}
        weather = weather or {}

        # 1. Severity sub-score (0-100)
        sev_lower = (severity or "Medium").lower()
        is_healthy = "healthy" in (context.get("predicted_disease") or "").lower() or sev_lower == "none"

        if is_healthy:
            sev_score = 0.0
            conf_score = 0.0
        else:
            if "high" in sev_lower:
                sev_score = 90.0
            elif "low" in sev_lower:
                sev_score = 25.0
            else:
                sev_score = 60.0

            # 2. Confidence sub-score (0-100)
            # Active pathogen confidence amplifies risk
            conf_score = float(confidence) * 100.0 if confidence else 50.0

        # 3. Weather & Moisture sub-score (0-100)
        humidity = weather.get("humidity_pct", 70)
        rain_desc = (weather.get("rainfall_desc") or context.get("rainfall") or "Moderate").lower()
        
        weather_score = 40.0
        if "heavy" in rain_desc or "continuous" in rain_desc:
            weather_score += 35.0
        elif "moderate" in rain_desc:
            weather_score += 15.0
        elif "none" in rain_desc or "dry" in rain_desc:
            weather_score -= 15.0

        if humidity >= 85:
            weather_score += 25.0
        elif humidity >= 75:
            weather_score += 10.0
        elif humidity < 50:
            weather_score -= 10.0

        weather_score = max(5.0, min(100.0, weather_score))

        # 4. Irrigation & Drainage sub-score (0-100)
        irrigation = (context.get("irrigation") or "Every 2-3 days").lower()
        drainage = (context.get("drainage") or "Good").lower()

        irr_score = 45.0
        if "daily" in irrigation or "overhead" in irrigation or "flood" in irrigation:
            irr_score += 25.0
        elif "weekly" in irrigation:
            irr_score -= 10.0

        if "poor" in drainage or "waterlogged" in drainage:
            irr_score += 25.0
        elif "good" in drainage:
            irr_score -= 10.0

        irr_score = max(5.0, min(100.0, irr_score))

        # 5. Crop Stage Vulnerability (0-100)
        stage = (context.get("growth_stage") or "Vegetative").lower()
        stage_score = 50.0
        if "flowering" in stage or "fruiting" in stage or "bulking" in stage:
            stage_score = 85.0  # Crucial yield formation window
        elif "seedling" in stage:
            stage_score = 70.0  # High mortality risk
        elif "harvest" in stage:
            stage_score = 55.0

        # 6. Spread Area & Duration (0-100)
        area = (context.get("affected_area") or "10-30%").lower()
        duration = (context.get("duration") or "4-7 days").lower()

        spread_score = 40.0
        if ">30%" in area or "widespread" in area:
            spread_score += 35.0
        elif "<10%" in area or "isolated" in area:
            spread_score -= 15.0

        if "1-2 weeks" in duration or ">2 weeks" in duration or "chronic" in duration:
            spread_score += 25.0
        elif "<3 days" in duration:
            spread_score -= 10.0

        spread_score = max(5.0, min(100.0, spread_score))

        # Weighted calculation
        total_score = (
            (sev_score * w["severity"]) +
            (conf_score * w["confidence"]) +
            (weather_score * w["weather_moisture"]) +
            (irr_score * w["irrigation_drainage"]) +
            (stage_score * w["crop_vulnerability"]) +
            (spread_score * w["spread_area"])
        )

        final_score = int(round(max(0.0, min(100.0, total_score))))

        # Classify risk category
        if final_score <= cls.THRESHOLDS["low"][1]:
            category = "Low Risk"
            category_hi = "कम जोखिम"
            color = "#16a34a"  # Green
        elif final_score <= cls.THRESHOLDS["moderate"][1]:
            category = "Moderate Risk"
            category_hi = "मध्यम जोखिम"
            color = "#ca8a04"  # Yellow/Amber
        elif final_score <= cls.THRESHOLDS["high"][1]:
            category = "High Risk"
            category_hi = "उच्च जोखिम"
            color = "#ea580c"  # Orange
        else:
            category = "Critical Risk"
            category_hi = "गंभीर / आपातकालीन जोखिम"
            color = "#dc2626"  # Red

        explanation_en = (
            f"Your crop currently has a {category.lower()} level ({final_score}/100) because the detected "
            f"symptoms combined with recent weather and farm conditions may support disease development."
        )
        explanation_hi = (
            f"आपकी फसल में वर्तमान में {category_hi} स्तर ({final_score}/100) है, क्योंकि पत्ती के लक्षण, "
            f"हालिया मौसम और खेत की नमी रोग के तेजी से फैलने के अनुकूल हो सकते हैं।"
        )

        disclaimer = (
            "App-Generated Risk Indicator Notice: This score is an automated composite advisory index "
            "synthesized from visual symptoms, local microclimate, and farmer-reported variables. "
            "It is not a laboratory-certified or official statutory measurement."
        )

        return {
            "score": final_score,
            "category": category,
            "category_hindi": category_hi,
            "color": color,
            "explanation": explanation_en,
            "explanation_hindi": explanation_hi,
            "contributing_breakdown": {
                "severity_score": int(sev_score),
                "confidence_score": int(conf_score),
                "weather_moisture_score": int(weather_score),
                "irrigation_drainage_score": int(irr_score),
                "crop_vulnerability_score": int(stage_score),
                "spread_area_score": int(spread_score)
            },
            "disclaimer": disclaimer
        }
