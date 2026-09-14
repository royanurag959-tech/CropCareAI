from typing import Dict, Any
from app.telecom.base import BaseTelecomProvider

class MockTelecomProvider(BaseTelecomProvider):
    """
    Simulated Telecom Gateway for hackathons and demo mode.
    Emulates IVR 1800 voice menus and cellular 160-character SMS queries.
    """

    def __init__(self):
        self.provider_name = "MockTelecomProvider (Keypad IVR & SMS Gateway)"

    def process_ivr_call(
        self,
        caller_phone: str,
        language: str,
        crop: str,
        symptoms_key: str,
        keypad_input: str = "1"
    ) -> Dict[str, Any]:
        lang = (language or "hi").lower()
        crop_name = (crop or "Tomato").title()
        sym = (symptoms_key or "spots").lower()

        # Handle keypad 9: Request expert assistance
        if keypad_input == "9":
            script_hi = (
                f"आपका अनुरोध दर्ज कर लिया गया है। हमारे कृषि विशेषज्ञ जल्द ही {crop_name} "
                f"फसल की जांच के लिए आपके मोबाइल {caller_phone} पर संपर्क करेंगे। धन्यवाद।"
            )
            script_en = (
                f"Your request has been registered. An agricultural expert will call your number {caller_phone} "
                f"shortly to assist with your {crop_name} crop. Thank you."
            )
            return {
                "call_status": "expert_requested",
                "caller_phone": caller_phone,
                "language": lang,
                "crop": crop_name,
                "symptoms_key": sym,
                "predicted_disease": f"{crop_name} Condition - Expert Triage",
                "voice_script": script_hi if lang == "hi" else script_en,
                "expert_callback_scheduled": True,
                "provider_name": self.provider_name
            }

        # Disease match based on symptom key
        if "spot" in sym or "blight" in sym:
            if crop_name == "Tomato":
                disease = "Tomato Leaf Blight"
                advice_hi = "संभावित रोग टमाटर पत्ता झुलसा है। अधिक नमी के कारण हो सकता है। रोगी पत्तों को तोड़कर अलग करें और धूप आने दें। विशेषज्ञ से बात करने के लिए 9 दबाएं।"
                advice_en = "Possible disease is Tomato Leaf Blight caused by excess moisture. Remove affected lower leaves and improve aeration. Press 9 to request an expert callback."
            elif crop_name == "Potato":
                disease = "Potato Early Blight"
                advice_hi = "संभावित रोग आलू अगेती झुलसा है। शाम के समय पत्तियों पर पानी न डालें और संतुलित पोटाश दें। विशेषज्ञ से बात करने के लिए 9 दबाएं।"
                advice_en = "Possible disease is Potato Early Blight. Avoid late evening watering and ensure balanced potassium. Press 9 to request an expert callback."
            else:
                disease = f"{crop_name} Leaf Spot"
                advice_hi = f"संभावित रोग {crop_name} पत्ती धब्बा है। खेत में जलभराव न होने दें। विशेषज्ञ से बात करने के लिए 9 दबाएं।"
                advice_en = f"Possible condition is {crop_name} Leaf Spot. Avoid stagnant water in the field. Press 9 to request an expert callback."
        elif "curl" in sym or "yellow" in sym:
            disease = f"{crop_name} Yellow Leaf Curl"
            advice_hi = "संभावित रोग पत्ती मरोड़ विषाणु है जो सफेद मक्खी से फैलता है। पीले चिपचिपे ट्रैप लगाएं और नीम तेल का छिड़काव करें। विशेषज्ञ से बात करने के लिए 9 दबाएं।"
            advice_en = "Possible viral leaf curl transmitted by whiteflies. Install yellow sticky traps and spray neem oil. Press 9 to request an expert callback."
        else:
            disease = f"{crop_name} Moisture Stress"
            advice_hi = "फसल में नमी या पोषक तत्वों का असंतुलन हो सकता है। विशेषज्ञ से बात करने के लिए 9 दबाएं।"
            advice_en = "Your crop may have moisture stress or nutrient imbalance. Press 9 to request an expert callback."

        voice_script = advice_hi if lang == "hi" else advice_en

        return {
            "call_status": "in_progress",
            "caller_phone": caller_phone,
            "language": lang,
            "crop": crop_name,
            "symptoms_key": sym,
            "predicted_disease": disease,
            "voice_script": voice_script,
            "recommended_action_hi": advice_hi,
            "recommended_action_en": advice_en,
            "audio_tts_ready": True,
            "provider_name": self.provider_name
        }

    def process_sms_query(
        self,
        sender_phone: str,
        message: str
    ) -> Dict[str, Any]:
        raw_msg = message.strip().upper()

        if "EXPERT" in raw_msg or "मदद" in raw_msg or "HELP" in raw_msg:
            sms_reply = f"CropCare: Expert review registered for {sender_phone}. A certified Krishi expert will call you within 2 hours. Helpline: 18001801551"
            return {
                "sender_phone": sender_phone,
                "original_query": message,
                "inferred_crop": "General",
                "predicted_disease": "Expert Assistance",
                "sms_response": sms_reply,
                "character_count": len(sms_reply),
                "status": "delivered",
                "provider_name": self.provider_name
            }

        crop = "Tomato"
        if "POTATO" in raw_msg or "आलू" in raw_msg:
            crop = "Potato"
        elif "RICE" in raw_msg or "धान" in raw_msg:
            crop = "Rice"
        elif "WHEAT" in raw_msg or "गेहूं" in raw_msg:
            crop = "Wheat"
        elif "APPLE" in raw_msg or "सेब" in raw_msg:
            crop = "Apple"
        elif "COTTON" in raw_msg or "कपास" in raw_msg:
            crop = "Cotton"

        if "CURL" in raw_msg or "मरोड़" in raw_msg or "YELLOW" in raw_msg:
            disease = f"{crop} Leaf Curl Virus"
            sms_reply = f"CropCare SMS: {crop} Leaf Curl detected. Vector: Whitefly. Action: Uproot stunted plants, set yellow sticky traps, spray neem oil. Reply EXPERT for help."
        elif "BLAST" in raw_msg or "झोंका" in raw_msg:
            disease = "Rice Blast"
            sms_reply = "CropCare SMS: Rice Blast detected. Action: Stop urea nitrogen. Drain excess water. Spray bio-fungicide as per label. Reply EXPERT for doctor call."
        else:
            disease = f"{crop} Leaf Blight"
            sms_reply = f"CropCare SMS: {crop} Leaf Blight detected. Cause: Excess moisture/humidity. Action: Pluck infected leaves, avoid overhead watering. Reply EXPERT for help."

        return {
            "sender_phone": sender_phone,
            "original_query": message,
            "inferred_crop": crop,
            "predicted_disease": disease,
            "sms_response": sms_reply,
            "character_count": len(sms_reply),
            "status": "delivered",
            "provider_name": self.provider_name
        }
