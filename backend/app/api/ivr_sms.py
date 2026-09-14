from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.schemas import IVRCallRequest, SMSQueryRequest
from app.telecom.factory import get_telecom_provider

router = APIRouter(prefix="/telecom", tags=["IVR Helpline & SMS for Basic Phones"])

@router.post("/ivr")
def process_ivr_call(payload: IVRCallRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Simulates IVR telecom gateway via modular TelecomProvider:
    Keypad digits: 1=Language, 2=Crop, 3=Symptoms, 9=Request Expert Assistance.
    """
    provider = get_telecom_provider()
    return provider.process_ivr_call(
        caller_phone=payload.caller_phone,
        language=payload.language,
        crop=payload.crop,
        symptoms_key=payload.symptoms_key,
        keypad_input=payload.keypad_input or "1"
    )

@router.post("/sms")
def process_sms_query(payload: SMSQueryRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Simulates inbound SMS short-code gateway via modular TelecomProvider:
    Handles keywords like 'TOMATO LEAF SPOTS', 'धान झोंका', 'EXPERT'.
    """
    provider = get_telecom_provider()
    return provider.process_sms_query(
        sender_phone=payload.sender_phone,
        message=payload.message
    )
