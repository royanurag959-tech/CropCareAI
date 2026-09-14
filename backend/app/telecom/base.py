from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTelecomProvider(ABC):
    """
    Abstract base class for Telecom Gateways in CropCare AI.
    Handles IVR voice helplines and cellular SMS short-codes for 2G feature phones.
    """

    @abstractmethod
    def process_ivr_call(
        self,
        caller_phone: str,
        language: str,
        crop: str,
        symptoms_key: str,
        keypad_input: str = "1"
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def process_sms_query(
        self,
        sender_phone: str,
        message: str
    ) -> Dict[str, Any]:
        pass
