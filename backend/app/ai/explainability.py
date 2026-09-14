from typing import Dict, Any, List, Optional

class ExplainableAIEngine:
    """
    Synthesizes causal root-factor explanations ('Why did this happen?')
    by correlating disease epidemiology with field-level context and weather variables.
    Adheres strictly to cautious agricultural standards:
    - Never declares a single cause as absolute fact based only on an image.
    - Categorizes factors into Environmental, Farming-Related, and Biological Vectors.
    - Uses cautious phrasing: 'Possible reasons include...', 'This may be related to...'.
    """

    @staticmethod
    def generate_explanation(
        disease_name: str,
        crop_name: str,
        context: Optional[Dict[str, Any]] = None,
        weather: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        context = context or {}
        weather = weather or {}

        growth_stage = context.get("growth_stage", "Vegetative")
        crop_age = context.get("crop_age", "Not specified")
        rainfall = context.get("rainfall", weather.get("rainfall_desc", "Moderate"))
        irrigation = context.get("irrigation", "Every 2-3 days")
        drainage = context.get("drainage", "Good")
        duration = context.get("duration", "4-7 days")
        affected_area = context.get("affected_area", "10-30%")
        location = context.get("location", weather.get("location", "Pune District"))

        temp_c = weather.get("temperature_c", 26.0)
        humidity_pct = weather.get("humidity_pct", 80)

        env_factors: List[Dict[str, Any]] = []
        farm_factors: List[Dict[str, Any]] = []
        bio_factors: List[Dict[str, Any]] = []

        # 1. Environmental Factors
        if "blight" in disease_name.lower() or "spot" in disease_name.lower() or "scab" in disease_name.lower() or "blast" in disease_name.lower():
            env_factors.append({
                "factor": "High Ambient Humidity & Prolonged Foliar Moisture",
                "factor_hi": "हवा में अधिक नमी और पत्तियों पर ठहरा हुआ पानी",
                "impact_level": "High",
                "explanation": "Fungal zoospores require free water droplets on leaf surfaces for several continuous hours to germinate and penetrate plant stomata.",
                "explanation_hi": "फफूंद के बीजाणुओं को अंकुरित होने के लिए पत्तियों पर कुछ घंटों तक लगातार पानी की बूंदों की आवश्यकता होती है।"
            })
            if rainfall in ["Heavy", "Continuous", "Heavy / Continuous"]:
                env_factors.append({
                    "factor": "Recent Heavy Rainfall Episodes",
                    "factor_hi": "हाल ही में हुई भारी या लगातार बारिश",
                    "impact_level": "High",
                    "explanation": "Rainstorms cause direct soil splashing onto bottom leaves and maintain persistent saturation in the microclimate.",
                    "explanation_hi": "तेज बारिश से मिट्टी के कण निचली पत्तियों पर उछलते हैं जिससे फफूंद का फैलाव तेजी से होता है।"
                })
            else:
                env_factors.append({
                    "factor": "Moderate Dew & Microclimate Saturation",
                    "factor_hi": "सुबह की ओस और स्थानीय नमी का जमाव",
                    "impact_level": "Medium",
                    "explanation": "Nocturnal dew formation in combination with 20°C–28°C temperatures creates recurring infection windows.",
                    "explanation_hi": "रात और सुबह के समय पत्तों पर ओस ठहरने से रोगजनक कवक को पनपने में मदद मिलती है।"
                })
        elif "curl" in disease_name.lower():
            env_factors.append({
                "factor": "Warm, Dry Weather Favorable to Insect Vectors",
                "factor_hi": "गर्म और सूखा मौसम (कीटों के अनुकूल)",
                "impact_level": "High",
                "explanation": "Warm spells accelerate whitefly reproductive cycles, causing exponential vector swarms across crop rows.",
                "explanation_hi": "गर्म मौसम में सफेद मक्खी कीट की संख्या तेजी से बढ़ती है, जो इस विषाणु को फैलाती है।"
            })
        else:
            env_factors.append({
                "factor": "Microclimate Temperature Fluctuations",
                "factor_hi": "मौसम और तापमान में उतार-चढ़ाव",
                "impact_level": "Medium",
                "explanation": "Sudden shifts in temperature weaken host physiological defense mechanisms against opportunist pathogens.",
                "explanation_hi": "तापमान में अचानक बदलाव से पौधे की प्राकृतिक रोग प्रतिरोधक क्षमता कमजोर पड़ जाती है।"
            })

        # 2. Farming-Related Factors
        if "daily" in irrigation.lower() or "flood" in irrigation.lower() or "overhead" in irrigation.lower():
            farm_factors.append({
                "factor": "Frequent or Overhead Irrigation Practices",
                "factor_hi": "बार-बार या ऊपर से फव्वारा सिंचाई",
                "impact_level": "High",
                "explanation": "Overhead watering wets the entire foliar canopy and washes pathogen spores from infected leaves onto healthy foliage.",
                "explanation_hi": "ऊपर से पानी देने से पूरी पत्तियां गीली हो जाती हैं और पानी के छींटों से रोग अन्य पत्तियों तक फैलता है।"
            })
        else:
            farm_factors.append({
                "factor": "Irrigation Interval & Canopy Aeration",
                "factor_hi": "सिंचाई अंतराल और पौधों में हवा का संचार",
                "impact_level": "Medium",
                "explanation": "Even moderate watering can trap moisture if plant rows are tightly spaced with limited cross-ventilation.",
                "explanation_hi": "पौधे अधिक पास-पास होने पर सिंचाई की नमी नीचे ही फंसी रह जाती है और हवा नहीं लग पाती।"
            })

        if "poor" in drainage.lower() or "waterlogged" in drainage.lower():
            farm_factors.append({
                "factor": "Poor Field Drainage & Waterlogging",
                "factor_hi": "खेत में खराब जल निकासी व जलभराव",
                "impact_level": "High",
                "explanation": "Stagnant standing water suffocates root hairs, inducing physiological hypoxia and opening roots to vascular wilt pathogens.",
                "explanation_hi": "जड़ों के पास पानी जमा रहने से पौधे को ऑक्सीजन नहीं मिलती और पौधे की जड़ें कमजोर हो जाती हैं।"
            })

        # 3. Biological & Crop Vulnerability Factors
        if "flowering" in growth_stage.lower() or "fruiting" in growth_stage.lower():
            bio_factors.append({
                "factor": f"High Sink Demand during {growth_stage} Phase",
                "factor_hi": f"{growth_stage} अवस्था में पौधे का अधिक ऊर्जा व्यय",
                "impact_level": "High",
                "explanation": "During reproductive development, the plant allocates massive carbohydrates to fruit/flower organs, reducing foliar secondary metabolite defenses.",
                "explanation_hi": "फूल और फल बनते समय पौधे की अधिकांश ऊर्जा उपज में लगती है, जिससे पत्तियां संक्रमण के प्रति अधिक संवेदनशील हो जाती हैं।"
            })

        if "1-2 weeks" in duration.lower() or ">2 weeks" in duration.lower():
            bio_factors.append({
                "factor": f"Prolonged Inoculum Residence ({duration})",
                "factor_hi": f"लक्षणों की लंबी अवधि ({duration})",
                "impact_level": "High",
                "explanation": "Symptoms have persisted over multiple life-cycles, indicating secondary sporulation has established within the plot.",
                "explanation_hi": "रोग काफी दिनों से मौजूद है, जिसका अर्थ है कि खेत में कवक ने अपनी अगली पीढ़ी तैयार कर ली है।"
            })

        # Compile humble, cautious summaries
        possible_causes_en = [f["factor"].lower() for f in (env_factors + farm_factors)[:3]]
        summary_en = (
            f"Possible reasons include {', '.join(possible_causes_en)}. "
            f"Image analysis combined with your farm conditions suggests this may be related to prolonged leaf surface wetness, "
            f"microclimate humidity ({humidity_pct}%), and localized canopy aeration."
        )

        summary_hi = (
            f"संभावित कारणों में {env_factors[0]['factor_hi']} तथा {farm_factors[0]['factor_hi']} शामिल हो सकते हैं। "
            f"पत्ती की फोटो और आपके खेत की स्थिति दर्शाती है कि यह समस्या अधिक नमी, मौसम में उमस ({humidity_pct}%), "
            f"और पौधों के बीच हवा की कमी से जुड़ी हो सकती है।"
        )

        # Farm conditions overview
        farm_conditions = {
            "temperature_c": temp_c,
            "humidity_pct": humidity_pct,
            "rainfall_status": rainfall,
            "irrigation_practice": irrigation,
            "soil_drainage": drainage,
            "crop_growth_stage": growth_stage,
            "crop_age": crop_age,
            "affected_area_pct": affected_area,
            "location": location,
            "impact_summary_en": f"Current farm conditions ({temp_c}°C, {humidity_pct}% humidity with {drainage.lower()} drainage) indicate a favorable environment for foliar pathogens.",
            "impact_summary_hi": f"वर्तमान खेत की स्थिति ({temp_c}°C तापमान, {humidity_pct}% उमस व {drainage} जल निकासी) दर्शाती है कि परिस्थितियां फंगल संक्रमण के अनुकूल हैं।"
        }

        # Flat list of contributing factors for backwards compatibility
        all_factors = []
        for f in env_factors:
            all_factors.append({
                "category": "Environmental Factor",
                "category_hi": "पर्यावरणीय कारक",
                "factor": f["factor"],
                "factor_hi": f.get("factor_hi", f["factor"]),
                "impact_level": f["impact_level"],
                "scientific_rationale": f["explanation"],
                "scientific_rationale_hi": f.get("explanation_hi", f["explanation"])
            })
        for f in farm_factors:
            all_factors.append({
                "category": "Farming-Related Factor",
                "category_hi": "खेती संबंधी कारक",
                "factor": f["factor"],
                "factor_hi": f.get("factor_hi", f["factor"]),
                "impact_level": f["impact_level"],
                "scientific_rationale": f["explanation"],
                "scientific_rationale_hi": f.get("explanation_hi", f["explanation"])
            })
        for f in bio_factors:
            all_factors.append({
                "category": "Crop & Biological Factor",
                "category_hi": "फसल व जैविक कारक",
                "factor": f["factor"],
                "factor_hi": f.get("factor_hi", f["factor"]),
                "impact_level": f["impact_level"],
                "scientific_rationale": f["explanation"],
                "scientific_rationale_hi": f.get("explanation_hi", f["explanation"])
            })

        return {
            "primary_summary": summary_en,
            "primary_summary_hi": summary_hi,
            "cautious_disclaimer": "Important: An image alone cannot establish a single definitive cause. These are potential contributing factors based on visual symptoms and field context.",
            "environmental_factors": env_factors,
            "farming_factors": farm_factors,
            "biological_factors": bio_factors,
            "contributing_factors": all_factors,
            "farm_conditions": farm_conditions,
            "context_insights": [
                f"Growth phase: {growth_stage}",
                f"Recent rainfall: {rainfall}",
                f"Irrigation schedule: {irrigation}",
                f"Symptom duration: {duration}"
            ]
        }
