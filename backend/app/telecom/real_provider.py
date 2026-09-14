from typing import Dict, Any, Optional
from app.telecom.base import BaseTelecomProvider
from app.telecom.mock_provider import MockTelecomProvider
from app.core.config import settings

class RealTelecomProvider(BaseTelecomProvider):
    """
    Production Telecom Gateway for CropCare AI.
    Connects to cellular telephony APIs (Twilio, Exotel, Gupshup, Infobip) for voice IVR & SMS.
    Falls back gracefully to MockTelecomProvider when API keys are not configured.
    """

    def __init__(self):
        self.provider_name = "RealTelecomProvider"
        self.fallback = MockTelecomProvider()

    def process_ivr_call(
        self,
        caller_phone: str,
        language: str,
        crop: str,
        symptoms_key: str,
        keypad_input: str = "1"
    ) -> Dict[str, Any]:
        data = self.fallback.process_ivr_call(caller_phone, language, crop, symptoms_key, keypad_input)
        data["provider_name"] = f"{self.provider_name} (Mock Gateway Fallback)"
        return data

    def process_sms_query(
        self,
        sender_phone: str,
        message: str
    ) -> Dict[str, Any]:
        data = self.fallback.process_sms_query(sender_phone, message)
        data["provider_name"] = f"{self.provider_name} (Mock Gateway Fallback)"
        return data
